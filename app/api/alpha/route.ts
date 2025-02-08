import { NextResponse } from 'next/server';
import { SuiAgent } from '@/lib/sui-agent';

const suiAgent = SuiAgent.getInstance(process.env.ATOMASDK_BEARER_AUTH!);

export async function POST(req: Request) {
    try {
        const { context } = await req.json();

        // Get market analysis from Atlas
        const atlasResponse = await suiAgent.processQuery(
            "Analyze current market conditions and provide trading insights",
            {
                role: "ATLAS_PRIME",
                context: {
                    marketData: context.marketData,
                    technicalIndicators: context.technicalIndicators,
                    sentiment: context.sentiment
                }
            }
        );

        // Get Midas Rex's response to Atlas's analysis
        const midasResponse = await suiAgent.processQuery(
            `Respond to this analysis: ${atlasResponse.response}`,
            {
                role: "MIDAS_REX",
                context: {
                    portfolioData: context.portfolioData,
                    riskProfile: context.riskProfile
                }
            }
        );

        return NextResponse.json({
            atlas: atlasResponse.response,
            midas: midasResponse.response
        });

    } catch (error: any) {
        return NextResponse.json(
            { error: error.message },
            { status: 500 }
        );
    }
} 