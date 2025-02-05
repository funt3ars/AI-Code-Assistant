import { NextResponse } from 'next/server'
import { tavily } from '@tavily/core'

export async function POST(req: Request) {
  try {
    const { query } = await req.json()

    if (!query || typeof query !== 'string') {
      return NextResponse.json({ error: 'Invalid query parameter' }, { status: 400 })
    }

    if (!process.env.TAVILY_API_KEY) {
      console.error('TAVILY_API_KEY environment variable is not set')
      return NextResponse.json({ error: 'Search service is not configured. Please contact the administrator.' }, { status: 500 })
    }

    const tvly = tavily({ apiKey: process.env.TAVILY_API_KEY })

    const response = await tvly.search(query)

    if (!response || !Array.isArray(response.results)) {
      console.error('Invalid response from Tavily API:', response)
      return NextResponse.json({ error: 'Invalid response from search service' }, { status: 500 })
    }

    return NextResponse.json({ results: response.results })

  } catch (error) {
    console.error('Web Search error:', error)
    return NextResponse.json({ error: 'An error occurred during web search. Please try again later.' }, { status: 500 })
  }
}

