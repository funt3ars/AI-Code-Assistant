import { StreamingTextResponse, LangChainStream } from 'ai'
import Anthropic from '@anthropic-ai/sdk'

export const runtime = 'edge'

export async function POST(req: Request) {
  try {
    const { messages } = await req.json()

    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    })

    const stream = await anthropic.completions.create({
      model: 'claude-2',
      max_tokens_to_sample: 300,
      prompt: `Human: You are Aegir, an AI assistant specialized in the Sui ecosystem. Please provide information and answers related to the following query: ${messages[messages.length - 1].content}`,
    })

    const streamResponse = new LangChainStream(stream)

    return new StreamingTextResponse(streamResponse)
  } catch (error) {
    console.error('Error:', error)
    return new Response('Error', { status: 500 })
  }
}

