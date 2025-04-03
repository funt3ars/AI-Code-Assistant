"""
Devin Integration Package

A reusable package for integrating Devin-like AI capabilities into Python projects.
"""

__version__ = "0.1.0"

from .core.planner import Planner
from .core.executor import Executor
from .tools.web_scraper import WebScraper
from .tools.search_engine import SearchEngine
from .config.settings import load_settings

__all__ = [
    'Planner',
    'Executor',
    'WebScraper',
    'SearchEngine',
    'load_settings'
] 