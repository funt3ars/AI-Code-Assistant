import { SuiClient } from '@mysten/sui.js/client';
import { TransactionBlock } from '@mysten/sui.js/transactions';

export class TransactionHelper {
    private client: SuiClient;

    constructor() {
        this.client = new SuiClient({
            url: 'https://fullnode.mainnet.sui.io'
        });
    }

    /**
     * Creates a transaction for transferring SUI
     */
    async buildTransferTx(amount: bigint, recipient: string): Promise<TransactionBlock> {
        const tx = new TransactionBlock();
        const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(amount)]);
        tx.transferObjects([coin], tx.pure.address(recipient));
        return tx;
    }

    /**
     * Estimates gas for a transaction
     */
    async estimateGas(txBytes: string): Promise<string> {
        try {
            const dryRunResult = await this.client.dryRunTransactionBlock({
                transactionBlock: txBytes
            });
            return dryRunResult.effects.gasUsed.computationCost;
        } catch (error: unknown) {
            throw new Error(`Failed to estimate gas: ${error instanceof Error ? error.message : String(error)
                }`);
        }
    }
} 