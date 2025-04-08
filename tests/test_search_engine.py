"""
Unit tests for the search engine tool.
"""
import unittest
from unittest.mock import patch
from tools.search_ddg import SearchEngine

class TestSearchEngine(unittest.TestCase):
    """Test cases for SearchEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.search_engine = SearchEngine(max_results=5)
        self.test_results = [
            {
                'title': 'Test Result 1',
                'link': 'https://test1.com',
                'snippet': 'Test snippet 1'
            },
            {
                'title': 'Test Result 2',
                'link': 'https://test2.com',
                'snippet': 'Test snippet 2'
            }
        ]
    
    @patch('tools.search_ddg.ddg')
    def test_search_success(self, mock_ddg):
        """Test successful search."""
        # Mock successful search
        mock_ddg.return_value = self.test_results
        
        results = self.search_engine.search("test query")
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Test Result 1')
        self.assertEqual(results[1]['link'], 'https://test2.com')
        mock_ddg.assert_called_once_with("test query", max_results=5)
    
    @patch('tools.search_ddg.ddg')
    def test_search_empty_results(self, mock_ddg):
        """Test search with no results."""
        # Mock empty results
        mock_ddg.return_value = []
        
        results = self.search_engine.search("test query")
        
        self.assertEqual(len(results), 0)
    
    @patch('tools.search_ddg.ddg')
    def test_search_failure(self, mock_ddg):
        """Test search failure."""
        # Mock search failure
        mock_ddg.side_effect = Exception("Test error")
        
        results = self.search_engine.search("test query")
        
        self.assertEqual(len(results), 1)
        self.assertIn('error', results[0])
        self.assertEqual(results[0]['query'], "test query")
    
    def test_max_results_limit(self):
        """Test max results parameter."""
        search_engine = SearchEngine(max_results=3)
        self.assertEqual(search_engine.max_results, 3)

if __name__ == '__main__':
    unittest.main() 