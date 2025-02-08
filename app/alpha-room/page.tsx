"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Bot, AlertCircle } from "lucide-react"
import useSWR from "swr"

interface Message {
    role: 'midas' | 'atlas'
    content: string
    timestamp: Date
}

interface MarketData {
    suiPrice: number
    marketCap: number
    volume24h: number
    priceChange24h: number
    marketSentiment: {
        score: number
        trend: 'bullish' | 'bearish' | 'neutral'
        signals: string[]
    }
}

async function fetchAnalysis(context: any) {
    try {
        const response = await fetch('/api/alpha', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ context })
        });
        if (!response.ok) throw new Error('Failed to fetch analysis');
        return response.json();
    } catch (error) {
        console.error('Error fetching analysis:', error);
        throw error;
    }
}

function AlphaRoomContent() {
    const [messages, setMessages] = useState<Message[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);

    // Fetch market data using SWR
    const { data: marketData, error: marketError, isLoading } = useSWR<MarketData>('/api/market-data');

    // Initialize conversation when market data is available
    useEffect(() => {
        if (marketData && messages.length === 0) {
            const initialMessages: Message[] = [
                {
                    role: 'midas',
                    content: "Atlas, I've noticed some interesting movements in the Sui market. What's your analysis?",
                    timestamp: new Date()
                }
            ];
            setMessages(initialMessages);

            // Fetch initial analysis
            fetchAnalysis({
                marketData,
                technicalIndicators: {
                    rsi: marketData.marketSentiment.score,
                    trend: marketData.marketSentiment.trend
                },
                sentiment: marketData.marketSentiment
            }).then(response => {
                setMessages(prev => [...prev, {
                    role: 'atlas',
                    content: response.atlas,
                    timestamp: new Date()
                }]);
            }).catch(error => {
                console.error('Error in initial analysis:', error);
            });
        }
    }, [marketData, messages.length]);

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
            </div>
        );
    }

    if (marketError) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-destructive">
                <AlertCircle className="w-8 h-8 mb-2" />
                <p>Failed to load market data</p>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="flex items-center justify-between px-4 py-2 border-b">
                <h2 className="text-lg font-semibold">Alpha Room</h2>
                <div className="flex items-center space-x-2">
                    <span className="text-sm text-muted-foreground">Live Analysis</span>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                </div>
            </div>

            <ScrollArea ref={scrollRef} className="flex-1 p-4">
                <AnimatePresence initial={false}>
                    {messages.map((message, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className={`flex items-start space-x-3 mb-4 ${message.role === 'atlas' ? 'flex-row-reverse space-x-reverse' : ''
                                }`}
                        >
                            <div className={`flex items-center justify-center w-8 h-8 rounded-full ${message.role === 'midas' ? 'bg-primary' : 'bg-secondary'
                                }`}>
                                <Bot className="w-4 h-4 text-primary-foreground" />
                            </div>
                            <div className={`flex flex-col ${message.role === 'atlas' ? 'items-end' : ''}`}>
                                <div className="text-sm font-medium">
                                    {message.role === 'midas' ? 'Midas Rex' : 'Atlas Prime'}
                                </div>
                                <div className={`mt-1 p-3 rounded-lg ${message.role === 'midas'
                                    ? 'bg-primary text-primary-foreground'
                                    : 'bg-secondary text-secondary-foreground'
                                    }`}>
                                    {message.content}
                                </div>
                                <span className="text-xs text-muted-foreground mt-1">
                                    {message.timestamp.toLocaleTimeString()}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </ScrollArea>
        </div>
    );
}

export default function Page() {
    return <AlphaRoomContent />;
} 