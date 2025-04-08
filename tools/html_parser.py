import logging
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup
from pathlib import Path

logger = logging.getLogger('html_parser')

class HTMLParser:
    def __init__(self, parser: str = 'html.parser'):
        """
        Initialize the HTML parser.
        
        Args:
            parser: BeautifulSoup parser to use ('html.parser', 'lxml', or 'html5lib')
        """
        self.parser = parser
        
    def parse(self, html_content: str, url: str) -> Dict[str, Any]:
        """
        Parse HTML content and extract relevant information.
        
        Args:
            html_content: Raw HTML content
            url: Source URL of the HTML
            
        Returns:
            Dictionary containing parsed data
        """
        try:
            soup = BeautifulSoup(html_content, self.parser)
            
            # Extract basic information
            title = self._get_title(soup)
            meta_description = self._get_meta_description(soup)
            main_text = self._get_main_text(soup)
            
            # Extract links
            links = self._get_links(soup, url)
            
            # Extract images
            images = self._get_images(soup, url)
            
            return {
                'url': url,
                'title': title,
                'meta_description': meta_description,
                'main_text': main_text,
                'links': links,
                'images': images,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error parsing HTML from {url}: {str(e)}")
            return {
                'url': url,
                'status': 'error',
                'error': str(e)
            }
            
    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.text.strip() if title_tag else ''
        
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta['content'].strip() if meta and 'content' in meta.attrs else ''
        
    def _get_main_text(self, soup: BeautifulSoup) -> str:
        """Extract main text content."""
        # Try to find main content area
        main = soup.find('main') or soup.find('article') or soup.find('body')
        if main:
            # Remove script and style elements
            for element in main(['script', 'style']):
                element.decompose()
            return main.get_text(separator=' ', strip=True)
        return ''
        
    def _get_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract and normalize links."""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            
            # Normalize URL
            if href.startswith('/'):
                href = f"{base_url.rstrip('/')}{href}"
            elif not href.startswith(('http://', 'https://')):
                href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
                
            links.append({
                'url': href,
                'text': text
            })
        return links
        
    def _get_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract and normalize image information."""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Normalize image URL
            if src.startswith('/'):
                src = f"{base_url.rstrip('/')}{src}"
            elif not src.startswith(('http://', 'https://')):
                src = f"{base_url.rstrip('/')}/{src.lstrip('/')}"
                
            images.append({
                'url': src,
                'alt': alt
            })
        return images

def parse_html(html_content: str, url: str, parser: str = 'html.parser') -> Dict[str, Any]:
    """
    Convenience function to parse HTML content.
    
    Args:
        html_content: Raw HTML content
        url: Source URL of the HTML
        parser: BeautifulSoup parser to use
        
    Returns:
        Dictionary containing parsed data
    """
    parser = HTMLParser(parser)
    return parser.parse(html_content, url) 