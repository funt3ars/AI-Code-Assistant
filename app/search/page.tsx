"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { SearchForm } from "@/components/search-form"
import { Socials } from "@/components/socials"
import { SearchResults } from "@/components/search-results"
import { StarsBackground } from "@/components/stars-background"
import { AnimatedSection } from "@/components/animated-section"

export default function SearchPage() {
  const [searchResults, setSearchResults] = useState<any>(null)

  const handleSearch = (results: any) => {
    setSearchResults(results)
  }

  return (
    <div className="min-h-screen bg-background/95 text-foreground flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-16 flex flex-col items-center relative">
        <StarsBackground />
        <AnimatedSection className="w-full max-w-3xl text-center min-h-[calc(100vh-200px)] flex flex-col justify-center items-center">
          <h2 className="text-4xl font-bold mb-8">Sui-Powered Web Search Engine</h2>
          <SearchForm onSearch={handleSearch} />
          {searchResults && <SearchResults results={searchResults} />}
        </AnimatedSection>
      </main>
      <footer className="border-t mt-16 bg-background/95">
        <div className="container mx-auto p-4 text-center text-sm text-muted-foreground">
          <Socials />
          <div className="mt-4">© 2025 Aegir. All rights reserved. Powered by Sui.</div>
        </div>
      </footer>
    </div>
  )
}

