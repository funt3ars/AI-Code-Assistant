import { INTENT_PROMPT } from './prompts/intent-agent';
import { FINAL_ANSWER_PROMPT } from './prompts/final-answer';
import { TransactionHelper } from '../sui/transaction-helper';
import { PriceService } from '../services/price-service';
import type { AgentResponse } from './types';
import { validateAgentResponse } from './validation';

interface IntentResponse {
    success: boolean;
    selected_tool: string | null;
    response: string | null;
    needs_additional_info: boolean;
    additional_info_required: string[] | null;
    tool_arguments: any[] | null;
}

export class AtomaAgent {
    private bearerToken: string;
    private baseUrl: string;
    private model: string;
    private transactionHelper: TransactionHelper;
    private priceService: PriceService;

    constructor(bearerToken: string) {
        this.bearerToken = bearerToken;
        this.baseUrl = 'https://api.atoma.network/v1';
        this.model = process.env.ATOMA_CHAT_COMPLETIONS_MODEL || 'meta-llama/Llama-3.3-70B-Instruct';
        this.transactionHelper = new TransactionHelper();
        this.priceService = new PriceService();

        // Log initialization
        console.log('AtomaAgent initialized:', {
            hasToken: !!this.bearerToken,
            baseUrl: this.baseUrl,
            model: this.model
        });
    }

    private async callAtoma(prompt: string, systemPrompt: string): Promise<string> {
        const requestData = {
            messages: [
                {
                    role: "system",
                    content: systemPrompt
                },
                {
                    role: "user",
                    content: prompt
                }
            ],
            model: this.model
        };

        const response = await fetch(`${this.baseUrl}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.bearerToken}`,
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data.choices?.[0]?.message?.content || '';
    }

    private async analyzeIntent(prompt: string): Promise<IntentResponse> {
        try {
            // Handle greetings
            if (prompt.toLowerCase().match(/^(hi|hello|hey|greetings)/)) {
                return {
                    success: true,
                    selected_tool: null,
                    response: "Hello! I'm your Sui blockchain assistant. I can help you with checking prices, making transfers, or getting blockchain information. What would you like to know?",
                    needs_additional_info: false,
                    additional_info_required: null,
                    tool_arguments: null
                };
            }

            // Handle off-topic queries
            const offTopicPatterns = /weather|time|date|temperature|forecast|clock/i;
            if (offTopicPatterns.test(prompt)) {
                return {
                    success: true,
                    selected_tool: null,
                    response: "I'm a Sui blockchain assistant. I can help you with Sui-related tasks like checking prices, making transfers, or getting blockchain information. What would you like to know about Sui?",
                    needs_additional_info: false,
                    additional_info_required: null,
                    tool_arguments: null
                };
            }

            const response = await this.callAtoma(prompt, INTENT_PROMPT);
            console.log('Raw AI response:', response);

            // Parse the response
            try {
                const parsed = JSON.parse(response);
                const intentResponse = Array.isArray(parsed) ? parsed[0] : parsed;

                // Validate the response structure
                if (!intentResponse || typeof intentResponse !== 'object') {
                    throw new Error('Invalid response structure');
                }

                // Ensure all required fields exist
                const defaultResponse: IntentResponse = {
                    success: true,
                    selected_tool: null,
                    response: null,
                    needs_additional_info: false,
                    additional_info_required: null,
                    tool_arguments: null
                };

                return { ...defaultResponse, ...intentResponse };
            } catch (error) {
                console.error('Parse error:', error);
                return {
                    success: true,
                    selected_tool: null,
                    response: "I'm here to help with Sui blockchain operations. Would you like to check prices, make transfers, or get blockchain information?",
                    needs_additional_info: false,
                    additional_info_required: null,
                    tool_arguments: null
                };
            }
        } catch (error) {
            console.error('Intent analysis error:', error);
            return {
                success: true,
                selected_tool: null,
                response: "I'm here to help with Sui blockchain! What would you like to know?",
                needs_additional_info: false,
                additional_info_required: null,
                tool_arguments: null
            };
        }
    }

    private async validateTransaction(amount: bigint, recipient: string): Promise<void> {
        // Validate recipient address
        if (!recipient.startsWith('0x') || recipient.length !== 66) {
            throw new Error('Invalid recipient address format');
        }

        // Validate amount
        if (amount <= BigInt(0)) {
            throw new Error('Amount must be greater than 0');
        }

        // Basic validation only
        return Promise.resolve();
    }

    private async executeTool(toolName: string, args: any[]): Promise<string> {
        switch (toolName) {
            case 'balance':
                if (!args[0]) {
                    throw new Error('Wallet address is required');
                }
                const balance = await this.transactionHelper.getBalance(args[0]);
                return `Your SUI balance is ${balance} SUI`;

            case 'transfer':
                if (!args[0] || !args[1]) {
                    throw new Error('Amount and recipient address are required');
                }
                const amount = BigInt(args[0]);
                const recipient = args[1];

                await this.validateTransaction(amount, recipient);
                const tx = await this.transactionHelper.buildTransferTx(amount, recipient);
                return JSON.stringify({
                    transaction: tx,
                    action: 'transfer',
                    context: `Transfer of ${amount} MIST to ${recipient.substring(0, 6)}...`
                });

            case 'price':
                if (!args[0]) {
                    throw new Error('Token symbol is required for price check');
                }
                const price = await this.priceService.getTokenPrice(args[0]);
                return `The price of ${args[0]} is $${price}`;

            default:
                throw new Error(`Unknown tool: ${toolName}`);
        }
    }

    async query({ prompt, context = {} }: { prompt: string; context?: any }): Promise<AgentResponse> {
        try {
            const intentResponse = await this.analyzeIntent(prompt);

            // Handle direct responses (like greetings) immediately
            if (intentResponse.success && intentResponse.response && !intentResponse.selected_tool) {
                return {
                    reasoning: 'Direct response',
                    response: intentResponse.response,
                    status: 'success',
                    query: prompt,
                    errors: []
                };
            }

            // Process based on intent
            let result: string;
            if (intentResponse.success && !intentResponse.needs_additional_info) {
                result = intentResponse.response || 'No direct response available';
            } else if (intentResponse.selected_tool && intentResponse.tool_arguments) {
                result = await this.executeTool(
                    intentResponse.selected_tool,
                    intentResponse.tool_arguments
                );
            } else {
                return {
                    reasoning: 'Additional information required',
                    response: `I need more information: ${intentResponse.additional_info_required?.join(', ')}`,
                    status: 'failure',
                    query: prompt,
                    errors: ['Insufficient information']
                };
            }

            // Format final response
            const finalResponse = await this.callAtoma(
                `Query: ${prompt}\nResult: ${result}`,
                FINAL_ANSWER_PROMPT
            );

            try {
                const [formattedResponse] = JSON.parse(finalResponse);
                return formattedResponse;
            } catch (parseError) {
                // Fallback if parsing fails
                return {
                    reasoning: 'Direct response',
                    response: result,
                    status: 'success',
                    query: prompt,
                    errors: []
                };
            }
        } catch (error: unknown) {
            console.error('Atoma API Error:', error);
            return {
                reasoning: 'API request failed',
                response: `Error: ${error instanceof Error ? error.message : String(error)}`,
                status: 'failure',
                query: prompt,
                errors: [error instanceof Error ? error.message : String(error)]
            };
        }
    }

    private breakIntoMessages(text: string): string[] {
        const MAX_LENGTH = 200;
        const parts: string[] = [];

        while (text.length > 0) {
            if (text.length <= MAX_LENGTH) {
                parts.push(text);
                break;
            }

            let cutoff = text.lastIndexOf(' ', MAX_LENGTH);
            if (cutoff === -1) cutoff = MAX_LENGTH;

            parts.push(text.substring(0, cutoff));
            text = text.substring(cutoff + 1);
        }

        return parts;
    }
} 