import { NextResponse } from 'next/server'
import rateLimit from 'express-rate-limit'
import { NextApiRequest, NextApiResponse } from 'next'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
})

const applyRateLimit = (req: NextApiRequest, res: NextApiResponse) =>
  new Promise((resolve, reject) => {
    limiter(req, res, (result: any) => {
      if (result instanceof Error) {
        return reject(result)
      }
      return resolve(result)
    })
  })

export async function POST(req: NextApiRequest, res: NextApiResponse) {
  try {
    await applyRateLimit(req, res)

    const { query } = await req.json()

    if (!process.env.TWITTER_BEARER_TOKEN) {
      throw new Error('TWITTER_BEARER_TOKEN is not set')
    }

    const response = await fetch(`https://api.twitter.com/2/tweets/search/recent?query=${encodeURIComponent(query)}`, {
      headers: {
        'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`,
      },
    })

    if (!response.ok) {
      if (response.status === 429) {
        return NextResponse.json({ error: 'Twitter API rate limit exceeded. Please try again later.' }, { status: 429 })
      }
      throw new Error(`Twitter API error! status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('X Posts Search error:', error)
    return NextResponse.json({ error: 'An error occurred during X posts search: ' + (error as Error).message }, { status: 500 })
  }
}

