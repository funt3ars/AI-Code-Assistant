# Contributing to Devin Integration

Thank you for your interest in contributing to the Devin Integration package! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/devin_integration.git
   cd devin_integration
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests and checks:
   ```bash
   pytest
   black .
   isort .
   mypy .
   flake8
   ```
4. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a Pull Request

## Code Style

- Use Black for code formatting
- Use isort for import sorting
- Use type hints
- Follow PEP 8 guidelines
- Write docstrings for all public functions and classes

## Testing

- Write tests for all new features
- Ensure all tests pass
- Maintain or improve test coverage
- Use pytest for testing
- Use pytest-asyncio for async tests

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions and classes
- Update type hints if needed
- Document breaking changes

## Pull Request Process

1. Update the version number in setup.py
2. Update CHANGELOG.md with your changes
3. Ensure all tests pass
4. Request review from maintainers

## Release Process

1. Update version in setup.py
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. The CI/CD pipeline will automatically publish to PyPI

## Questions?

Feel free to open an issue if you have any questions about contributing!
