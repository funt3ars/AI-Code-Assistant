'use client'

import { useState } from 'react'
import { Search } from 'lucide-react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { useToast } from './ui/use-toast'

export function SearchForm({ onSearch }: { onSearch: (results: any) => void }) {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isLoading) {
      setIsLoading(true)
      try {
        const response = await fetch('/api/web-search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: input }),
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'An error occurred during the search.')
        }

        const data = await response.json()
        onSearch(data.results)
      } catch (error) {
        console.error('Search error:', error)
        toast({
          title: "Search Error",
          description: (error as Error).message || "An unexpected error occurred. Please try again.",
          variant: "destructive",
        })
      } finally {
        setIsLoading(false)
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="flex space-x-2">
        <div className="relative flex-grow">
          <Search className="absolute left-4 top-3 h-6 w-6 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search the web..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="h-14 pl-14 pr-4 text-lg"
            disabled={isLoading}
          />
        </div>
        <Button 
          type="submit" 
          disabled={isLoading} 
          className="h-14 px-6 bg-[#4285F4] hover:bg-[#4285F4]/90"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </Button>
      </div>
    </form>
  )
}

