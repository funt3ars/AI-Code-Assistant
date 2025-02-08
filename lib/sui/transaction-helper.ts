import { TransactionBlock } from '@mysten/sui.js/transactions';
import { SuiClient } from '@mysten/sui.js/client';

interface ITransactionHelper {
    buildTransferTx(amount: bigint, recipient: string): Promise<TransactionBlock>;
    getBalance(address: string): Promise<string>;
    estimateGas(txBytes: string): Promise<string>;
}

export class TransactionHelper implements ITransactionHelper {
    private client: SuiClient;

    constructor() {
        this.client = new SuiClient({
            url: 'https://fullnode.mainnet.sui.io'
        });
    }

    /**
     * Creates a transaction for transferring SUI
     * Following Sui SDK documentation
     */
    async buildTransferTx(amount: bigint, recipient: string): Promise<TransactionBlock> {
        try {
            const tx = new TransactionBlock();

            // Split coins for the transfer
            const [coin] = tx.splitCoins(tx.gas, [
                tx.pure(amount)
            ]);

            // Transfer the split coin to the recipient
            tx.transferObjects([coin], tx.pure(recipient));

            // Set gas budget
            tx.setGasBudget(20000000);

            return tx;
        } catch (error) {
            console.error('Error building transfer tx:', error);
            throw error;
        }
    }

    /**
     * Gets SUI balance for a wallet address
     */
    async getBalance(address: string): Promise<string> {
        try {
            if (!address) {
                throw new Error('Wallet address is required');
            }

            const { totalBalance } = await this.client.getBalance({
                owner: address,
                coinType: '0x2::sui::SUI'
            });

            return totalBalance;
        } catch (error) {
            console.error('Error getting balance:', error);
            throw new Error('Failed to get balance');
        }
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
            throw new Error(`Failed to estimate gas: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
} 