import { TransactionBlock } from '@mysten/sui.js/transactions';

/**
 * Response structure for AI agent interactions
 */
export interface AgentResponse {
    /** Explanation of the agent's thought process */
    reasoning: string;
    /** The actual response content */
    response: string;
    /** Operation status */
    status: 'success' | 'failure';
    /** The original query that was processed */
    query: string;
    /** Array of error messages if any occurred */
    errors: string[];
    /** Optional transaction block for blockchain operations */
    transaction?: TransactionBlock;
    /** Type of action being performed */
    action?: string;
    /** Whether this operation requires wallet interaction */
    requiresWallet?: boolean;
    /** Whether this operation is a continuation of a previous one */
    continuation?: boolean;
}

export interface ToolDefinition {
    name: string;
    description: string;
    parameters: {
        name: string;
        type: string;
        description: string;
        required: boolean;
    }[];
    process: Function;
} 