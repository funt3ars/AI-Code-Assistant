# Devin-like AI Assistant Integration

This document explains how to use the integrated Devin-like AI capabilities in your projects.

## Setup

1. Run the setup script to install dependencies and configure the environment:

```bash
./setup-devin.sh
```

2. No external API keys are required as this integration now uses CursorAI's built-in capabilities.

## Features

This integration provides several advanced AI capabilities to enhance your development workflow:

### 1. Multi-Agent System

- **Planner**: High-level analysis, task breakdown, and strategic planning
- **Executor**: Implements specific tasks and handles details

The multi-agent system leverages CursorAI's built-in capabilities rather than external APIs, making it more seamless to use.

### 2. Extended Toolset

- **Web Scraping**: For gathering data and documentation

  ```bash
  source devin-venv/bin/activate
  python tools/web_scrape.py https://example.com
  ```

- **Search Engine**: Find relevant information
  ```bash
  source devin-venv/bin/activate
  python tools/search_ddg.py "your search query"
  ```

### 3. Self-Evolution

The system learns from your corrections and feedback, improving over time by updating the "Lessons" section in the `.cursorrules` file.

## Usage with Cursor IDE

1. Make sure Cursor is installed and you've opened your project in it
2. The `.cursorrules` file will be automatically loaded by Cursor
3. Use the AI assistant as normal, but now it has enhanced capabilities
4. For complex tasks, the system will coordinate between Planner and Executor roles automatically

## Workflow Example

1. Ask the AI assistant to help implement a new feature
2. The Planner will analyze and break down the task
3. The Executor will implement the solution
4. The system continuously updates the `.cursorrules` file to track progress

## Troubleshooting

- If the AI assistant doesn't seem to use the enhanced capabilities, restart Cursor
- If you see Python errors, make sure all dependencies are installed with `./setup-devin.sh`

