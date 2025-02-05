import { SuiSentimentAnalyzer } from '@/lib/twitter-sentiment'

const analyzer = new SuiSentimentAnalyzer()

export async function GET() {
  try {
    const data = await analyzer.updateSentimentData()
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Failed to fetch sentiment data' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
} 