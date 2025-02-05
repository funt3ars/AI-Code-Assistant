import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const { query, depth } = await req.json()
  const searxngUrl = process.env.SEARXNG_URL || 'https://searx.be'

  const response = await fetch(`${searxngUrl}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      q: query,
      format: 'json',
      engines: depth === 'advanced' ? 'google,bing,duckduckgo' : 'google',
    }),
  })

  const data = await response.json()
  return NextResponse.json(data)
}

