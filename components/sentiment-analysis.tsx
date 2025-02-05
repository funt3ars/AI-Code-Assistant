"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { useState, useEffect } from "react"
import { MessageCircle, TrendingUp, AlertCircle, ArrowUp, ArrowDown, RefreshCw } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

interface MarketSentiment {
  source: string
  sentiment: number
  confidence: number
  timestamp: string
  highlights: string[]
  impact: "HIGH" | "MEDIUM" | "LOW"
  trend: "up" | "down" | "neutral"
  tweetCount?: number
  keyInfluencers?: string[]
  priceImpact?: {
    prediction: "positive" | "negative" | "neutral"
    confidence: number
  }
}

export function SentimentAnalysis() {
  const [sentiments, setSentiments] = useState<MarketSentiment[]>([
    {
      source: "Twitter",
      sentiment: 0.85,
      confidence: 0.92,
      timestamp: "2m ago",
      highlights: [
        "Major SUI influencers showing bullish signals",
        "Increased staking activity discussion",
        "Positive community response to recent updates"
      ],
      impact: "HIGH",
      trend: "up",
      tweetCount: 1243,
      keyInfluencers: ["@SuiNetwork", "@MystenLabs", "@CryptoGuru"],
      priceImpact: {
        prediction: "positive",
        confidence: 0.87
      }
    },
    {
      source: "Community",
      sentiment: 0.75,
      confidence: 0.88,
      timestamp: "5m ago",
      highlights: [
        "Growing developer activity on Discord",
        "New DeFi protocol announcements",
        "Active governance participation"
      ],
      impact: "MEDIUM",
      trend: "up",
      tweetCount: 856,
      priceImpact: {
        prediction: "positive",
        confidence: 0.82
      }
    },
    {
      source: "Market",
      sentiment: 0.78,
      confidence: 0.85,
      timestamp: "15m ago",
      highlights: [
        "Institutional interest growing",
        "Partnership ecosystem expanding",
        "Technical indicators positive"
      ],
      impact: "HIGH",
      trend: "up",
      tweetCount: 967,
      priceImpact: {
        prediction: "positive",
        confidence: 0.89
      }
    }
  ])

  const [isRefreshing, setIsRefreshing] = useState(false)

  const refreshData = async () => {
    setIsRefreshing(true)
    // Simulate API call to sentiment analysis service
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsRefreshing(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Real-time Sentiment Analysis</h3>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={refreshData}
          className="flex items-center gap-2 text-sm text-emerald-500 hover:text-emerald-400"
        >
          <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          Refresh
        </motion.button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <AnimatePresence mode="wait">
          {sentiments.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <Card className="relative overflow-hidden h-full">
                <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent" />
                <div className="p-4 space-y-4 relative">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={item.sentiment > 0.8 ? "success" : "secondary"}
                        className="font-semibold"
                      >
                        {item.source}
                      </Badge>
                      {item.impact === "HIGH" && (
                        <Badge variant="destructive" className="font-semibold">
                          High Impact
                        </Badge>
                      )}
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {item.timestamp}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 bg-emerald-500/10 p-2 rounded-lg">
                    {item.trend === "up" ? (
                      <ArrowUp className="h-4 w-4 text-emerald-500" />
                    ) : (
                      <ArrowDown className="h-4 w-4 text-red-500" />
                    )}
                    <span className="text-sm font-medium">
                      {(item.sentiment * 100).toFixed(0)}% Positive
                    </span>
                    <div className="flex-1 h-1.5 bg-black/20 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-emerald-500"
                        initial={{ width: 0 }}
                        animate={{ width: `${item.sentiment * 100}%` }}
                        transition={{ duration: 0.8, delay: index * 0.1 }}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="text-sm font-medium">Key Highlights:</div>
                    <ul className="space-y-1">
                      {item.highlights.map((highlight, i) => (
                        <motion.li
                          key={i}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 + i * 0.1 }}
                          className="text-sm text-muted-foreground flex items-start gap-2"
                        >
                          <AlertCircle className="h-4 w-4 mt-0.5 text-emerald-500" />
                          {highlight}
                        </motion.li>
                      ))}
                    </ul>
                  </div>

                  <div className="pt-3 border-t border-gray-800">
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="space-y-1">
                        <span className="text-muted-foreground">Tweet Volume</span>
                        <div className="font-medium">{item.tweetCount?.toLocaleString()}</div>
                      </div>
                      <div className="space-y-1">
                        <span className="text-muted-foreground">Price Impact</span>
                        <div className="font-medium text-emerald-500">
                          {item.priceImpact?.confidence.toLocaleString(undefined, {
                            style: 'percent',
                            minimumFractionDigits: 0
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  )
} 