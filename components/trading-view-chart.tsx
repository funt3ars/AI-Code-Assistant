"use client"

import { useEffect, useRef } from "react"

interface TradingViewChartProps {
  symbol: string
  theme?: "light" | "dark"
}

export function TradingViewChart({ symbol, theme = "light" }: TradingViewChartProps) {
  const container = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const script = document.createElement("script")
    script.src = "https://s3.tradingview.com/tv.js"
    script.async = true
    script.onload = () => {
      if (typeof TradingView !== "undefined" && container.current) {
        new TradingView.widget({
          autosize: true,
          symbol: symbol,
          interval: "D",
          timezone: "Etc/UTC",
          theme: theme,
          style: "1",
          locale: "en",
          toolbar_bg: "#f1f3f6",
          enable_publishing: false,
          hide_side_toolbar: false,
          allow_symbol_change: true,
          container_id: container.current.id,
        })
      }
    }
    document.head.appendChild(script)
    return () => {
      document.head.removeChild(script)
    }
  }, [symbol, theme])

  return <div ref={container} id={`tradingview_${symbol}`} className="w-full h-[600px]" />
}

