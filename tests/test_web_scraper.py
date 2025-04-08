"""
Unit tests for the web scraping tool.
"""
import unittest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
import requests
from tools.web_scrape import WebScraper

class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = WebScraper()
        self.test_html = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <h1>Main Heading</h1>
                <h2>Sub Heading</h2>
                <main>
                    <p>Main content here</p>
                    <a href="/docs">Documentation</a>
                    <a href="/api">API Reference</a>
                    <a href="/other">Other Link</a>
                </main>
            </body>
        </html>
        """
        self.test_soup = BeautifulSoup(self.test_html, 'html.parser')
    
    def test_get_title(self):
        """Test title extraction."""
        title = self.scraper._get_title(self.test_soup)
        self.assertEqual(title, "Test Page")
    
    def test_get_headings(self):
        """Test headings extraction."""
        headings = self.scraper._get_headings(self.test_soup)
        self.assertEqual(headings, ["Main Heading", "Sub Heading"])
    
    def test_get_main_content(self):
        """Test main content extraction."""
        content = self.scraper._get_main_content(self.test_soup)
        self.assertIn("Main content here", content)
    
    def test_get_relevant_links(self):
        """Test relevant links extraction."""
        links = self.scraper._get_relevant_links(self.test_soup)
        self.assertEqual(len(links), 2)  # Should find doc and api links
        self.assertTrue(any(link['url'] == '/docs' for link in links))
        self.assertTrue(any(link['url'] == '/api' for link in links))
    
    @patch('requests.get')
    def test_scrape_success(self, mock_get):
        """Test successful scraping."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = self.test_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.scraper.scrape("https://test.com")
        
        self.assertEqual(result['title'], "Test Page")
        self.assertEqual(len(result['headings']), 2)
        self.assertTrue(result['content'])
        self.assertEqual(len(result['links']), 2)
    
    @patch('requests.get')
    def test_scrape_failure(self, mock_get):
        """Test scraping failure."""
        # Mock failed response
        mock_get.side_effect = requests.exceptions.RequestException("Test error")
        
        result = self.scraper.scrape("https://test.com")
        
        self.assertIn('error', result)
        self.assertEqual(result['url'], "https://test.com")

if __name__ == '__main__':
    unittest.main() 