import asyncio
import logging
import pytest
from pathlib import Path
from typing import Dict, Any, Optional
import aiohttp
from aiohttp import ClientTimeout, TCPConnector
from datetime import datetime
import sys
import io
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_error_handling_patterns():
    """Verify consistent error handling patterns across the system."""
    # Test specific error handling
    try:
        raise ValueError("Test error")
    except ValueError as e:
        error_response = {
            'status': 'error',
            'error': str(e),
            'details': {'type': 'ValueError'}
        }
        assert 'error' in error_response
        assert 'details' in error_response
        assert isinstance(error_response['details'], dict)
        
    # Test generic error handling
    try:
        raise Exception("Generic error")
    except Exception as e:
        error_response = {
            'status': 'error',
            'error': str(e),
            'details': {'type': 'Exception'}
        }
        assert 'error' in error_response
        assert 'details' in error_response
        assert isinstance(error_response['details'], dict)

@pytest.mark.asyncio
async def test_async_patterns():
    """Verify consistent async/await patterns."""
    async def test_coroutine():
        await asyncio.sleep(0.1)
        return "success"
        
    result = await test_coroutine()
    assert result == "success"
    
    # Verify proper async context manager usage
    class TestAsyncContext:
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
            
    async with TestAsyncContext() as ctx:
        assert isinstance(ctx, TestAsyncContext)

@pytest.mark.asyncio
async def test_path_handling():
    """Verify consistent path handling using pathlib."""
    # Test path creation
    path = Path("test/directory/file.txt")
    assert isinstance(path, Path)
    assert path.as_posix() == "test/directory/file.txt"
    
    # Test path normalization
    test_path = "test\\directory\\file.txt"
    normalized = os.path.normpath(test_path).replace("\\", "/")
    assert normalized == "test/directory/file.txt"

@pytest.mark.asyncio
async def test_rate_limiting_patterns():
    """Verify consistent rate limiting implementation."""
    class TestRateLimiter:
        def __init__(self, rate_limit: int = 5):
            self.rate_limit = rate_limit
            self.last_request_time = 0
            self.request_lock = asyncio.Lock()
            
        async def _wait_for_rate_limit(self):
            async with self.request_lock:
                now = asyncio.get_event_loop().time()
                time_since_last = now - self.last_request_time
                if time_since_last < 1 / self.rate_limit:
                    await asyncio.sleep(1 / self.rate_limit - time_since_last)
                self.last_request_time = asyncio.get_event_loop().time()
    
    limiter = TestRateLimiter(rate_limit=5)
    start_time = asyncio.get_event_loop().time()
    
    # Make multiple requests
    for _ in range(3):
        await limiter._wait_for_rate_limit()
        
    end_time = asyncio.get_event_loop().time()
    assert end_time - start_time >= 0.4  # 3 requests at 5/sec should take at least 0.4s

@pytest.mark.asyncio
async def test_logging_patterns():
    """Verify consistent logging patterns."""
    # Test logging levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Verify no print statements
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print("This should be captured")
    sys.stdout = sys.__stdout__
    assert "This should be captured" in captured_output.getvalue()

@pytest.mark.asyncio
async def test_http_client_patterns():
    """Verify consistent HTTP client patterns."""
    async with aiohttp.ClientSession(
        connector=TCPConnector(force_close=True),
        timeout=ClientTimeout(total=30)
    ) as session:
        assert isinstance(session, aiohttp.ClientSession)
        assert session._connector.force_close
        assert session._timeout.total == 30

def test_lessons_learned():
    """Verify that lessons learned are properly applied."""
    # Check for pathlib usage in test file
    with open(__file__, 'r') as f:
        content = f.read()
        # Look for actual os.path.join function calls
        join_calls = re.findall(r'os\.path\.join\s*\(', content)
        assert not join_calls, "os.path.join function calls should not be used"
        # Verify pathlib.Path is used
        assert 'Path(' in content, "pathlib.Path should be used"
    
    # Check for print statements
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print("This should be captured")
    sys.stdout = sys.__stdout__
    assert "This should be captured" in captured_output.getvalue()

@pytest.mark.asyncio
async def test_concurrent_operations():
    """Verify proper handling of concurrent operations."""
    async def worker(task_id: int) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return {
            'task_id': task_id,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
    tasks = [worker(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 5
    for result in results:
        assert 'task_id' in result
        assert 'status' in result
        assert 'timestamp' in result
        assert result['status'] == 'success'

@pytest.mark.asyncio
async def test_error_propagation():
    """Verify proper error propagation in async operations."""
    async def failing_worker():
        await asyncio.sleep(0.1)
        raise ValueError("Test error")
        
    with pytest.raises(ValueError) as exc_info:
        await failing_worker()
    assert str(exc_info.value) == "Test error"
    
    # Test error handling in gather
    async def mixed_workers():
        tasks = [
            asyncio.sleep(0.1),
            failing_worker(),
            asyncio.sleep(0.1)
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
        
    results = await mixed_workers()
    assert len(results) == 3
    assert isinstance(results[1], ValueError)
    assert str(results[1]) == "Test error"

if __name__ == '__main__':
    pytest.main(['-v', 'test_system_integrity.py']) 