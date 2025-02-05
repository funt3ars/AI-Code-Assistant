"use client"

import { ConnectButton as WalletKitConnectButton } from "@mysten/wallet-kit"
import { Button } from "@/components/ui/button"
import { Github, Twitter } from "lucide-react"

export function ConnectButton() {
  return (
    <div className="flex items-center gap-4">
      {/* Social Links */}
      <div className="flex items-center gap-2">
        <a
          href="https://github.com/your-repo"
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-primary transition-colors"
        >
          <Github className="h-5 w-5" />
        </a>
        <a
          href="https://twitter.com/your-handle"
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-primary transition-colors"
        >
          <Twitter className="h-5 w-5" />
        </a>
      </div>

      {/* Connect Wallet Button */}
      <WalletKitConnectButton>
        {({ connected, connecting, connect, account }) => (
          <Button
            variant={connected ? "outline" : "default"}
            onClick={connect}
            disabled={connecting}
            className="min-w-[140px]"
          >
            {connecting ? (
              "Connecting..."
            ) : connected ? (
              <span className="truncate">
                {account?.address?.slice(0, 4)}...{account?.address?.slice(-4)}
              </span>
            ) : (
              "Connect Wallet"
            )}
          </Button>
        )}
      </WalletKitConnectButton>
    </div>
  )
} 