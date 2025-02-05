"use client"

import { CryptoDashboard } from "@/components/crypto-dashboard"
import { StarsBackground } from "@/components/stars-background"
import { useWalletKit } from "@mysten/wallet-kit"
import { ConnectButton } from "@mysten/wallet-kit"
import { useState, useEffect } from "react"
import { MessageSquare } from 'lucide-react'
import { AIPortfolioChat } from "@/components/ai-portfolio-chat"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import Image from "next/image"
import { TransactionSuccess } from "@/components/transaction-success"

export default function HubPage() {
  const { currentAccount } = useWalletKit()
  const [isLoaded, setIsLoaded] = useState(false)
  const [showTransactionSuccess, setShowTransactionSuccess] = useState(false)
  const [lastTransaction, setLastTransaction] = useState<{
    type: 'STAKE' | 'SWAP' | 'TRANSFER' | 'NFT_PURCHASE' | 'LIQUIDITY_ADD' | 'GOVERNANCE' | 'DEFAULT'
    fromAmount: number
    toAmount: number
    txHash: string
    additionalInfo?: {
      tokenSymbol?: string
      nftName?: string
      poolName?: string
      proposalId?: string
    }
  } | null>(null)

  const [portfolioData, setPortfolioData] = useState({
    suiPrice: null,
    totalPortfolioValue: 0,
    portfolioData: [],
    treasuryUSDC: 0,
    treasurySUI: 0,
    updateHubInfo: () => { }
  })

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  if (!isLoaded) return <div>Loading...</div>

  if (!currentAccount) {
    return (
      <div className="flex h-screen bg-black text-white relative">
        <StarsBackground />
        <div className="flex flex-col items-center justify-center w-full relative z-10 space-y-6">
          <div className="text-center space-y-4">
            <h1 className="text-3xl font-bold">Welcome to Aegir Hub</h1>
            <p className="text-zinc-400">Connect your wallet to access the dashboard</p>
          </div>
          <div className="flex items-center gap-4">
            <ConnectButton />
          </div>
          <Link
            href="/"
            className="text-sm text-zinc-500 hover:text-zinc-400 transition-colors"
          >
            Return to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-black text-white relative">
      <StarsBackground />

      {/* Main Content */}
      <div className="flex-1 flex relative z-10">
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="h-14 border-b border-gray-800 flex items-center bg-black/30 backdrop-blur-sm">
            <div className="flex-1 flex items-center px-4">
              <Link href="/" className="hover:opacity-80 transition-opacity">
                <Image
                  src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/beautiful_flat-style_logo_desi-Mxrj2lGzGBxZB7jWTgQ6vXatSStLad.jpeg"
                  alt="Aegir Logo"
                  width={32}
                  height={32}
                  className="rounded-full"
                  style={{
                    filter: "drop-shadow(0 0 10px rgba(64, 224, 208, 0.5))",
                  }}
                />
              </Link>
              <h1 className="ml-6 text-lg font-semibold">Aegir Hub</h1>
            </div>
          </header>

          {/* Dashboard Content */}
          <div className="flex-1 overflow-auto">
            <CryptoDashboard />
          </div>
        </div>

        {/* Right Panel - AI Chat */}
        <div className="w-[400px] bg-black/30 backdrop-blur-sm">
          <div className="h-14 border-b border-gray-800 flex items-center justify-end px-4">
            <ConnectButton />
          </div>
          <div className="h-[calc(100vh-3.5rem)]">
            <AIPortfolioChat data={portfolioData} />
          </div>
        </div>
      </div>

      {/* Transaction Success Notification */}
      {showTransactionSuccess && lastTransaction && (
        <TransactionSuccess
          type={lastTransaction.type}
          fromAmount={lastTransaction.fromAmount}
          toAmount={lastTransaction.toAmount}
          txHash={lastTransaction.txHash}
          additionalInfo={lastTransaction.additionalInfo}
          onClose={() => setShowTransactionSuccess(false)}
          position="bottom-left"
        />
      )}
    </div>
  )
}

