"use client"

import { Button } from "@/components/ui/button"
import { Twitter, Send } from "lucide-react"

export function ThemeToggle() {
  return (
    <div className="flex items-center space-x-4">
      <a
        href="https://twitter.com/YourTwitterHandle"
        target="_blank"
        rel="noopener noreferrer"
        className="text-foreground hover:text-primary"
      >
        <Twitter size={20} />
      </a>
      <a
        href="https://t.me/YourTelegramChannel"
        target="_blank"
        rel="noopener noreferrer"
        className="text-foreground hover:text-primary"
      >
        <Send size={20} />
      </a>
      <Button variant="outline" size="sm" onClick={() => console.log("Connect wallet clicked")}>
        Connect Wallet
      </Button>
    </div>
  )
}

