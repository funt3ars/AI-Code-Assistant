"use client"

import Link from "next/link"
import type React from "react"
import { ConnectButton } from "@mysten/wallet-kit"
import Image from "next/image"

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        {/* Left side with logo only */}
        <div className="flex-1 flex items-center">
          <Link href="/" className="flex items-center justify-center">
            <div className="w-10 h-10 bg-black/40 backdrop-blur-sm flex items-center justify-center">
              <Image
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/beautiful_flat-style_logo_desi-Mxrj2lGzGBxZB7jWTgQ6vXatSStLad.jpeg"
                alt="Aegir Logo"
                width={32}
                height={32}
                className="rounded-full"
                style={{
                  filter: "drop-shadow(0 0 10px rgba(64, 224, 208, 0.5))",
                }}
              />
            </div>
          </Link>
        </div>

        {/* Right side with connect button only */}
        <div className="flex items-center justify-end">
          <ConnectButton />
        </div>
      </div>
    </header>
  )
}

