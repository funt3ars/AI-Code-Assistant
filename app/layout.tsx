import { StarsBackground } from "../components/stars-background"
import { ThemeProvider } from "../components/theme-provider"
import { WalletProvider } from "../components/wallet-provider"
import "./globals.css"
import type React from "react"

export const metadata = {
  title: "Aegir - Sui Search Engine",
  description: "Discover the power of Sui with our advanced search engine and portfolio management tools.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <WalletProvider>
          <ThemeProvider>
            <StarsBackground />
            {children}
          </ThemeProvider>
        </WalletProvider>
      </body>
    </html>
  )
}

