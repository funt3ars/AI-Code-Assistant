import { AtomaAgent } from './atoma-agent';
import type { AgentResponse } from '@elizaos/core';

export interface SuiAgentResponse extends AgentResponse {
    response: string;
    updates?: {
        portfolioValue?: number;
        transactions?: any[];
        positions?: any[];
        [key: string]: any;
    };
}

export class SuiAgent {
    private static instance: SuiAgent;
    private atomaAgent: AtomaAgent;
    private bearerToken: string;

    private constructor(bearerToken: string) {
        // Log the token being used (first 4 chars only for security)
        console.log('SuiAgent initializing with token prefix:', bearerToken.substring(0, 4));

        this.bearerToken = bearerToken;
        this.atomaAgent = new AtomaAgent(this.bearerToken);
    }

    public static getInstance(): SuiAgent {
        if (!SuiAgent.instance) {
            // Try both environment variables
            const token = process.env.NEXT_PUBLIC_ATOMASDK_BEARER_AUTH || process.env.ATOMASDK_BEARER_AUTH;
            if (!token) {
                throw new Error('ATOMASDK_BEARER_AUTH environment variable is not set');
            }
            SuiAgent.instance = new SuiAgent(token);
        }
        return SuiAgent.instance;
    }

    async processQuery(query: string, context: {
        suiPrice: number | null;
        totalValue: number;
        treasury: {
            usdc: number;
            sui: number;
        };
    }): Promise<SuiAgentResponse> {
        try {
            // Use Atoma's agent to process the query
            const result = await this.atomaAgent.query({
                prompt: query,
                context: context
            });

            return {
                reasoning: result.reasoning || 'Processing query',
                response: result.response || 'No response available',
                status: result.status || 'success',
                query: query,
                errors: result.errors || [],
                updates: {
                    portfolioValue: context.totalValue,
                }
            };
        } catch (error) {
            console.error('Atoma Agent Error:', error);
            throw error;
        }
    }

    async SuperVisorAgent(query: string): Promise<any> {
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