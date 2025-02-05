"use client"

import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"

interface CheckmarkProps {
  size?: number
  strokeWidth?: number
  color?: string
  className?: string
}

const draw = {
  hidden: { pathLength: 0, opacity: 0 },
  visible: (i: number) => ({
    pathLength: 1,
    opacity: 1,
    transition: {
      pathLength: {
        delay: i * 0.2,
        type: "spring",
        duration: 1.5,
        bounce: 0.2,
        ease: "easeInOut",
      },
      opacity: { delay: i * 0.2, duration: 0.2 },
    },
  }),
}

function Checkmark({ size = 100, strokeWidth = 2, color = "currentColor", className = "" }: CheckmarkProps) {
  return (
    <motion.svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      initial="hidden"
      animate="visible"
      className={className}
    >
      <title>Animated Checkmark</title>
      <motion.circle
        cx="50"
        cy="50"
        r="40"
        stroke={color}
        variants={draw}
        custom={0}
        style={{
          strokeWidth,
          strokeLinecap: "round",
          fill: "transparent",
        }}
      />
      <motion.path
        d="M30 50L45 65L70 35"
        stroke={color}
        variants={draw}
        custom={1}
        style={{
          strokeWidth,
          strokeLinecap: "round",
          strokeLinejoin: "round",
          fill: "transparent",
        }}
      />
    </motion.svg>
  )
}

function CrossMark({ size = 100, strokeWidth = 2, color = "currentColor", className = "" }: CheckmarkProps) {
  return (
    <motion.svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      initial="hidden"
      animate="visible"
      className={className}
    >
      <title>Animated Crossmark</title>
      <motion.circle
        cx="50"
        cy="50"
        r="40"
        stroke={color}
        variants={draw}
        custom={0}
        style={{
          strokeWidth,
          strokeLinecap: "round",
          fill: "transparent",
        }}
      />
      <motion.path
        d="M35 35L65 65M65 35L35 65"
        stroke={color}
        variants={draw}
        custom={1}
        style={{
          strokeWidth,
          strokeLinecap: "round",
          strokeLinejoin: "round",
          fill: "transparent",
        }}
      />
    </motion.svg>
  )
}

interface TransactionResultProps {
  type: 'STAKE' | 'SWAP' | 'TRANSFER' | 'NFT_PURCHASE' | 'LIQUIDITY_ADD' | 'GOVERNANCE' | 'DEFAULT'
  fromAmount: number
  toAmount: number
  txHash: string
  status: 'success' | 'error'
  errorMessage?: string
  additionalInfo?: {
    tokenSymbol?: string
    nftName?: string
    poolName?: string
    proposalId?: string
  }
  onClose: () => void
  position?: 'bottom-left' | 'bottom-right' | 'center'
}

export function TransactionResult({
  type,
  fromAmount,
  toAmount,
  txHash,
  status,
  errorMessage,
  additionalInfo,
  onClose,
  position = 'center'
}: TransactionResultProps) {
  const positionClasses = {
    'bottom-left': 'fixed bottom-4 left-4',
    'bottom-right': 'fixed bottom-4 right-4',
    'center': 'fixed inset-0 flex items-center justify-center'
  }

  return (
    <motion.div
      className={`${positionClasses[position]} z-50`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    >
      {position === 'center' && (
        <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
      )}

      <Card className={`${position === 'center'
          ? 'w-[320px] relative'
          : 'w-[320px]'
        } p-4 bg-emerald-500/10 border-emerald-500/20 backdrop-blur-sm`}
      >
        <CardContent className="p-0 space-y-3">
          <div className="flex items-center gap-3">
            <div className="relative">
              {status === 'success' ? (
                <Checkmark
                  size={40}
                  strokeWidth={3}
                  color="rgb(16 185 129)"
                  className="relative z-10"
                />
              ) : (
                <CrossMark
                  size={40}
                  strokeWidth={3}
                  color="rgb(239 68 68)"
                  className="relative z-10"
                />
              )}
            </div>
            <div className="flex-1">
              <h3 className="text-sm font-medium text-emerald-500">
                {status === 'success' ? 'Transaction Successful' : 'Transaction Failed'}
              </h3>
              <p className="text-xs text-emerald-500/80">
                {fromAmount.toFixed(2)} SUI (${toAmount.toFixed(2)})
              </p>
            </div>
            <motion.a
              href={`https://explorer.sui.io/txblock/${txHash}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-emerald-500/90 hover:text-emerald-400 transition-colors"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              View
            </motion.a>
          </div>

          {status === 'error' && errorMessage && (
            <p className="text-xs text-red-400/90">
              {errorMessage}
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
} 