"use client"

import { WalletKitProvider } from "@mysten/wallet-kit"
import { PropsWithChildren } from "react"

export function WalletProvider({ children }: PropsWithChildren) {
  return (
    <WalletKitProvider
      features={["sui:signAndExecuteTransaction"]}
    >
      {children}
    </WalletKitProvider>
  )
} 