# 🌟 Midas DeFi Assistant

An intelligent DeFi ecosystem for the Sui blockchain, powered by dual AI agents (Midas & Kassandra) and advanced portfolio management tools.

## 🤖 AI Agents

### Midas

- Portfolio analysis and DeFi strategy optimization
- Real-time market insights
- Transaction recommendations
- Portfolio rebalancing suggestions
- Yield farming optimization
- Risk assessment

### Kassandra

- Social sentiment analysis
- Web scraping for market intelligence
- Twitter sentiment analysis
- On-chain data analysis
- Transfer management through Eliza Sui plugin
- Market trend prediction

## 🤖 AI Development Tools

Midas includes Devin-like AI capabilities to enhance the development workflow. These tools provide:

- Multi-agent system with Planner and Executor roles powered by CursorAI
- Extended toolset for web scraping and search engine integration
- Self-evolution and learning from feedback

To use these AI capabilities:

1. Run `./setup-devin.sh` to set up the environment
2. See [DEVIN-INTEGRATION.md](DEVIN-INTEGRATION.md) for detailed usage instructions

No external API keys are required as this integration uses CursorAI's built-in capabilities.

## 🏗 Architecture

### Core Technologies

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Framer Motion** - Animations

### Blockchain Integration

- **Sui SDK** (@mysten/sui: ^1.21.2)
- **Wallet Connect** (@mysten/wallet-kit: ^0.8.6)
- **Aftermath SDK** (aftermath-ts-sdk: ^1.2.51)

### AI & Data

- **Atoma SDK** - AI agent framework
- **Atoma Agents** - Custom AI implementations
- **Tavily API** - Web scraping
- **Twitter API** - Social sentiment
- **TradingView** - Charts and technical analysis

## 📊 Features

### Portfolio Hub

- Real-time portfolio tracking
- Asset allocation visualization
- TradingView chart integration
- Transaction history
- Performance analytics
- DeFi position management

### Alpha Room

- AI-driven market insights
- Social sentiment dashboard
- Trend analysis
- Market opportunities
- Risk alerts

### DeFi Operations

- Token swaps
- Liquidity provision
- Yield farming
- Staking management
- Transaction optimization

## 🚀 Getting Started

1. Clone the repository

bash
git clone https://github.com/yourusername/midas.git
cd midas
bash
pnpm install
bash
cp .env.example .env.local
env
Atoma API Configuration
ATOMASDK_BEARER_AUTH=your_bearer_token
ATOMA_CHAT_COMPLETIONS_MODEL=meta-llama/Llama-3.3-70B-Instruct
Network Configuration
SUI_NETWORK=mainnet
API Keys
TAVILY_API_KEY=your_tavily_key
TWITTER_API_KEY=your_twitter_key
bash
pnpm dev
midas/
├── app/ # Next.js pages
├── components/
│ ├── ai-portfolio-chat/ # Midas AI chat interface
│ ├── alpha-room/ # Kassandra's insights
│ ├── trading-view/ # Chart components
│ └── wallet/ # Wallet integration
├── lib/
│ ├── sui-agent/ # Sui blockchain tools
│ ├── atoma-sdk-patch/ # Atoma SDK customization
│ └── utils/ # Helper functions
└── kassandra/ # Kassandra AI agent

## 🔧 Configuration

### Wallet Configuration

The project uses @mysten/wallet-kit for Sui wallet integration. Supported wallets:

- Sui Wallet
- Martian Wallet
- Ethos Wallet
- Suiet Wallet

### Trading View Integration

Custom TradingView charts with:

- Multiple timeframes
- Technical indicators
- Custom themes
- Real-time data

### Aftermath SDK Integration

- Liquidity pool management
- Swap operations
- Yield optimization
- Position management

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](docs/README.md)
- [Atoma Docs](https://docs.atoma.network)
- [Sui Docs](https://docs.sui.io)
- [Aftermath Docs](https://docs.aftermath.finance)

## 🐳 Docker Deployment

### Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

### Setup

1. Copy the example environment file

```bash
cp .env.example .env
```

2. Edit the `.env` file with your configuration:

```bash
# Add your environment variables
NEXT_PUBLIC_ATOMA_BEARER_TOKEN=your_token_here
# Add other required environment variables
```

### Building and Running with Docker Compose

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

### Building and Running with Docker

```bash
# Build the Docker image
docker build -t midas-app .

# Run the container
docker run -p 3000:3000 --env-file .env -d midas-app
```

### Production Deployment Considerations

- Use a reverse proxy like Nginx for SSL termination
- Consider using Docker Swarm or Kubernetes for orchestration
- Set up proper monitoring and logging
- Configure proper resource limits

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
