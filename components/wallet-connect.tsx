'use client';

import { ConnectButton } from '@mysten/wallet-kit';
import { useWalletKit } from '@mysten/wallet-kit';
import { useEffect } from 'react';
import { AftermathTools } from '../lib/agents/aftermath-tools';

export function WalletConnect() {
    const { currentAccount, isConnected } = useWalletKit();

    useEffect(() => {
        const initializeAftermath = async () => {
            if (isConnected && currentAccount) {
                const aftermathTools = AftermathTools.getInstance();

                // Set wallet configuration
                aftermathTools.setWalletConfig({
                    walletAddress: currentAccount.address,
                    provider: currentAccount
                });

                try {
                    await aftermathTools.initialize();
                    console.log('Aftermath initialized with wallet:', currentAccount.address);
                } catch (error) {
                    console.error('Failed to initialize Aftermath:', error);
                }
            }
        };

        initializeAftermath();
    }, [isConnected, currentAccount]);

    return (
        <div className="flex items-center gap-4">
            <ConnectButton connectText="Connect Wallet" />
            {isConnected && currentAccount && (
                <div className="text-sm">
                    Connected: {currentAccount.address.slice(0, 6)}...
                    {currentAccount.address.slice(-4)}
                </div>
            )}
        </div>
    );
} 