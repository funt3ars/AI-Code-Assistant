import { Tools } from './utils/tools';
import { AftermathTools } from './tools/aftermath-tools';

export class AtomaAgent {
    private bearerToken: string;
    private baseUrl: string;
    private model: string;
    private tools: Tools;

    constructor(bearerToken?: string) {
        this.bearerToken = 'GAULFgEkSYz8W03oMRUZtduAOC7byx';
        this.baseUrl = 'https://api.atoma.network/v1';
        this.model = 'meta-llama/Llama-3.3-70B-Instruct';
        this.tools = new Tools(this.bearerToken);

        // Register tools
        AftermathTools.registerTools(this.tools);

        // Debug log
        console.log('Debug - Token:', {
            token: this.bearerToken,
            length: this.bearerToken.length,
            hasSpaces: this.bearerToken.includes(' ')
        });
    }

    async query({ prompt, context = {} }: { prompt: string; context?: any }) {
        try {
            // First try tools
            const toolSelection = await this.tools.selectAppropriateTool(prompt);
            console.log('Tool Selection:', toolSelection);

            if (toolSelection.success && toolSelection.selected_tool) {
                console.log('Using tool:', toolSelection.selected_tool);
                const result = await this.tools.processQuery(
                    prompt,
                    toolSelection.selected_tool,
                    toolSelection.tool_arguments
                );

                return {
                    reasoning: `Using ${toolSelection.selected_tool}`,
                    response: result,
                    status: 'success',
                    query: prompt,
                    errors: []
                };
            }

            // If no tool matches, use the original Midas personality
            if (!prompt) {
                throw new Error('Prompt is required');
            }

            const requestData = {
                messages: [
                    {
                        role: "system",
                        content: "You are Midas Rex, an assistant specialized in DeFi for the Sui blockchain ecosystem. Your personality combines the wisdom of a seasoned DeFi expert with an approachable teaching style. You excel at simplifying complex DeFi concepts, analyzing portfolio strategies, and keeping users informed about the latest Sui network developments. While you can guide users through transfers, your true expertise shines when offering insights, optimizing portfolios, and navigating the DeFi landscape on Sui. You communicate with confidence and clarity, making DeFi accessible to users of all experience levels."
                    },
                    {
                        role: "user",
                        content: prompt
                    }
                ],
                model: this.model,
                temperature: 0.7,
                max_tokens: 1000
            };

            const response = await fetch(`${this.baseUrl}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.bearerToken.trim()}`,
                    'Accept': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(`API Error: ${responseData.error?.message || response.statusText}`);
            }

            return {
                reasoning: 'Midas Rex response',
                response: responseData.choices?.[0]?.message?.content || 'No response generated',
                status: 'success',
                query: prompt,
                errors: []
            };

        } catch (error: unknown) {
            console.error('Error in query:', error);
            return {
                reasoning: 'Error processing query',
                response: `Error: ${error instanceof Error ? error.message : String(error)}`,
                status: 'failure',
                query: prompt,
                errors: [error instanceof Error ? error.message : String(error)]
            };
        }
    }
} 