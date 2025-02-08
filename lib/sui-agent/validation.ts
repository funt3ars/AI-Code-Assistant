import { TransactionBlock } from '@mysten/sui.js/transactions';
import type { AgentResponse } from './types';

export function validateAgentResponse(response: AgentResponse): void {
    // Check required properties exist
    if (typeof response.reasoning !== 'string') throw new Error('reasoning must be a string');
    if (typeof response.response !== 'string') throw new Error('response must be a string');
    if (typeof response.query !== 'string') throw new Error('query must be a string');
    if (!Array.isArray(response.errors)) throw new Error('errors must be an array');
    if (response.status !== 'success' && response.status !== 'failure') {
        throw new Error('status must be either "success" or "failure"');
    }

    // Check optional properties if present
    if (response.transaction !== undefined && !(response.transaction instanceof TransactionBlock)) {
        throw new Error('transaction must be a TransactionBlock');
    }
    if (response.action !== undefined && typeof response.action !== 'string') {
        throw new Error('action must be a string');
    }
    if (response.requiresWallet !== undefined && typeof response.requiresWallet !== 'boolean') {
        throw new Error('requiresWallet must be a boolean');
    }
} 