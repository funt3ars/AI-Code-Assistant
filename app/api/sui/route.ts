import { SuiAgent } from '@/lib/sui-agent';
import { NextResponse } from 'next/server';

const suiAgent = SuiAgent.getInstance(process.env.ATOMASDK_BEARER_AUTH!);

export async function POST(req: Request) {
    try {
        const { prompt, context } = await req.json();
        const result = await suiAgent.processQuery(prompt, context);

        // Add transaction validation info if needed
        if (result.transaction) {
            result.requiresWallet = true;
        }

        return NextResponse.json(result);
    } catch (error: any) {
        return NextResponse.json(
            {
                reasoning: 'Error processing request',
                response: error.message,
                status: 'failure',
                query: '',
                errors: [error.message]
            },
            { status: 500 }
        );
    }
} 