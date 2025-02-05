import OpenAI from 'openai'

const openai = new OpenAI({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY
})

export class PortfolioAgent {
    static async processQuery(query: string, context: any) {
        try {
            const completion = await openai.chat.completions.create({
                model: "gpt-4",
                messages: [
                    {
                        role: "system",
                        content: `You are an AI assistant for a Sui blockchain portfolio. 
            Current portfolio context:
            - SUI Price: $${context.suiPrice}
            - Portfolio Value: $${context.totalValue}
            - Treasury: ${context.treasury.sui} SUI, $${context.treasury.usdc} USDC`
                    },
                    {
                        role: "user",
                        content: query
                    }
                ]
            })

            return {
                response: completion.choices[0].message.content,
                updates: null // Add portfolio update logic if needed
            }
        } catch (error) {
            console.error('Portfolio Agent Error:', error)
            throw error
        }
    }
} 