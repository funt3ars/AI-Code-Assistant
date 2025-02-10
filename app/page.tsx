"use client"

import { AnimatedSection } from "@/components/animated-section"
import { StarsBackground } from "@/components/stars-background"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Header } from "@/components/header"
import { TypewriterEffect } from "@/components/ui/typewriter-effect"
import { motion } from "framer-motion"
import { AlphaRoom } from "@/components/alpha-room"
import { Card } from "@/components/ui/card"

export default function Home() {
  const words = [
    {
      text: "Welcome",
    },
    {
      text: "to",
    },
    {
      text: "Midas",
      className: "bg-gradient-to-r from-white to-white/90 bg-clip-text text-transparent",
    },
  ]

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden flex flex-col">
      <StarsBackground />
      <div className="relative z-10 flex-1 flex flex-col">
        <Header />

        <main className="flex-1 w-full max-w-7xl mx-auto flex items-center justify-center">
          <AnimatedSection className="w-full">
            <div className="container px-4 md:px-6">
              <div className="flex flex-col items-center space-y-8 text-center">
                <div className="space-y-4">
                  <div className="h-[calc(theme(fontSize.7xl)*theme(lineHeight.tight))] overflow-hidden">
                    <TypewriterEffect words={words} />
                  </div>
                  <p className="mx-auto max-w-[700px] text-gray-400 md:text-xl">
                    Midas Rex: The AI-Powered DeFi Agent Turning Data Into Gold.
                  </p>
                  <div className="mt-16 flex gap-4 justify-center">
                    <Button
                      asChild
                      size="lg"
                      className="px-8 py-6 text-lg bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 shadow-lg hover:shadow-blue-500/25 transition-all duration-300 hover:scale-105"
                    >
                      <Link href="/hub">
                        Enter Hub
                      </Link>
                    </Button>
                    <Button
                      asChild
                      size="lg"
                      className="px-8 py-6 text-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 shadow-lg hover:shadow-purple-500/25 transition-all duration-300 hover:scale-105"
                    >
                      <Link href="/alpha-room">
                        Alpha Room
                      </Link>
                    </Button>
                  </div>
                </div>

                <div className="flex gap-4 mt-8">
                  <a
                    href="https://twitter.com/midasprotocol"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center hover:bg-white/20 transition-colors"
                  >
                    <img
                      src="https://img.icons8.com/ios/50/FFFFFF/x.png"
                      alt="X (Twitter)"
                      className="h-5 w-5"
                    />
                  </a>
                  <a
                    href="https://github.com/midasprotocol"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center hover:bg-white/20 transition-colors"
                  >
                    <img
                      src="https://img.icons8.com/ios/50/FFFFFF/github.png"
                      alt="GitHub"
                      className="h-5 w-5"
                    />
                  </a>
                  <a
                    href="https://t.me/midasprotocol"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center hover:bg-white/20 transition-colors"
                  >
                    <img
                      src="https://img.icons8.com/windows/32/FFFFFF/telegram-app.png"
                      alt="Telegram"
                      className="h-5 w-5"
                    />
                  </a>
                </div>
              </div>
            </div>
          </AnimatedSection>
        </main>

        <footer className="border-t border-white/10 py-4">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">© 2025 Midas. All rights reserved.</p>
              <nav className="flex gap-4">
                <Link href="#" className="text-xs text-muted-foreground hover:text-white transition-colors">
                  Terms of Service
                </Link>
                <Link href="#" className="text-xs text-muted-foreground hover:text-white transition-colors">
                  Privacy
                </Link>
              </nav>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}

