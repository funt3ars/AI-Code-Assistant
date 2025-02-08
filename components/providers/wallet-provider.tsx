'use client'

import { WalletKitProvider } from '@mysten/wallet-kit'
import { type ReactNode } from 'react'

interface WalletProviderProps {
    children: ReactNode;
}

export function WalletProvider({ children }: WalletProviderProps) {
    return (
        <WalletKitProvider>
            {children}
        </WalletKitProvider>
    )
} 