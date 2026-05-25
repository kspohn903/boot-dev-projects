from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def normalize_urls_testing(test_urls):
    print("--- Normalization Examples ---")
    for url in test_urls:
        print(f"Input:  {url}")
        print(f"Output: {normalize_url(url)}")
        print("-" * 20)

def normalize_url(url: str) -> str:
    """
    Normalizes a URL string by:
    1. Removing the scheme (http, https).
    2. Lowercasing the hostname.
    3. Removing query parameters, fragments, and userinfo.
    4. Removing any trailing slash from the path.
    
    The resulting format is: hostname/path
    """

    # 1. Parse the raw URL string
    try:
        parsed_url = urlparse(url)
    except Exception:
        # Handle simple parsing errors gracefully, though input is assumed valid
        return url
        
    # 2. Extract network location (hostname and port) and path
    # Hostnames are case-insensitive, so we lowercase the netloc for normalization.
    netloc = parsed_url.netloc.lower()
    path = parsed_url.path
    
    # 3. Combine them: netloc and path naturally exclude scheme, query, and fragment.
    normalized = netloc + path
    
    # 4. Remove a trailing slash if present
    if normalized.endswith('/'):
        # Use slicing to remove the last character
        normalized = normalized[:-1]
        
    return normalized

def get_h1_from_html(html: str) -> str:
    """
    Extracts the text content of the first <h1> tag found in the HTML.
    Returns an empty string if no <h1> tag is found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    return "" if (h1_tag is None) else (h1_tag.get_text().strip())
    # get_text() extracts text content, strip() removes leading/trailing whitespace

def get_first_paragraph_from_html(html: str) -> str:
    """
    Extracts the text content of the first meaningful paragraph.
    Prioritizes the first <p> tag inside a <main> tag.
    Falls back to the first <p> tag in the entire document if <main> is not found.
    Returns an empty string if no <p> tag is found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Search for the <main> tag
    container = soup.find('main')
    
    # 2. If <main> is not found, use the whole soup object as the container
    if container is None:
        container = soup
        
    # 3. Find the first <p> tag within the chosen container (main or soup)
    first_p = container.find('p')    
    return ("") if (first_p is None) else (first_p.get_text().strip())

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    """
    Extracts all URLs from <a> tags in the HTML and converts relative URLs 
    to absolute URLs using the base_url.
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    
    # Find all <a> tags
    a_tags = soup.find_all('a')
    
    for tag in a_tags:
        # Safely get the href attribute
        href = tag.get('href')
        if href:
            # urljoin combines the base URL with the (absolute or relative) href
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    
    return urls

def get_images_from_html(html: str, base_url: str) -> list[str]:
    """
    Extracts all image URLs from <img> tags in the HTML and converts relative URLs
    to absolute URLs using the base_url.
    """
    # Fixed typo in parser name: 'html.parser' changed to 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    image_urls = []
    
    # Find all <img> tags
    img_tags = soup.find_all('img')
    
    for tag in img_tags:
        # Safely get the src attribute
        src = tag.get('src')
        if src:
            # urljoin combines the base URL with the (absolute or relative) src
            absolute_url = urljoin(base_url, src)
            image_urls.append(absolute_url)
    
    return image_urls

def extract_page_data(html: str, page_url: str) -> dict:
    """
    Extracts core data points from an HTML page using existing helper functions.
    
    Returns a dictionary with keys: 
    url, h1, first_paragraph, outgoing_links, image_urls
    """
    data = {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }
    return data

if __name__ == '__main__':
   # Example usage for quick local testing (not part of the module export)
   test_urls = [
        "https://blog.boot.dev/path/",
        "http://blog.boot.dev/path",
        "https://Boot.Dev:8080/PATH/to/file/",
        "https://blog.boot.dev/path?query=1&sort=asc#fragment"
   ]
   normalize_urls_testing(test_urls)
    
   
