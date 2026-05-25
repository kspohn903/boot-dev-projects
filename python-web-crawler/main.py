import sys
import asyncio
import aiohttp
import datetime 
from urllib.parse import urlparse, urljoin
from crawl import normalize_url, extract_page_data
from csv_report import write_csv_report

class AsyncCrawler:
    """
    Manages shared state, concurrency control, and stopping logic 
    for the asynchronous web crawler.
    """
    def __init__(self, base_url: str, max_concurrency: int, max_pages: int):
        # State Management
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {} # Stores data for successful/failed/crawling pages

        # Concurrency Control
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None  # aiohttp.ClientSession initialized in __aenter__
        
        # Stopping mechanism
        self.should_stop = False
        self.all_tasks = set() # Set of all active crawl_page tasks for cancellation

        # Initial validation
        if not self.base_domain:
            raise ValueError("Invalid base URL: Could not extract domain.")
        
    # --- Async Context Manager Methods ---
    async def __aenter__(self):
        """Initializes the aiohttp ClientSession when entering the context."""
        # Custom headers including the User-Agent
        headers = {"User-Agent": "BootCrawler/1.0"}
        # Use ClientTimeout to ensure requests don't hang indefinitely
        timeout = aiohttp.ClientTimeout(total=15)
        self.session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the aiohttp ClientSession when exiting the context."""
        await self.session.close()

    # --- Core Crawler Methods ---

    async def add_page_visit(self, normalized_url: str) -> bool:
        """
        Safely checks and marks a page as being visited.
        Returns True if it's the first time visiting, False otherwise.
        Stops the crawler if max_pages is reached.
        """
        # Immediately return if another task has already requested a stop
        if self.should_stop:
            return False
            
        # Use the lock to safely access shared state (self.page_data)
        async with self.lock:
            # 1. Check if already known
            if normalized_url in self.page_data:
                return False
            
            # 2. Check page limit (0 means no limit)
            # len(self.page_data) counts all pages (crawling, failed, or complete)
            if self.max_pages > 0 and len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("\nReached maximum number of pages to crawl. Stopping all tasks.")
                
                # Cancel all running tasks in the set
                for task in self.all_tasks:
                    task.cancel()
                    
                return False

            # 3. Mark as 'crawling' and allow the crawl to proceed
            self.page_data[normalized_url] = {"status": "crawling"}
            return True

    async def get_html(self, url: str) -> str:
        """
        Fetches the HTML content of a URL using aiohttp.
        """
        # The session already includes the User-Agent and timeout
        async with self.session.get(url) as response:
            
            # 1. Return an error if the HTTP status code is an error-level code (400+)
            if response.status >= 400:
                raise Exception(f"HTTP error: Status code {response.status} for URL {url}")

            # 2. Return an error if the response content-type header is not an acceptable format.
            content_type = response.content_type.lower()
            
            acceptable_content_types = [
                'text/html', 
                'application/xml', 
                'text/xml', 
                'application/atom+xml', 
                'application/rss+xml'
            ]

            if content_type not in acceptable_content_types:
                raise Exception(f"Unsupported content: Expected one of {acceptable_content_types} but got '{content_type}'")

            # 3. Read and return the webpage's content (text)
            return await response.text()

    async def crawl_page(self, current_url: str):
        """
        Asynchronously fetches a page, extracts data, and queues new pages.
        """
        # Check if cancellation has been requested
        if self.should_stop:
            return

        # Get the current running Task object
        current_task = asyncio.current_task()
        
        # Use try/finally to ensure the task is removed from the active set
        try:
            # 1. Domain restriction check
            try:
                current_domain = urlparse(current_url).netloc
                if current_domain != self.base_domain:
                    return # External link, stop recursion
            except Exception:
                print(f"Skipping invalid URL: {current_url}")
                return
                
            normalized_url = normalize_url(current_url)

            # 2. Check and mark page visit safely
            if not await self.add_page_visit(normalized_url):
                # Only print 'Already crawled' if the page was previously known, not if we stopped
                if normalized_url in self.page_data and not self.should_stop:
                    status = self.page_data[normalized_url].get('status', 'complete')
                    print(f"Already crawled ({status}): {current_url} -> {normalized_url}")
                return

            print(f"CRAWLING: {current_url} -> {normalized_url}")
            
            # Immediate stop check after adding the page, in case add_page_visit set the flag
            if self.should_stop:
                return
            
            # 3. Limit the number of concurrent requests with the semaphore
            async with self.semaphore:
                
                html_content = ""
                outgoing_links = []
                
                # 4. Fetch the HTML
                try:
                    html_content = await self.get_html(current_url)
                except Exception as e:
                    print(f"Error fetching {current_url}: {e}")
                    async with self.lock:
                        self.page_data[normalized_url] = {"status": "failed_fetch", "error": str(e)}
                    return

                # 5. Extract data and safely update page_data
                try:
                    extracted_data = extract_page_data(html_content, current_url)
                    outgoing_links = extracted_data.get('outgoing_links', [])
                    
                    async with self.lock:
                        # Success: overwrite the entry, removing the 'status' key
                        self.page_data[normalized_url] = extracted_data
                        
                except Exception as e:
                    print(f"Error extracting data from {current_url}: {e}")
                    async with self.lock:
                        self.page_data[normalized_url] = {"status": "failed_extraction", "error": str(e)}
                    return

            # 6. Create tasks for all internal outgoing links
            child_tasks = []
            for link in outgoing_links:
                # Check for stop condition before creating new tasks
                if self.should_stop:
                    break
                
                # --- FIX: Resolve relative links before domain check ---
                # Convert relative links (like /posts/a-post) to absolute URLs against the current page's URL
                absolute_link = urljoin(current_url, link) 
                
                link_domain = urlparse(absolute_link).netloc
                if link_domain == self.base_domain:
                    # Create a new concurrent task for the linked page
                    task = asyncio.create_task(self.crawl_page(absolute_link)) # Use absolute_link
                    
                    # Add task to the global set for cancellation, must be done under lock!
                    async with self.lock:
                        self.all_tasks.add(task)
                    
                    child_tasks.append(task)
                    
            # 7. Wait for all child tasks started from this page to complete
            await asyncio.gather(*child_tasks)
            
        except asyncio.CancelledError:
            # Expected if cancellation comes from the limit being hit
            pass
        finally:
            # Safely remove this task from the active set if it was added
            async with self.lock:
                if current_task in self.all_tasks:
                    self.all_tasks.remove(current_task)

    async def crawl(self) -> dict:
        """Starts the crawl process from the base URL."""
        # Create the initial task and add it to the set for uniform management
        initial_task = asyncio.create_task(self.crawl_page(self.base_url))
        
        async with self.lock:
            self.all_tasks.add(initial_task)
            
        # Wait for the initial task and all its recursive children to complete
        try:
            await initial_task
        except asyncio.CancelledError:
            # Expected if the limit was reached
            pass
        
        # After the initial task graph completes/is cancelled, wait for any remaining tasks 
        # (which should be tasks that were running concurrently when cancellation occurred)
        remaining_tasks = list(self.all_tasks)
        if remaining_tasks:
            # Gather with return_exceptions=True to safely handle potentially cancelled tasks
            await asyncio.gather(*remaining_tasks, return_exceptions=True)
            
        return self.page_data

# --- New Async Site Entry Point ---

async def crawl_site_async(base_url: str, max_concurrency: int, max_pages: int) -> dict:
    """
    The main asynchronous orchestrator function.
    """
    # Use the AsyncCrawler context manager to ensure the session is closed
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        final_data = await crawler.crawl()
        return final_data

# --- Main Execution Logic ---

async def main_async():
    """
    Handles command line arguments and initiates the asynchronous crawl.
    """
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: uv run main.py URL [max_concurrency] [max_pages]")
        sys.exit(1)
    
    base_url = sys.argv[1]
    
    # Default settings (used if not provided)
    max_concurrency = 5
    max_pages = 0 # 0 means no limit
    
    # Parse max_concurrency
    if len(sys.argv) > 2:
        try:
            max_concurrency = int(sys.argv[2])
            if max_concurrency < 1:
                raise ValueError
        except ValueError:
            print("Error: max_concurrency must be a positive integer (e.g., 3).")
            sys.exit(1)

    # Parse max_pages
    if len(sys.argv) > 3:
        try:
            max_pages = int(sys.argv[3])
            if max_pages < 0:
                raise ValueError
        except ValueError:
            print("Error: max_pages must be a non-negative integer (e.g., 10).")
            sys.exit(1)
            
    # Simple validation outside of the crawler class
    try:
        normalized_base_url = normalize_url(base_url)
    except Exception as e:
        print(f"Error processing base URL: {e}")
        sys.exit(1)
        
    page_limit_str = f"Limit: {max_pages} pages" if max_pages > 0 else "Limit: None"
    print(f"Starting crawl of: {normalized_base_url} (Concurrency: {max_concurrency}, {page_limit_str})")
    
    try:
        # Pass the configurable values to crawl_site_async
        final_data = await crawl_site_async(base_url, max_concurrency, max_pages)
        
        print("\n--- CRAWL COMPLETE ---")
        
        # 1. Calculate statistics
        successful_pages = {k: v for k, v in final_data.items() if 'status' not in v}
        
        # Group failed pages by their status
        failed_pages = {k: v for k, v in final_data.items() if 'status' in v}
        status_counts = {}
        for page in failed_pages.values():
            status = page['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Report
        pages_crawled = len(successful_pages)
        pages_skipped_failed = len(failed_pages)
        
        print(f"Successfully crawled {pages_crawled} unique pages.")
        
        if pages_skipped_failed > 0:
            print(f"Total skipped or failed pages: {pages_skipped_failed}")
            for status, count in status_counts.items():
                # Format status strings for better readability
                readable_status = status.replace('_', ' ').capitalize()
                print(f"  - {readable_status}: {count}")
        else:
            print("No pages skipped or failed.")
        
        # 2. Export the successful data to CSV
        try:
            # --- Generate the unique, domain-specific filename ---
            
            # Extract FQDN (Fully Qualified Domain Name)
            domain = urlparse(base_url).netloc
            
            # Generate a detailed timestamp including milliseconds (SSS)
            now = datetime.datetime.now()
            # YYYY_MM_DD_HH_MM format
            dt_part = now.strftime("%Y_%m_%d_%H_%M")
            # Millisecond part (3 digits, zero-padded)
            ms_part = str(now.microsecond // 1000).zfill(3)
            
            timestamp_string = f"{dt_part}_{ms_part}"
            
            # Construct the unique filename: report_dtstring(YYYY_MM_DD_HH_MM_SSS)_url_fqdn.csv
            output_filename = f"report_{timestamp_string}_{domain}.csv"
            
            # Pass the unique filename to the report function
            write_csv_report(final_data, output_filename)
            print(f"Report saved to {output_filename}")
        except Exception as e:
            print(f"Error writing CSV report: {e}")
            
    except aiohttp.ClientError as e:
        print(f"A client request error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        # Catch unexpected errors, but also catch KeyboardInterrupt for clean exit
        if not isinstance(e, (KeyboardInterrupt, SystemExit)):
             print(f"An unexpected error occurred during crawling: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Use asyncio.run() to launch the asynchronous main function
    asyncio.run(main_async())

