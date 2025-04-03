# Feature Development Guide

This guide outlines the process for developing new features while maintaining high quality standards and incorporating lessons learned.

## Development Process

1. **Planning Phase**

   - Define clear success criteria
   - Identify potential edge cases
   - Plan error handling strategy
   - Consider rate limiting requirements

2. **Test-First Development**

   - Write test cases before implementation
   - Include tests for:
     - Happy path scenarios
     - Error conditions
     - Edge cases
     - Rate limiting (if applicable)
   - Use mock servers for controlled testing
   - Follow established async test patterns

3. **Implementation**

   - Follow established patterns:
     - Error handling
     - Rate limiting
     - Async/await usage
     - Logging
   - Maintain 80%+ test coverage
   - Ensure 100% coverage for critical paths
   - Use proper path handling (pathlib.Path)
   - Normalize file paths with forward slashes

4. **Quality Assurance**
   - Run full test suite
   - Verify coverage requirements
   - Check for pattern compliance
   - Review documentation

## Testing Guidelines

### Async Testing

```python
@pytest.mark.asyncio
async def test_feature():
    # Use proper async fixtures
    # Handle timing-sensitive tests carefully
    # Use mock servers for controlled testing
```

### Error Handling

```python
try:
    # Implementation
except (SpecificError1, SpecificError2) as e:
    # Proper error handling
    logger.error(f"Error occurred: {str(e)}")
    return {
        'status': 'error',
        'error': str(e),
        'details': error_details
    }
```

### Rate Limiting

```python
async def _wait_for_rate_limit(self):
    async with self.request_lock:
        now = asyncio.get_event_loop().time()
        time_since_last = now - self.last_request_time
        if time_since_last < 1 / self.rate_limit:
            await asyncio.sleep(1 / self.rate_limit - time_since_last)
        self.last_request_time = asyncio.get_event_loop().time()
```

## Documentation Requirements

1. **Feature Documentation**

   - Clear description of functionality
   - Usage examples
   - Error handling details
   - Rate limiting considerations

2. **Test Documentation**

   - Test coverage report
   - Test scenarios covered
   - Any intentionally uncovered code

3. **Success Criteria**
   - Clear metrics for success
   - Performance requirements
   - Error rate thresholds

## Common Pitfalls to Avoid

1. **Async Issues**

   - Not using proper async fixtures
   - Missing await statements
   - Improper event loop handling

2. **Testing Issues**

   - Flaky timing-dependent tests
   - Incomplete error case coverage
   - Missing edge case tests

3. **Error Handling**

   - Generic error catching
   - Missing error details
   - Inconsistent error response format

4. **Rate Limiting**
   - Inconsistent timing
   - Missing proper locking
   - Not accounting for system variations

## Best Practices

1. **Code Organization**

   - Use consistent patterns
   - Follow established error handling
   - Implement proper logging
   - Use type hints

2. **Testing**

   - Write tests first
   - Use mock servers
   - Handle timing carefully
   - Maintain high coverage

3. **Error Handling**

   - Be specific in error catching
   - Include detailed error information
   - Use consistent error response format
   - Log errors properly

4. **Rate Limiting**
   - Use proper locking
   - Account for timing variations
   - Implement exponential backoff
   - Test with realistic scenarios
