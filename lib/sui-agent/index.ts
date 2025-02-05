export class SuiAgent {
    private static instance: SuiAgent;
    private context: any;

    private constructor() {
        this.context = {};
    }

    public static getInstance(): SuiAgent {
        if (!SuiAgent.instance) {
            SuiAgent.instance = new SuiAgent();
        }
        return SuiAgent.instance;
    }

    async processQuery(query: string, portfolioContext: any) {
        try {
            // Store context for use in responses
            this.context = {
                ...portfolioContext,
                timestamp: new Date().toISOString()
            };

            // For now, return simulated responses based on keywords
            if (query.toLowerCase().includes('price')) {
                return {
                    response: `The current SUI price is $${portfolioContext.suiPrice}. Your portfolio value is $${portfolioContext.totalValue}.`,
                    updates: null
                };
            }

            if (query.toLowerCase().includes('treasury')) {
                return {
                    response: `Your treasury contains ${portfolioContext.treasury.sui} SUI and $${portfolioContext.treasury.usdc} USDC.`,
                    updates: null
                };
            }

            // Default response
            return {
                response: `I understand your query about "${query}". I'm analyzing your portfolio data to provide insights.`,
                updates: null
            };
        } catch (error) {
            console.error('Sui Agent Error:', error);
            throw error;
        }
    }
} 