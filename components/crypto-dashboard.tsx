"use client"

import { BarChart, Bar, XAxis, YAxis } from "recharts"
import { ResponsiveContainer, Tooltip } from "recharts"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { TabsContent, Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { PieChart, Pie, Cell } from "recharts"
import { AIPortfolioChat, type AIPortfolioChatProps } from "./ai-portfolio-chat"
import { ScrollArea } from "@/components/ui/scroll-area"
import { TradingViewChart } from "./trading-view-chart"
import { useState, useEffect } from "react"
import { AreaChart, Area } from "recharts"
import { useWalletKit } from "@mysten/wallet-kit"
import { SuiClient } from "@mysten/sui.js/client"
import { type StakeObject as SuiStakeObject, type DelegatedStake as SuiDelegatedStake } from "@mysten/sui.js/client"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { PlusCircle, MessageSquare, BarChart2, Sparkles, TrendingUp } from "lucide-react"
import { TransactionResult } from "@/components/transaction-success"
import { SentimentAnalysis } from "./sentiment-analysis"
import { motion, AnimatePresence } from "framer-motion"

interface HubUpdates {
  suiPrice?: number
  totalPortfolioValue?: number
  treasuryUSDC?: number
  treasurySUI?: number
}

const data = Array.from({ length: 30 }, (_, i) => ({
  name: `Day ${i + 1}`,
  total: Math.floor(1000000 + Math.random() * 500000),
}))

const portfolioData = [
  { name: "Staking", value: 400000, suiAmount: 109589.04, color: "#3B82F6" },     // Blue
  { name: "DeFi", value: 250000, suiAmount: 68493.15, color: "#10B981" },         // Emerald
  { name: "Liquidity", value: 180000, suiAmount: 49315.07, color: "#8B5CF6" },    // Purple
  { name: "Treasury", value: 150000, suiAmount: 41095.89, color: "#F59E0B" },     // Amber
  { name: "USDC", value: 120000, suiAmount: 32876.71, color: "#EC4899" },         // Pink
]

const totalPortfolioValueCalc = portfolioData.reduce((sum, item) => sum + item.value, 0)
const totalAllocatedSUI = portfolioData.reduce((sum, item) => sum + item.suiAmount, 0)

// Assuming SUI price of $3.65
const suiPrice = 3.65

// Calculate treasury values based on total portfolio
const treasuryPercentage = 0.2 // 20% of total portfolio in treasury
const totalPortfolioSUI = totalAllocatedSUI / (1 - treasuryPercentage) // Total including treasury
const initialTreasurySUI = totalPortfolioSUI * treasuryPercentage
const initialTreasuryValueUSD = initialTreasurySUI * suiPrice
const initialTreasuryUSDC = initialTreasuryValueUSD / 2
const initialTreasurySUIAmount = initialTreasurySUI / 2

const analyticsData = [
  { category: "Risk Score", value: 68, maxValue: 100 },
  { category: "Diversification", value: 82, maxValue: 100 },
  { category: "Performance", value: 75, maxValue: 100 },
  { category: "Market Alignment", value: 90, maxValue: 100 },
]

const aiActivityLogs = [
  {
    date: "2025-02-05",
    action: "Rebalanced SUI staking positions for 2,000 SUI profit. Reinvested in DeFi protocols.",
    fee: 0.5,
    txHash: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
  },
  {
    date: "2025-02-07",
    action: "Participated in SUI Governance vote on protocol upgrade.",
    fee: 0.3,
    txHash: "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
  },
  {
    date: "2025-02-10",
    action: "Optimized SUI liquidity pool positions for higher yields.",
    fee: 0.7,
    txHash: "0x112233445566778899aabbccddeeff112233445566778899aabbccddeeff",
  },
  {
    date: "2025-02-12",
    action: "Acquired trending SUI NFT. Cost: 350 SUI. Estimated value: 500 SUI.",
    fee: 1.2,
    txHash: "0xffeeddccbbaa99887766554433221100ffeeddccbbaa99887766554433221100",
  },
  {
    date: "2025-02-15",
    action: "Executed dollar-cost averaging strategy: Purchased 100 SUI at market rate.",
    fee: 0.1,
    txHash: "0x1111222233334444555566667777888899990000111122223333444455556666",
  },
]

// Add new interface for transaction types
interface TransactionDetails {
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
}

// First, add the ChartPie icon at the top
function ChartPieIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
      <path d="M22 12A10 10 0 0 0 12 2v10z" />
    </svg>
  )
}

export function CryptoDashboard() {
  const { currentAccount } = useWalletKit()
  const [portfolioData, setPortfolioData] = useState<Array<{
    name: string
    value: number
    suiAmount: number
    color: string
  }>>([
    { name: "Staking", value: 0, suiAmount: 0, color: "#3B82F6" },     // Blue
    { name: "NFTs", value: 0, suiAmount: 0, color: "#10B981" },         // Emerald
    { name: "DeFi Yield", value: 0, suiAmount: 0, color: "#8B5CF6" },   // Purple
    { name: "Liquidity Pools", value: 0, suiAmount: 0, color: "#F59E0B" }, // Amber
    { name: "Treasury", value: 0, suiAmount: 0, color: "#14B8A6" },    // Teal
    { name: "USDC", value: 0, suiAmount: 0, color: "#2563EB" },        // Blue
  ])
  const [suiPrice, setSuiPrice] = useState<number | null>(null)
  const [totalPortfolioValue, setTotalPortfolioValue] = useState<number>(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [treasuryUSDC, setTreasuryUSDC] = useState(0)
  const [treasurySUI, setTreasurySUI] = useState(0)
  const [connectedWallets, setConnectedWallets] = useState<Array<{
    address: string
    balance: number
  }>>([])

  const [analyticsData, setAnalyticsData] = useState([
    { category: "Risk Score", value: 0, maxValue: 100 },
    { category: "Diversification", value: 0, maxValue: 100 },
    { category: "Performance", value: 0, maxValue: 100 },
    { category: "Market Alignment", value: 0, maxValue: 100 },
  ])

  const [activityLogs, setActivityLogs] = useState<Array<{
    date: string
    action: string
    fee: number
    txHash: string
    aiGenerated?: boolean
  }>>([])

  const [selectedAsset, setSelectedAsset] = useState("SUIUSD")

  const [tradingPairs, setTradingPairs] = useState([
    { value: "SUIUSD", label: "SUI/USD", exchange: "BINANCE" },
    { value: "BTCUSD", label: "BTC/USD", exchange: "BINANCE" },
    { value: "ETHUSD", label: "ETH/USD", exchange: "BINANCE" },
    { value: "SOLUSD", label: "SOL/USD", exchange: "BINANCE" },
    { value: "AVAXUSD", label: "AVAX/USD", exchange: "BINANCE" },
  ])

  const [newPair, setNewPair] = useState({ symbol: "", exchange: "BINANCE" })
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  const [showTransactionSuccess, setShowTransactionSuccess] = useState(false)
  const [lastTransaction, setLastTransaction] = useState<TransactionDetails | null>(null)

  const [lastSeenTxHash, setLastSeenTxHash] = useState<string | null>(null)

  // Add error state for transactions
  const [transactionError, setTransactionError] = useState<string | null>(null)

  const updateHubInfo = (updates: HubUpdates) => {
    if (updates.suiPrice) setSuiPrice(updates.suiPrice)
    if (updates.totalPortfolioValue) setTotalPortfolioValue(updates.totalPortfolioValue)
    if (updates.treasuryUSDC) setTreasuryUSDC(updates.treasuryUSDC)
    if (updates.treasurySUI) setTreasurySUI(updates.treasurySUI)
    // Add more update logic for other state variables as needed
  }

  const calculateAnalytics = (portfolio: typeof portfolioData) => {
    // Risk Score: Based on portfolio diversification and asset types
    const riskScore = Math.min(
      Math.floor(
        (portfolio.length / 5) * 100 + // Number of different asset types
        (portfolio.reduce((sum, item) => sum + item.value, 0) > 0 ? 30 : 0) // Has value
      ),
      100
    )

    // Diversification: Based on how evenly distributed the portfolio is
    const totalValue = portfolio.reduce((sum, item) => sum + item.value, 0)
    const diversification = Math.min(
      Math.floor(
        portfolio.length * 20 + // Number of asset types
        (portfolio.every(item => item.value / totalValue < 0.5) ? 30 : 0) // No single asset > 50%
      ),
      100
    )

    // Performance: Could be calculated based on historical data
    const performance = 75 // Placeholder for now, will be calculated with historical data

    // Market Alignment: Based on having popular assets
    const marketAlignment = Math.min(
      Math.floor(
        (portfolio.some(item => item.name === "Staking") ? 30 : 0) +
        (portfolio.some(item => item.name === "NFTs") ? 30 : 0) +
        (portfolio.some(item => item.name === "Treasury") ? 40 : 0)
      ),
      100
    )

    return [
      { category: "Risk Score", value: riskScore, maxValue: 100 },
      { category: "Diversification", value: diversification, maxValue: 100 },
      { category: "Performance", value: performance, maxValue: 100 },
      { category: "Market Alignment", value: marketAlignment, maxValue: 100 },
    ]
  }

  useEffect(() => {
    const loadPortfolioData = async () => {
      try {
        setIsLoading(true)
        console.log('Loading portfolio data...')

        if (!currentAccount?.address) {
          console.log('Waiting for wallet connection...')
          setIsLoading(false)
          return
        }

        const client = new SuiClient({
          url: "https://fullnode.mainnet.sui.io:443"
        })

        // Fetch main wallet balance
        const balance = await client.getBalance({
          owner: currentAccount.address,
          coinType: "0x2::sui::SUI"
        })

        // Fetch USDC balance
        const usdcBalance = await client.getBalance({
          owner: currentAccount.address,
          coinType: "0x5d4b302506645c37ff133b98c4b50a5ae14841659738d6d733d59d0d217a93bf::coin::COIN"
        })

        // Convert balances
        const suiBalance = Number(balance.totalBalance) / 1e9
        const usdcAmount = Number(usdcBalance.totalBalance) / 1e6

        // Update portfolio data with real values
        setPortfolioData(prev => prev.filter(item => {
          // Only keep USDC if there's a balance
          if (item.name === "USDC") {
            return usdcAmount > 0
          }
          return true
        }).map(item => {
          if (item.name === "Treasury") {
            return {
              ...item,
              value: suiBalance * (suiPrice || 0),
              suiAmount: suiBalance
            }
          }
          if (item.name === "USDC" && usdcAmount > 0) {
            return {
              ...item,
              value: usdcAmount,
              suiAmount: usdcAmount / (suiPrice || 1)
            }
          }
          return item
        }))

        // Update connected wallets with correct balance
        if (currentAccount) {
          setConnectedWallets([{
            address: currentAccount.address,
            balance: suiBalance
          }])
        }

        // Update total portfolio value
        setTotalPortfolioValue(suiBalance * (suiPrice || 0) + usdcAmount)

        // After setting portfolio data, calculate analytics
        const newAnalytics = calculateAnalytics(portfolioData)
        setAnalyticsData(newAnalytics)

        // Fetch recent transactions for activity logs
        const transactions = await client.queryTransactionBlocks({
          filter: {
            FromAddress: currentAccount.address
          },
          options: {
            showInput: true,
            showEffects: true,
            showEvents: true
          }
        })

        // Convert transactions to activity logs
        const newActivityLogs = transactions.data.map(tx => ({
          date: new Date(Number(tx.timestampMs)).toISOString().split('T')[0],
          action: `Transaction executed: ${tx.digest.slice(0, 8)}`,
          fee: Number(tx.effects?.gasUsed?.computationCost || 0) / 1e9, // Convert to SUI
          txHash: tx.digest,
          aiGenerated: false
        }))

        setActivityLogs(newActivityLogs)

        // Update treasury values (no automatic split)
        setTreasuryUSDC(0) // Only set if you have USDC
        setTreasurySUI(suiBalance)

        setIsLoading(false)
      } catch (err) {
        console.error('Error loading portfolio:', err)
        setError('Failed to load portfolio data. Please try again.')
        setIsLoading(false)
      }
    }

    loadPortfolioData()
  }, [currentAccount?.address, suiPrice])

  // Keep the SUI price fetching logic
  useEffect(() => {
    const fetchSuiPrice = async () => {
      try {
        const response = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=sui&vs_currencies=usd")
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        const data = await response.json()
        if (data?.sui?.usd) setSuiPrice(data.sui.usd)
      } catch (error) {
        console.error("Error fetching SUI price:", error)
      }
    }

    fetchSuiPrice()
    const interval = setInterval(fetchSuiPrice, 60000)
    return () => clearInterval(interval)
  }, [])

  // Function to determine transaction type from events
  const determineTransactionType = (tx: any) => {
    const events = tx.events || []
    const moveFunction = tx.transaction?.data?.sender_signed_data?.transactions?.[0]?.Move?.function || ''

    // Check for different transaction types based on events or move function
    if (events.some((e: any) => e.type.includes('::staking::'))) {
      return 'STAKE'
    }
    if (events.some((e: any) => e.type.includes('::dex::'))) {
      return 'SWAP'
    }
    if (moveFunction.includes('transfer')) {
      return 'TRANSFER'
    }
    if (events.some((e: any) => e.type.includes('::nft::'))) {
      return 'NFT_PURCHASE'
    }
    if (events.some((e: any) => e.type.includes('::liquidity::'))) {
      return 'LIQUIDITY_ADD'
    }
    if (events.some((e: any) => e.type.includes('::governance::'))) {
      return 'GOVERNANCE'
    }
    return 'DEFAULT'
  }

  // Update transaction checking logic
  useEffect(() => {
    const checkNewTransactions = async () => {
      if (!currentAccount?.address) return

      try {
        const client = new SuiClient({
          url: "https://fullnode.mainnet.sui.io:443"
        })

        const transactions = await client.queryTransactionBlocks({
          filter: { FromAddress: currentAccount.address },
          options: { showInput: true, showEffects: true, showEvents: true }
        })

        if (transactions.data[0] && transactions.data[0].digest !== lastSeenTxHash) {
          const latestTx = transactions.data[0]
          const amount = Number(latestTx.effects?.gasUsed?.computationCost || 0) / 1e9
          const txType = determineTransactionType(latestTx)

          // Check if transaction was successful
          const isSuccess = latestTx.effects?.status?.status === "success"

          const txDetails: TransactionDetails = {
            type: txType,
            fromAmount: amount,
            toAmount: amount * (suiPrice || 0),
            txHash: latestTx.digest,
            additionalInfo: {
              tokenSymbol: txType === 'SWAP' ? 'SUI' : undefined,
              nftName: txType === 'NFT_PURCHASE' ? 'SUI NFT' : undefined,
              poolName: txType === 'LIQUIDITY_ADD' ? 'SUI-USDC' : undefined,
              proposalId: txType === 'GOVERNANCE' ? '123' : undefined,
            }
          }

          setLastTransaction(txDetails)
          setShowTransactionSuccess(true)
          setLastSeenTxHash(latestTx.digest)

          if (!isSuccess) {
            setTransactionError("Transaction failed. Please check explorer for details.")
          }
        }
      } catch (error) {
        console.error("Error checking transactions:", error)
        setTransactionError("Failed to process transaction")
      }
    }

    const interval = setInterval(checkNewTransactions, 5000)
    return () => clearInterval(interval)
  }, [currentAccount?.address, lastSeenTxHash, showTransactionSuccess, suiPrice])

  useEffect(() => {
    if (showTransactionSuccess) {
      const timer = setTimeout(() => {
        setShowTransactionSuccess(false)
      }, 5000)

      return () => clearTimeout(timer)
    }
  }, [showTransactionSuccess])

  const handleAddPair = () => {
    if (newPair.symbol) {
      const formattedSymbol = newPair.symbol.toUpperCase().replace('/', '')
      const newTradingPair = {
        value: formattedSymbol,
        label: newPair.symbol.toUpperCase(),
        exchange: newPair.exchange.toUpperCase()
      }
      setTradingPairs([...tradingPairs, newTradingPair])
      setNewPair({ symbol: "", exchange: "BINANCE" })
      setIsDialogOpen(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-8 space-y-4">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="h-8 w-8 border-2 border-primary rounded-full border-t-transparent"
        />
        <p className="text-muted-foreground">Loading portfolio data...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-8">
        <p className="text-red-500">{error}</p>
        <Button
          onClick={() => window.location.reload()}
          className="mt-4"
        >
          Retry
        </Button>
      </div>
    )
  }

  return (
    <div className="w-full h-full relative overflow-hidden">
      <div>
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList className="w-full justify-start sticky top-0 z-10 bg-background/95 backdrop-blur">
            <div className="flex items-center gap-2">
              <ChartPieIcon className="h-5 w-5" />
              <TabsTrigger value="overview">Overview</TabsTrigger>
            </div>
            <TabsTrigger value="allocation">Allocation</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
            <TabsTrigger value="chart">Chart</TabsTrigger>
          </TabsList>

          <div className="h-[calc(100vh-8rem)] overflow-auto">
            <TabsContent value="overview" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Portfolio Value</CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="text-2xl font-semibold">
                          ${totalPortfolioValue.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                        </div>
                        <p className="text-sm text-muted-foreground">Total Portfolio Value</p>
                      </div>
                      <div className="h-24 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart data={data.slice(-30)} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                            <defs>
                              <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                              </linearGradient>
                            </defs>
                            <Area
                              type="monotone"
                              dataKey="total"
                              stroke="#8884d8"
                              fillOpacity={1}
                              fill="url(#colorTotal)"
                            />
                            <Tooltip
                              content={({ active, payload }) => {
                                if (active && payload && payload.length > 0 && payload[0]?.payload) {
                                  const data = payload[0].payload
                                  return (
                                    <div className="bg-background border rounded p-2 shadow-md">
                                      <p className="font-semibold">{data.name}</p>
                                      <p>${(data.value || 0).toLocaleString()}</p>
                                    </div>
                                  )
                                }
                                return null
                              }}
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-base font-medium">Top Positions</CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <rect x="18" y="3" width="4" height="18"></rect>
                      <rect x="10" y="8" width="4" height="13"></rect>
                      <rect x="2" y="13" width="4" height="8"></rect>
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold">1. Staking</span>
                        <span>${portfolioData[0].value.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-semibold">2. NFTs</span>
                        <span>${portfolioData[1].value.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-semibold">3. Meme Coins</span>
                        <span>${portfolioData[2].value.toLocaleString()}</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">SUI Treasury</CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    {isLoading ? (
                      <div>Loading...</div>
                    ) : error ? (
                      <div className="text-red-500">{error}</div>
                    ) : (
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold">Total Value</span>
                          <span className="text-green-500">
                            $
                            {(treasuryUSDC + treasurySUI * (suiPrice || 0)).toLocaleString(undefined, {
                              maximumFractionDigits: 2,
                            })}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="font-semibold">USDC</span>
                          <span>${treasuryUSDC.toLocaleString(undefined, { maximumFractionDigits: 2 })}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="font-semibold">SUI Amount</span>
                          <span>{treasurySUI.toLocaleString(undefined, { maximumFractionDigits: 2 })} SUI</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="font-semibold">SUI Price</span>
                          <span>${suiPrice?.toFixed(2)}</span>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Active SUI Wallets</CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4" />
                      <path d="M4 6v12c0 1.1.9 2 2 2h14v-4" />
                      <path d="M18 12a2 2 0 0 0-2 2c0 1.1.9 2 2 2h4v-4h-4z" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {connectedWallets.map((wallet, index) => (
                        <div key={index} className="flex justify-between items-center">
                          <span className="font-semibold">
                            {wallet.address.slice(0, 6)}...{wallet.address.slice(-4)}
                          </span>
                          <span>${(wallet.balance * (suiPrice || 0)).toLocaleString()}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="pt-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Market Sentiment</CardTitle>
                    <CardDescription>Real-time Sui ecosystem sentiment analysis</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <SentimentAnalysis />
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="allocation">
              <Card className="col-span-7">
                <CardHeader className="text-center">
                  <CardTitle>Allocation</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col md:flex-row h-[400px]">
                  <div className="w-full md:w-1/2 pl-2">
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={portfolioData}
                          cx="50%"
                          cy="50%"
                          innerRadius={80}
                          outerRadius={120}
                          paddingAngle={2}
                          dataKey="value"
                        >
                          {portfolioData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          content={({ active, payload }) => {
                            if (active && payload && payload.length > 0 && payload[0]?.payload) {
                              const data = payload[0].payload
                              return (
                                <div className="rounded-lg border bg-background p-3 shadow-lg">
                                  <div className="grid gap-1">
                                    <span className="font-semibold" style={{ color: data.color }}>
                                      {data.name}
                                    </span>
                                    <span className="text-sm">
                                      ${data.value.toLocaleString()}
                                    </span>
                                    <span className="text-xs text-muted-foreground">
                                      {data.suiAmount.toFixed(2)} SUI
                                    </span>
                                  </div>
                                </div>
                              )
                            }
                            return null
                          }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="w-full md:w-1/2">
                    <div className="space-y-4">
                      {portfolioData.map((item, index) => (
                        <div key={index} className="flex items-center">
                          <div className="w-2 h-2 rounded-full mr-2" style={{ backgroundColor: item.color }}></div>
                          <div className="flex-1 flex justify-between items-start">
                            <span className="font-medium">{item.name}</span>
                            <span className="flex flex-col items-end">
                              <span>
                                ${item.value.toLocaleString()} (
                                {((item.value / portfolioData.reduce((sum, i) => sum + i.value, 0)) * 100).toFixed(1)}
                                %)
                              </span>
                              <span className="text-sm text-muted-foreground">{item.suiAmount.toFixed(2)} SUI</span>
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="analytics">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart2 className="h-5 w-5" />
                    Portfolio Analytics
                  </CardTitle>
                  <CardDescription>Real-time AI-powered portfolio analysis</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-8">
                    <div className="grid gap-6">
                      {analyticsData.map((entry, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.5, delay: index * 0.1 }}
                          className="grid gap-2"
                        >
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">{entry.category}</span>
                            <motion.span
                              className="text-sm text-muted-foreground"
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              transition={{ duration: 0.5, delay: index * 0.1 + 0.3 }}
                            >
                              {entry.value}%
                            </motion.span>
                          </div>
                          <div className="h-2 rounded-full bg-secondary overflow-hidden">
                            <motion.div
                              className="h-full rounded-full bg-primary"
                              initial={{ width: 0 }}
                              animate={{ width: `${entry.value}%` }}
                              transition={{ duration: 0.8, delay: index * 0.1 + 0.5, ease: "easeOut" }}
                            />
                          </div>
                        </motion.div>
                      ))}
                    </div>

                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.8 }}
                      className="rounded-lg border p-6 bg-black/20"
                    >
                      <h4 className="text-sm font-semibold mb-4 flex items-center gap-2">
                        <Sparkles className="h-4 w-4" />
                        AI Insights
                      </h4>
                      <div className="space-y-4">
                        <p className="text-sm text-muted-foreground">
                          Based on current market conditions and your portfolio composition:
                        </p>
                        <ul className="space-y-2 text-sm">
                          <motion.li
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 1 }}
                            className="flex items-start gap-2"
                          >
                            <TrendingUp className="h-4 w-4 text-green-500 mt-1" />
                            <span>Strong diversification across major asset classes</span>
                          </motion.li>
                          {/* Add more insights with animations */}
                        </ul>
                      </div>
                    </motion.div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="reports">
              <Card>
                <CardHeader>
                  <CardTitle>Activity Logs</CardTitle>
                  <CardDescription>Transaction history and AI actions</CardDescription>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-[600px] w-full pr-4">
                    <ul className="space-y-4">
                      {activityLogs.map((log, index) => (
                        <li key={index} className="border-b pb-4 last:border-b-0">
                          <div className="flex justify-between items-start">
                            <div>
                              <span className="font-semibold">{log.date}:</span> {log.action}
                              {log.aiGenerated && (
                                <span className="ml-2 text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                                  AI Generated
                                </span>
                              )}
                            </div>
                            <div className="text-sm text-muted-foreground">Fee: {log.fee} SUI</div>
                          </div>
                          <div className="mt-2 text-sm">
                            <a
                              href={`https://explorer.sui.io/txblock/${log.txHash}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline"
                            >
                              View on Sui Explorer
                            </a>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </ScrollArea>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="chart">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>TradingView Chart</CardTitle>
                    <CardDescription>Real-time price charts</CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    <Select value={selectedAsset} onValueChange={setSelectedAsset}>
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select Asset" />
                      </SelectTrigger>
                      <SelectContent>
                        {tradingPairs.map((pair) => (
                          <SelectItem key={pair.value} value={pair.value}>
                            <div className="flex items-center">
                              <span>{pair.label}</span>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>

                    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                      <DialogTrigger asChild>
                        <Button variant="outline" size="icon">
                          <PlusCircle className="h-4 w-4" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Add Trading Pair</DialogTitle>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                          <div className="grid gap-2">
                            <Label htmlFor="symbol">Trading Pair Symbol</Label>
                            <Input
                              id="symbol"
                              placeholder="BTC/USD"
                              value={newPair.symbol}
                              onChange={(e) => setNewPair({ ...newPair, symbol: e.target.value })}
                            />
                            <p className="text-sm text-muted-foreground">
                              Format: ASSET/USD (e.g., BTC/USD, ETH/USD)
                            </p>
                          </div>
                          <div className="grid gap-2">
                            <Label htmlFor="exchange">Exchange</Label>
                            <Select
                              value={newPair.exchange}
                              onValueChange={(value) => setNewPair({ ...newPair, exchange: value })}
                            >
                              <SelectTrigger>
                                <SelectValue placeholder="Select Exchange" />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="BINANCE">Binance</SelectItem>
                                <SelectItem value="COINBASE">Coinbase</SelectItem>
                                <SelectItem value="KRAKEN">Kraken</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                        </div>
                        <div className="flex justify-end">
                          <Button onClick={handleAddPair}>Add Pair</Button>
                        </div>
                      </DialogContent>
                    </Dialog>
                  </div>
                </CardHeader>
                <CardContent>
                  <TradingViewChart
                    symbol={`${tradingPairs.find(p => p.value === selectedAsset)?.exchange}:${selectedAsset}`}
                    theme="light"
                  />
                </CardContent>
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>

      {/* Transaction notifications */}
      {showTransactionSuccess && lastTransaction && (
        <TransactionResult
          type={lastTransaction.type}
          fromAmount={lastTransaction.fromAmount}
          toAmount={lastTransaction.toAmount}
          txHash={lastTransaction.txHash}
          additionalInfo={lastTransaction.additionalInfo}
          onClose={() => {
            setShowTransactionSuccess(false)
            setTransactionError(null)
          }}
          position="center"
          status={transactionError ? "error" : "success"}
          errorMessage={transactionError || undefined}
        />
      )}
    </div>
  )
}

