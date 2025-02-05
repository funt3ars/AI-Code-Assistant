import Link from "next/link"
import { HowToUse } from "../../components/how-to-use"
import { ClientThemeToggle } from "../../components/client-theme-toggle"
import { Button } from "../../components/ui/button"
import { Home } from "lucide-react"

export default function HowToUsePage() {
  return (
    <div className="min-h-screen bg-background/95 text-foreground flex flex-col">
      <header className="border-b sticky top-0 z-10 backdrop-blur-sm">
        <div className="container mx-auto flex items-center justify-between p-4 bg-transparent">
          <div className="flex items-center space-x-4">
            <Link href="/">
              <Button variant="ghost">
                <Home className="w-4 h-4 mr-2" />
                Home
              </Button>
            </Link>
            <Link href="/how-to-use">
              <Button variant="ghost">How to Use</Button>
            </Link>
            <Link href="/hub">
              <Button variant="ghost">Hub</Button>
            </Link>
          </div>
          <ClientThemeToggle />
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-16 flex flex-col items-center">
        <HowToUse />
      </main>

      <footer className="border-t mt-16 bg-background/95">
        <div className="container mx-auto p-4 text-center text-sm text-muted-foreground">
          © 2025 AetherMind. All rights reserved. Powered by Sui.
        </div>
      </footer>
    </div>
  )
}

