"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useState, useRef, useEffect } from "react"
import { Send, Bot, User, RefreshCw, MessageSquare, Crown } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { SuiAgent } from "@/lib/sui-agent"
import { useWalletKit } from '@mysten/wallet-kit'
import { TransactionBlock } from '@mysten/sui.js/transactions'
import { TransactionHelper } from '@/lib/sui/transaction-helper'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface AIPortfolioChatProps {
  data: {
    suiPrice: number | null
    totalPortfolioValue: number
    portfolioData: any[]
    treasuryUSDC: number
    treasurySUI: number
    updateHubInfo: (updates: any) => void
  }
}

export function AIPortfolioChat({ data }: AIPortfolioChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! How can I help you today?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  const { currentAccount, signAndExecuteTransactionBlock } = useWalletKit()
  const transactionHelper = new TransactionHelper()

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleTransaction = async (tx: TransactionBlock) => {
    try {
      if (!currentAccount?.address) {
        throw new Error('Please connect your wallet first')
      }

      // Add pending message
      const pendingMessage: Message = {
        role: 'assistant',
        content: 'Processing transaction...',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, pendingMessage])

      // Execute transaction
      const result = await signAndExecuteTransactionBlock({
        transactionBlock: tx,
        chain: 'mainnet',
        options: {
          showInput: true,
          showEffects: true,
          showEvents: true,
        }
      })

      if (result.effects?.status?.status === 'success') {
        const successMessage = {
          role: 'assistant',
          content: `Transaction successful!\nDigest: ${result.digest.substring(0, 10)}...\nGas used: ${result.effects.gasUsed.computationCost} MIST`,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, successMessage])
      } else {
        throw new Error('Transaction failed: ' + result.effects?.status?.error)
      }

      return result
    } catch (error) {
      console.error('Transaction failed:', error)
      const errorMessage = {
        role: 'assistant',
        content: `Transaction failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
      throw error
    }
  }

  const processQuery = async (query: string) => {
    try {
      if (!currentAccount?.address) {
        throw new Error('Please connect your wallet first')
      }

      // Add user message
      const userMessage: Message = {
        role: 'user',
        content: query,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, userMessage])

      const response = await fetch('/api/sui', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: query,
          context: {
            walletAddress: currentAccount.address,
            connected: true,
            suiPrice: data.suiPrice
          }
        })
      })

      const result = await response.json()

      if (result.transaction) {
        await handleTransaction(result.transaction)
      } else {
        const assistantMessage: Message = {
          role: 'assistant',
          content: result.response,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, assistantMessage])
      }

      if (result.updates) {
        data.updateHubInfo(result.updates)
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsProcessing(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isProcessing) return

    const query = input.trim()
    setInput('')
    await processQuery(query)
  }

  return (
    <div className="flex h-full flex-col">
      {/* Chat Header */}
      <div className="border-b border-gray-800 p-4">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-emerald-500/10 flex items-center justify-center">
            <MessageSquare className="h-4 w-4 text-emerald-500" />
          </div>
          <div>
            <h2 className="text-sm font-semibold">Midas Rex</h2>
            <p className="text-xs text-gray-400">Your Sui Portfolio Assistant</p>
          </div>
        </div>
      </div>

      <ScrollArea ref={scrollRef} className="flex-1 p-4">
        <div className="space-y-4">
          <AnimatePresence mode="wait">
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className={`flex gap-2 ${message.role === 'assistant' ? 'flex-row' : 'flex-row-reverse'}`}
              >
                <div className={`flex-1 ${message.role === 'assistant'
                  ? 'bg-gray-900/50 rounded-br-xl'
                  : 'bg-emerald-500/10 rounded-bl-xl'
                  } rounded-t-xl p-3`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    {message.role === 'assistant' ? (
                      <Bot className="h-4 w-4" />
                    ) : (
                      <User className="h-4 w-4" />
                    )}
                    <span className="text-xs text-muted-foreground">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-sm">{message.content}</p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isProcessing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-2 text-sm text-muted-foreground"
            >
              <RefreshCw className="h-4 w-4 animate-spin" />
              Processing...
            </motion.div>
          )}
        </div>
      </ScrollArea>

      <form onSubmit={handleSubmit} className="p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your portfolio..."
            disabled={isProcessing}
          />
          <Button
            type="submit"
            size="icon"
            disabled={isProcessing || !input.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  )
}

