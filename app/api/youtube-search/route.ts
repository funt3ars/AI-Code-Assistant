import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  try {
    const { query } = await req.json()
    const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&key=${process.env.YOUTUBE_API_KEY}`)

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('YouTube Search error:', error)
    return NextResponse.json({ error: 'An error occurred during YouTube search' }, { status: 500 })
  }
}

