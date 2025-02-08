import { AtomaAgent } from './atoma-agent';
import type { AgentResponse } from './types';
import { validateAgentResponse } from './validation';

export class SuiAgent {
    private static instance: SuiAgent;
    private atomaAgent: AtomaAgent;

    private constructor(bearerToken: string) {
        this.atomaAgent = new AtomaAgent(bearerToken);
    }

    public static getInstance(bearerToken?: string): SuiAgent {
        if (!SuiAgent.instance) {
            if (!bearerToken) {
                throw new Error('Bearer token is required for first initialization');
            }
            SuiAgent.instance = new SuiAgent(bearerToken);
        }
        return SuiAgent.instance;
    }

    async processQuery(prompt: string, context?: any): Promise<AgentResponse> {
        try {
            // Use Atoma's agent to process the query
            const result = await this.atomaAgent.query({ prompt, context });

            const response: AgentResponse = {
                reasoning: result.reasoning || 'Processing query',
                response: result.response || 'No response available',
                status: (result.status === 'success' || result.status === 'failure') ? result.status : 'failure',
                query: prompt,
                errors: result.errors || []
            };

            validateAgentResponse(response);
            return response;
        } catch (error) {
            console.error('Atoma Agent Error:', error);
            const errorResponse: AgentResponse = {
                reasoning: 'Error processing query',
                response: (error as Error).message,
                status: 'failure',
                query: prompt,
                errors: [(error as Error).message]
            };

            validateAgentResponse(errorResponse);
            return errorResponse;
        }
    }

    async SuperVisorAgent(query: string): Promise<AgentResponse> {
        try {
            // Use Atoma's agent directly
            const result = await this.atomaAgent.query({
                prompt: query
            });

            return {
                reasoning: result.reasoning || 'Query processed',
                response: result.response,
                status: 'success',
                query: query,
                errors: []
            };
        } catch (error) {
            return {
                reasoning: 'Error processing query',
                response: (error as Error).message,
                status: 'failure',
                query: query,
                errors: [(error as Error).message]
            };
        }
    }
}

export default SuiAgent; 