import { NextResponse } from 'next/server';

export async function GET() {
    try {
        // Mock data for now - replace with real API calls
        const marketData = {
            suiPrice: 3.14,
            marketCap: 2500000000,
            volume24h: 150000000,
            priceChange24h: 5.23,
            marketSentiment: {
                score: 75,
                trend: 'bullish' as const,
                signals: [
                    'increasing buy pressure on major exchanges',
                    'positive social sentiment metrics',
                    'growing developer activity'
                ]
            }
        };

        return NextResponse.json(marketData);
    } catch (error: any) {
        return NextResponse.json(
            { error: error.message },
            { status: 500 }
        );
    }
} 