import { Tools } from '../utils/tools';
import { Aftermath } from 'aftermath-ts-sdk';
import { NETWORK_CONFIG } from '@/lib/config/network';

export class AftermathTools {
    private static instance: AftermathTools;
    private sdk: Aftermath;
    private router: any; // Will type this properly
    private pools: any;  // Will type this properly

    private constructor() {
        this.sdk = new Aftermath('mainnet');
        this.router = this.sdk.Router();
        this.pools = this.sdk.Pools();
    }

    public static getInstance(): AftermathTools {
        if (!AftermathTools.instance) {
            AftermathTools.instance = new AftermathTools();
        }
        return AftermathTools.instance;
    }

    public static registerTools(tools: Tools) {
        const instance = AftermathTools.getInstance();

        // Balance Check Tool
        tools.registerTool(
            'get_wallet_balance',
            'Get wallet token balances',
            [{
                name: 'walletAddress',
                type: 'string',
                description: 'Wallet address to check',
                required: true
            }],
            instance.getWalletBalance.bind(instance)
        );

        // Transfer Preparation Tool
        tools.registerTool(
            'prepare_transfer',
            'Prepare a transfer transaction (unsigned)',
            [{
                name: 'recipient',
                type: 'string',
                description: 'Recipient address',
                required: true
            },
            {
                name: 'amount',
                type: 'string',
                description: 'Amount to transfer',
                required: true
            },
            {
                name: 'tokenType',
                type: 'string',
                description: 'Token type to transfer (e.g. SUI)',
                required: true
            }],
            instance.prepareTransfer.bind(instance)
        );

        // Gas Estimation Tool
        tools.registerTool(
            'estimate_gas',
            'Estimate gas for a transaction',
            [{
                name: 'txBytes',
                type: 'string',
                description: 'Transaction bytes to estimate',
                required: true
            }],
            instance.estimateGas.bind(instance)
        );
    }

    private async getWalletBalance(walletAddress: string): Promise<string> {
        const poolData = await this.pools.getPoolsForAddress(walletAddress);
        return JSON.stringify(poolData);
    }

    private async prepareTransfer(recipient: string, amount: string, tokenType: string): Promise<string> {
        const route = await this.router.getRoute({
            coinTypeIn: tokenType,
            coinTypeOut: recipient,
            amountIn: amount
        });
        return JSON.stringify(route);
    }

    private async estimateGas(txBytes: string): Promise<string> {
        const gasEstimate = await this.router.estimateGas(txBytes);
        return JSON.stringify(gasEstimate);
    }
} 