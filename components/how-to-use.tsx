"use client"

import { Wallet, ChartBar, Brain, Sparkles } from "lucide-react"
import { motion } from "framer-motion"
import Image from 'next/image'

const shineEffect = `
  @keyframes shine {
    to {
      background-position: 200% center;
    }
  }
  .shine-on-hover:hover {
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    background-size: 200% 100%;
    animation: shine 1s linear infinite;
  }
`

export function HowToUse() {
  const steps = [
    {
      icon: Wallet,
      title: "Connect Wallet",
      description: "Connect your Sui wallet to access personalized DeFi insights.",
    },
    {
      icon: ChartBar,
      title: "Portfolio Analysis",
      description: "Get real-time analysis of your DeFi positions and opportunities.",
    },
    {
      icon: Brain,
      title: "AI Insights",
      description:
        "Receive intelligent DeFi recommendations from Midas, your personal financial advisor.",
    },
    {
      icon: Sparkles,
      title: "Optimize & Grow",
      description: "Execute optimal DeFi strategies based on Midas's expert analysis.",
    },
  ]

  return (
    <section className="text-center">
      <div className="mb-8">
        <Image
          src="/midas-logo.png"
          alt="Midas Logo"
          width={120}
          height={120}
          className="mx-auto"
        />
      </div>
      <h2 className="text-3xl font-bold mb-6">How to Use Midas</h2>
      <p className="mb-8 text-lg text-muted-foreground">
        Your intelligent DeFi companion for optimizing portfolio performance on the Sui blockchain.
      </p>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            className="bg-card rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 shine-on-hover"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{ position: "relative", overflow: "hidden" }}
          >
            <style jsx>{shineEffect}</style>
            <step.icon className="h-12 w-12 mx-auto mb-4 text-primary" />
            <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
            <p className="text-muted-foreground">{step.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  )
}

