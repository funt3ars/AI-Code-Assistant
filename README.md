# Devin Integration

A Python package that provides Devin-like AI capabilities for your projects. This package includes tools for web scraping, search functionality, and AI model integration.

## Features

- Multi-agent system with Planner and Executor roles
- Web scraping capabilities
- Search engine integration
- Screenshot verification workflow
- LLM integration with multiple providers

## Installation

You can install the package using pip:

```bash
pip install devin-integration
```

For development installation with additional tools:

```bash
pip install devin-integration[dev]
```

## Usage

```python
from devin_integration import Planner, Executor

# Initialize the multi-agent system
planner = Planner()
executor = Executor()

# Use the planner to analyze a task
task_analysis = planner.analyze_task("Implement a new feature")

# Let the executor implement the solution
result = executor.execute(task_analysis)
```

## Development

1. Clone the repository:

```bash
git clone https://github.com/funt3ars/devin_integration.git
cd devin_integration
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

3. Run tests:

```bash
pytest tests/
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
