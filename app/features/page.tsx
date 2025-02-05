import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ClientThemeToggle } from "@/components/client-theme-toggle"
import { StarsBackground } from "@/components/stars-background"
import { Home, Search, Zap, Brain, Sparkles } from "lucide-react"

export default function FeaturesPage() {
  const features = [
    {
      icon: Search,
      title: "Advanced Search",
      description: "Powerful Sui-focused search capabilities to find exactly what you need.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Optimized for speed, delivering instant results for your Sui queries.",
    },
    {
      icon: Brain,
      title: "AI-Powered Insights",
      description: "Intelligent analysis and suggestions tailored to the Sui ecosystem.",
    },
    {
      icon: Sparkles,
      title: "Customizable Experience",
      description: "Personalize your search preferences and dashboard for a unique experience.",
    },
  ]

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
            <Link href="/search">
              <Button variant="ghost">Search</Button>
            </Link>
            <Link href="/features">
              <Button variant="ghost">Features</Button>
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

      <main className="flex-grow container mx-auto px-4 py-16 flex flex-col items-center relative">
        <StarsBackground />
        <h1 className="text-4xl font-bold mb-12">Aegir Features</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl">
          {features.map((feature, index) => (
            <Card key={index} className="bg-background/80 backdrop-blur-sm">
              <CardHeader className="flex flex-row items-center space-x-4">
                <feature.icon className="w-8 h-8 text-primary" />
                <CardTitle>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p>{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>

      <footer className="border-t mt-16 bg-background/95">
        <div className="container mx-auto p-4 text-center text-sm text-muted-foreground">
          © 2025 Aegir. All rights reserved. Powered by Sui.
        </div>
      </footer>
    </div>
  )
}

