"use client"

import { useEffect, useRef } from "react"

declare global {
  interface Window {
    TradingView: any
  }
}

interface TradingViewChartProps {
  symbol?: string
  theme?: 'light' | 'dark'
  autosize?: boolean
  interval?: string
}

export function TradingViewChart({
  symbol = 'BINANCE:SUIUSDT',
  theme = 'dark',
  autosize = true,
  interval = '1D'
}: TradingViewChartProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const script = document.createElement("script")
    script.src = "https://s3.tradingview.com/tv.js"
    script.async = true
    script.onload = () => {
      if (containerRef.current && window.TradingView) {
        new window.TradingView.widget({
          container: containerRef.current,
          symbol: symbol,
          interval: interval,
          timezone: "Etc/UTC",
          theme: theme,
          style: "1",
          locale: "en",
          toolbar_bg: "#f1f3f6",
          enable_publishing: false,
          allow_symbol_change: true,
          save_image: false,
          hide_side_toolbar: false,
          autosize: autosize,
          studies: [
            "RSI@tv-basicstudies",
            "MASimple@tv-basicstudies",
            "MACD@tv-basicstudies"
          ],
          overrides: {
            "mainSeriesProperties.candleStyle.upColor": "#00C853",
            "mainSeriesProperties.candleStyle.downColor": "#FF5252",
            "mainSeriesProperties.candleStyle.borderUpColor": "#00C853",
            "mainSeriesProperties.candleStyle.borderDownColor": "#FF5252",
            "mainSeriesProperties.candleStyle.wickUpColor": "#00C853",
            "mainSeriesProperties.candleStyle.wickDownColor": "#FF5252",
          },
        })
      }
    }
    document.head.appendChild(script)

    return () => {
      script.remove()
    }
  }, [symbol, theme, autosize, interval])

  return (
    <div
      ref={containerRef}
      className="w-full h-full min-h-[400px] bg-black/20 backdrop-blur-sm rounded-lg"
    />
  )
}

