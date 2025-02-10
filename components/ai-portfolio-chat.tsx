"use client"

import { useRef, useEffect, useState } from "react"
import { Card } from "./ui/card"
import { Input } from "./ui/input"
import { Button } from "./ui/button"
import { Send, Bot } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { SuiAgent, SuiAgentResponse } from "@/lib/sui-agent"

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
    updateHubInfo: (updates: SuiAgentResponse['updates']) => void
  }
}

export function AIPortfolioChat({ data }: AIPortfolioChatProps) {
  const [messages, setMessages] = useState<Message[]>([{
    role: 'assistant',
    content: "Hello! I'm your Sui portfolio assistant. How can I help you today?",
    timestamp: new Date()
  }])
  const [input, setInput] = useState("")
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const [isAtBottom, setIsAtBottom] = useState(true)

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      const { scrollHeight, clientHeight } = chatContainerRef.current
      chatContainerRef.current.scrollTop = scrollHeight - clientHeight
    }
  }

  // Handle scroll events to detect if we're at the bottom
  const handleScroll = () => {
    if (chatContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current
      const bottom = Math.abs(scrollHeight - clientHeight - scrollTop) < 10
      setIsAtBottom(bottom)
    }
  }

  // Auto-scroll only if we were at the bottom before new message
  useEffect(() => {
    if (isAtBottom) {
      scrollToBottom()
    }
  }, [messages, isAtBottom])

  // Add scroll event listener
  useEffect(() => {
    const container = chatContainerRef.current
    if (container) {
      container.addEventListener('scroll', handleScroll)
      return () => container.removeEventListener('scroll', handleScroll)
    }
  }, [])

  const processQuery = async (query: string) => {
    try {
      const userMessage: Message = {
        role: 'user',
        content: query,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, userMessage])

      // Use the Sui Agent with instruction for concise responses
      const agent = SuiAgent.getInstance();
      const result: SuiAgentResponse = await agent.processQuery(
        `Please provide a concise response (max 2-3 sentences) to: ${query}`,
        {
          suiPrice: data.suiPrice,
          totalValue: data.totalPortfolioValue,
          treasury: {
            usdc: data.treasuryUSDC,
            sui: data.treasurySUI
          }
        }
      );

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
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    await processQuery(input.trim())
    setInput("")
  }

  return (
    <div className="flex flex-col h-full max-h-screen">
      {/* Header */}
      <div className="shrink-0 px-4 py-2 border-b border-white/10">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <Bot className="h-5 w-5" />
          AI Assistant
        </h2>
      </div>

      {/* Messages Container */}
      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent hover:scrollbar-thumb-white/20"
      >
        <div className="flex flex-col space-y-4">
          <AnimatePresence initial={false}>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.2 }}
                className={`rounded-lg p-3 ${message.role === 'assistant'
                  ? 'bg-white/5'
                  : 'bg-blue-500/10 ml-auto max-w-[80%]'
                  }`}
              >
                <p className="text-sm text-white">{message.content}</p>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* Input Container - Fixed at bottom */}
      <div className="shrink-0 p-4 border-t border-white/10 bg-black/20 backdrop-blur-sm">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your portfolio..."
            className="flex-1 bg-white/5 border-white/10 text-white placeholder:text-white/50"
          />
          <Button
            type="submit"
            size="icon"
            className="bg-white/10 hover:bg-white/20"
            disabled={!input.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </div>
  )
}

