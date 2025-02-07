export class AtomaAgent {
    private bearerToken: string;
    private baseUrl: string;

    constructor(bearerToken: string) {
        this.bearerToken = bearerToken;
        // You might need to adjust this URL based on Atoma's actual API endpoint
        this.baseUrl = 'https://api.atoma.network/api';
    }

    async query({ prompt, context = {} }: { prompt: string; context?: any }) {
        try {
            console.log('Making request to Atoma API with:', {
                prompt,
                contextKeys: Object.keys(context)
            });

            const response = await fetch(`${this.baseUrl}/sui/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.bearerToken}`,
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    prompt,
                    context
                })
            });

            const responseText = await response.text();
            console.log('Raw API Response:', responseText);

            if (!response.ok) {
                throw new Error(`API request failed: ${response.status} ${response.statusText}\nResponse: ${responseText}`);
            }

            try {
                const data = JSON.parse(responseText);
                return data;
            } catch (parseError) {
                console.error('Failed to parse JSON response:', parseError);
                return {
                    reasoning: 'Error parsing response',
                    response: 'The API response could not be processed.',
                    status: 'failure',
                    errors: [parseError.message]
                };
            }
        } catch (error) {
            console.error('Atoma API Error:', {
                error,
                token: this.bearerToken ? 'Token present' : 'No token',
                url: this.baseUrl
            });

            // Return a formatted error response instead of throwing
            return {
                reasoning: 'API request failed',
                response: error.message || 'An unknown error occurred',
                status: 'failure',
                errors: [error.message]
            };
        }
    }
} 