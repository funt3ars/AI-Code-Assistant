export class AtomaAgent {
    private bearerToken: string;
    private baseUrl: string;
    private model: string;

    constructor(bearerToken: string) {
        this.bearerToken = bearerToken;
        this.baseUrl = 'https://api.atoma.network/v1';
        this.model = process.env.ATOMA_CHAT_COMPLETIONS_MODEL || 'meta-llama/Llama-3.3-70B-Instruct';

        // Log initialization
        console.log('AtomaAgent initialized:', {
            hasToken: !!this.bearerToken,
            baseUrl: this.baseUrl,
            model: this.model
        });
    }

    async query({ prompt, context = {} }: { prompt: string; context?: any }) {
        try {
            // Validate inputs
            if (!prompt) {
                throw new Error('Prompt is required');
            }

            if (!this.bearerToken) {
                throw new Error('Bearer token is not set');
            }

            // Format the request according to the chat completions API
            const requestData = {
                messages: [
                    {
                        role: "system",
                        content: "You are a helpful AI assistant specializing in Sui blockchain operations and information."
                    },
                    {
                        role: "user",
                        content: prompt
                    }
                ],
                model: this.model,
                context: context // Additional context if needed
            };

            const url = `${this.baseUrl}/chat/completions`;

            // Log request details
            console.log('Preparing Atoma API request:', {
                url,
                method: 'POST',
                hasToken: !!this.bearerToken,
                tokenPrefix: this.bearerToken.substring(0, 4) + '...',
                model: this.model
            });

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.bearerToken}`,
                    'Accept': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            // Log response details
            console.log('Received API Response:', {
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries())
            });

            const responseText = await response.text();
            console.log('Response body:', responseText);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}\nBody: ${responseText}`);
            }

            const data = JSON.parse(responseText);

            // Format the response to match our expected structure
            return {
                reasoning: 'Chat completion successful',
                response: data.choices?.[0]?.message?.content || 'No response generated',
                status: 'success',
                query: prompt,
                errors: []
            };
        } catch (error) {
            console.error('Atoma API Error:', {
                message: error.message,
                stack: error.stack,
                name: error.name,
                hasToken: !!this.bearerToken,
                url: `${this.baseUrl}/chat/completions`
            });

            return {
                reasoning: 'API request failed',
                response: `Error: ${error.message}`,
                status: 'failure',
                errors: [error.message]
            };
        }
    }
} 