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
