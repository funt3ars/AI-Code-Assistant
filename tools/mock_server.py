import asyncio
import logging
from aiohttp import web
from pathlib import Path
import json
import random
from typing import Dict, Any

logger = logging.getLogger('mock_server')

class MockServer:
    def __init__(self, port: int = 8080):
        """
        Initialize the mock server.
        
        Args:
            port: Port to run the server on
        """
        self.port = port
        self.app = web.Application()
        self.runner = None
        self.site = None
        
        # Register routes
        self.app.router.add_get('/', self.handle_root)
        self.app.router.add_get('/page{num}', self.handle_path)
        self.app.router.add_get('/error/{code}', self.handle_error)
        self.app.router.add_get('/slow/{delay}', self.handle_slow)
        self.app.router.add_get('/malformed', self.handle_malformed)
        
    async def handle_root(self, request: web.Request) -> web.Response:
        """Handle root path request."""
        return web.Response(
            text=self._generate_html('Home Page', 'Welcome to the mock server'),
            content_type='text/html'
        )
        
    async def handle_path(self, request: web.Request) -> web.Response:
        """Handle path-based requests."""
        num = request.match_info['num']
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page {num}</title>
            <meta name="description" content="Mock page description">
        </head>
        <body>
            <h1>Page {num}</h1>
            <p>Page: {num}</p>
            <img src="/images/test.jpg" alt="Test Image">
            <a href="/page1">Link 1</a>
            <a href="/page2">Link 2</a>
            <a href="https://example.com">External Link</a>
        </body>
        </html>
        """
        return web.Response(text=content, content_type='text/html')
        
    async def handle_error(self, request: web.Request) -> web.Response:
        """Handle error code requests."""
        code = int(request.match_info['code'])
        return web.Response(
            text=json.dumps({'error': f'Mock error {code}'}),
            status=code,
            content_type='application/json'
        )
        
    async def handle_slow(self, request: web.Request) -> web.Response:
        """Handle slow response requests."""
        delay = float(request.match_info['delay'])
        await asyncio.sleep(delay)
        return web.Response(
            text=self._generate_html('Slow Page', f'Response delayed by {delay}s'),
            content_type='text/html'
        )
        
    async def handle_malformed(self, request: web.Request) -> web.Response:
        """Handle malformed HTML requests."""
        return web.Response(
            text='<html><body><p>Malformed HTML</body>',  # Missing closing tags
            content_type='text/html'
        )
        
    def _generate_html(self, title: str, content: str) -> str:
        """Generate HTML content."""
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <meta name="description" content="Mock page description">
        </head>
        <body>
            <h1>{title}</h1>
            <p>{content}</p>
            <img src="/images/test.jpg" alt="Test Image">
            <a href="/page1">Link 1</a>
            <a href="/page2">Link 2</a>
            <a href="https://example.com">External Link</a>
        </body>
        </html>
        '''
        
    async def start(self):
        """Start the mock server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, 'localhost', self.port)
        await self.site.start()
        logger.info(f"Mock server running on http://localhost:{self.port}")
        
    async def stop(self):
        """Stop the mock server."""
        await self.app.shutdown()
        await self.app.cleanup()

async def main():
    """Run the mock server."""
    server = MockServer()
    try:
        await server.start()
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        logger.info("Shutting down mock server")
        await server.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 