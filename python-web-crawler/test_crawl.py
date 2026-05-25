import unittest
from crawl import (
    get_h1_from_html, 
    get_first_paragraph_from_html, 
    get_urls_from_html, 
    get_images_from_html,
    extract_page_data # New function import
)

class TestContentExtraction(unittest.TestCase):

    # --- Tests for get_h1_from_html (Previous tests included for completeness) ---
    
    def test_get_h1_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_not_found(self):
        input_body = '<html><body><h2>Not H1</h2><p>text</p></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_nested_content(self):
        input_body = '<html><body><h1>Welcome to <span>Boot.dev</span>!</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Welcome to Boot.dev!"
        self.assertEqual(actual, expected)
        
    def test_get_h1_from_html_whitespace(self):
        input_body = '<html><body> <h1>   Title with Space   </h1> </body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Title with Space"
        self.assertEqual(actual, expected)


    # --- Tests for get_first_paragraph_from_html (Previous tests included for completeness) ---

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main_fallback(self):
        input_body = '''<html><body>
            <p>First paragraph, no main.</p>
            <div><p>Second paragraph.</p></div>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph, no main."
        self.assertEqual(actual, expected)
        
    def test_get_first_paragraph_from_html_empty_or_missing(self):
        input_body = '<html><body><h1>Title</h1><div><span>text</span></div></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_only_main_empty_p(self):
        input_body = '''<html><body>
            <p>The document P.</p>
            <main>
                <div>Not a paragraph</div>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "" 
        self.assertEqual(actual, expected)
        
    # --- Tests for get_urls_from_html (Previous tests included for completeness) ---

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev/path"
        input_body = '<html><body><a href="https://blog.boot.dev/other">Boot.dev</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/other"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://example.com/blog/"
        input_body = '<html><body><a href="/about">About Us</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://example.com/about"]
        self.assertEqual(actual, expected)
        
    def test_get_urls_from_html_multiple_and_mixed(self):
        input_url = "https://example.com"
        input_body = '''<html><body>
            <a href="/contact">Contact</a>
            <a href="https://google.com">Google</a>
            <a href="/services">Services</a>
            <a>No Href</a>
            </body></html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://example.com/contact",
            "https://google.com",
            "https://example.com/services"
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://example.com"
        input_body = '<html><body><p>Just text</p></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
        
    # --- Tests for get_images_from_html (Previous tests included for completeness) ---

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)
        
    def test_get_images_from_html_absolute_and_no_src(self):
        input_url = "https://example.net/page"
        input_body = '''<html><body>
            <img src="https://images.example.net/pic.jpg" alt="pic">
            <img alt="no src here">
            <img src="icon.svg">
            </body></html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://images.example.net/pic.jpg",
            "https://example.net/icon.svg" 
        ]
        self.assertEqual(actual, expected)
        
    def test_get_images_from_html_multiple_and_subpath(self):
        input_url = "https://host.co/docs/"
        input_body = '''<html><body>
            <img src="./assets/icon.svg">
            <img src="https://static.host.co/ads/banner.gif">
            <img src="sidebar/widget.png">
            </body></html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://host.co/docs/assets/icon.svg",
            "https://static.host.co/ads/banner.gif",
            "https://host.co/docs/sidebar/widget.png"
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://example.com"
        input_body = '<html><body><a href="/home">Home</a></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
        
    # --- Tests for extract_page_data ---
    
    def test_extract_page_data_basic(self):
        # The example test case provided in the assignment
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)
        
    def test_extract_page_data_missing_elements(self):
        # Case where <h1> and <img> are missing, and links are absolute
        input_url = "https://no-h1.net"
        input_body = '''<html><body>
            <h2>No H1 Here</h2>
            <main><p>Main content paragraph.</p></main>
            <a href="https://other.net/external">External Link</a>
            </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://no-h1.net",
            "h1": "", 
            "first_paragraph": "Main content paragraph.", 
            "outgoing_links": ["https://other.net/external"],
            "image_urls": [] 
        }
        self.assertEqual(actual, expected)
        
    def test_extract_page_data_all_elements_present_complex(self):
        # Case with main, multiple links/images, and relative URLs
        # Base URL: http://web.org/path/sub (No trailing slash)
        input_url = "http://web.org/path/sub"
        input_body = '''<html><head>
            <title>Web Page</title>
        </head><body>
            <h1>Final Assignment Title</h1>
            <p>Ignore this paragraph (not in main).</p>
            <main>
                <p>The first main paragraph content.</p>
                <a href="../relative.html">Up one level</a>
                <img src="/global/logo.png">
                <p>Second paragraph.</p>
                <a href="https://example.com">Absolute link</a>
                <img src="local.gif">
            </main>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "http://web.org/path/sub",
            "h1": "Final Assignment Title",
            "first_paragraph": "The first main paragraph content.",
            # Corrected: ../ on a base without a trailing slash (sub) 
            # results in /relative.html
            "outgoing_links": [
                "http://web.org/relative.html", 
                "https://example.com"
            ],
            # Corrected: local.gif on a base without a trailing slash (sub) replaces the last segment
            "image_urls": [
                "http://web.org/global/logo.png",
                "http://web.org/path/local.gif"
            ]
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

