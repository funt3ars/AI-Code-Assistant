# AI Code Assistant

A sophisticated Python-based AI coding assistant that provides Devin-like capabilities for software development projects. This system implements a multi-agent architecture to analyze, plan, and execute coding tasks efficiently.

## Overview

The AI Code Assistant is designed to enhance software development workflows through:
- Intelligent task analysis and breakdown
- Automated code execution and validation
- Project management and documentation
- Integration with various development tools and services

## Architecture

### Core Components

1. **Multi-Agent System**
   - **Planner**: Handles high-level analysis and strategic planning
   - **Executor**: Manages task execution and implementation details

2. **Directory Structure**
```
.
├── core/               # Core implementation
│   ├── executor.py    # Task execution logic
│   └── planner.py     # Planning and analysis logic
├── tools/             # Utility tools
├── tests/             # Test suite
├── config/            # Configuration files
└── devin_integration/ # Integration components
```

## Features

- **Task Analysis and Planning**
  - Task breakdown into manageable steps
  - Challenge identification
  - Success criteria definition
  - Progress tracking

- **Code Execution**
  - Command execution
  - File editing capabilities
  - Test running and validation
  - Error handling and feedback

- **Project Management**
  - Status tracking
  - Lesson recording
  - Documentation management

- **Integration Capabilities**
  - Web scraping support
  - Search engine integration
  - Screenshot verification
  - Multiple LLM provider support

## Installation

### Basic Installation
```bash
pip install devin-integration
```

### Development Installation
```bash
pip install devin-integration[dev]
```

## Usage

### Basic Usage
```python
from devin_integration import Planner, Executor

# Initialize components
planner = Planner(project_root="path/to/project")
executor = Executor(project_root="path/to/project")

# Analyze a task
task_analysis = planner.analyze_task("Implement a new feature")

# Execute the task
result = executor.execute_task(task_analysis)
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/funt3ars/devin_integration.git
cd devin_integration
```

2. Set up the development environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

3. Run tests:
```bash
pytest tests/
```

## Technical Details

### Dependencies
- Python 3.x
- See `devin-requirements.txt` for complete list

### Configuration
- Project configuration is stored in the `config/` directory
- Task history and lessons learned are stored in `.cursorrules`

### Error Handling
- Comprehensive error handling in both Planner and Executor
- Detailed logging for debugging and monitoring
- Graceful failure handling with informative error messages

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
