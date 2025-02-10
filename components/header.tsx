"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ConnectButton } from "@mysten/wallet-kit"
import Image from "next/image"

export function Header() {
  return (
    <header className="border-b border-white/10 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex gap-6 items-center">
            <Link href="/" className="flex items-center">
              <div className="w-10 h-10 relative overflow-hidden rounded-full bg-black/40 backdrop-blur-sm">
                <div className="absolute inset-0 bg-cyan-500/20 animate-pulse" />
                <div
                  className="absolute inset-0"
                  style={{
                    boxShadow: `
                      inset 0 0 20px rgba(64, 224, 208, 0.5),
                      0 0 20px rgba(64, 224, 208, 0.3)
                    `,
                  }}
                />
                <Image
                  src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/beautiful_flat-style_logo_desi-Mxrj2lGzGBxZB7jWTgQ6vXatSStLad.jpeg"
                  alt="Midas Logo"
                  width={40}
                  height={40}
                  className="object-cover relative z-10"
                  priority
                  style={{
                    filter: "drop-shadow(0 0 10px rgba(64, 224, 208, 0.5))",
                  }}
                />
              </div>
            </Link>
            <nav className="hidden md:flex gap-6">
              <Link href="/hub" className="text-sm text-zinc-400 hover:text-white transition-colors">
                Hub
              </Link>
              <Link href="/alpha-room" className="text-sm text-zinc-400 hover:text-white transition-colors">
                Alpha Room
              </Link>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <ConnectButton />
          </div>
        </div>
      </div>
    </header>
  )
}

