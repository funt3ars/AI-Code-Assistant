"use client"

import { WalletKitProvider } from "@mysten/wallet-kit"
import { ReactNode } from "react"

export function WalletProvider({ children }: { children: ReactNode }) {
  return (
    <WalletKitProvider>
      {children}
    </WalletKitProvider>
  )
} 