"use client"

import { useEffect, useRef } from "react"

interface Star {
  x: number
  y: number
  size: number
  speed: number
}

export function StarsBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const context = canvas.getContext("2d", { alpha: false })
    if (!context) return

    const canvasElement = canvas
    const ctx = context

    const resizeCanvas = () => {
      const { innerWidth: width, innerHeight: height } = window
      canvasElement.width = width
      canvasElement.height = height
      canvasElement.style.width = `${width}px`
      canvasElement.style.height = `${height}px`
    }

    resizeCanvas()
    window.addEventListener("resize", resizeCanvas)

    const stars: Star[] = []
    const numStars = 200
    const maxSize = 2

    // Initialize stars
    for (let i = 0; i < numStars; i++) {
      stars.push({
        x: Math.random() * canvasElement.width,
        y: Math.random() * canvasElement.height,
        size: Math.random() * maxSize,
        speed: Math.random() * 0.2 + 0.1,
      })
    }

    let animationFrameId: number

    function animate() {
      // Clear canvas
      ctx.fillStyle = '#000000'
      ctx.fillRect(0, 0, canvasElement.width, canvasElement.height)

      // Draw stars
      ctx.fillStyle = '#ffffff'
      stars.forEach((star) => {
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2)
        ctx.fill()

        star.y += star.speed

        if (star.y > canvasElement.height) {
          star.y = 0
          star.x = Math.random() * canvasElement.width
        }
      })

      animationFrameId = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener("resize", resizeCanvas)
      cancelAnimationFrame(animationFrameId)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 w-full h-full pointer-events-none"
      style={{ zIndex: 0 }}
    />
  )
}

