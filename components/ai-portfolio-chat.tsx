"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useState, useRef, useEffect } from "react"
import { Send, Bot, User, RefreshCw } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { SuiAgent } from "@/lib/sui-agent"

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
      content: 'Hello! I\'m your Sui portfolio assistant. How can I help you today?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const processQuery = async (query: string) => {
    try {
      setIsProcessing(true)

      const userMessage: Message = {
        role: 'user',
        content: query,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, userMessage])

      // Use the Sui Agent
      const agent = SuiAgent.getInstance();
      const result = await agent.processQuery(query, {
        suiPrice: data.suiPrice,
        totalValue: data.totalPortfolioValue,
        treasury: {
          usdc: data.treasuryUSDC,
          sui: data.treasurySUI
        }
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: result.response,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])

      if (result.updates) {
        data.updateHubInfo(result.updates)
      }

    } catch (error) {
      console.error('Error processing query:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
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
    <div className="flex flex-col h-full">
      <div className="px-4 py-2">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <Bot className="h-5 w-5" />
          AI Assistant
        </h2>
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

