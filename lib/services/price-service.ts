import { SuiClient } from '@mysten/sui.js/client';
import { SuiObjectResponse, SuiMoveObject } from '@mysten/sui.js/client';

interface PoolData {
    coinInReserve: bigint;
    coinOutReserve: bigint;
    decimalsIn: number;
    decimalsOut: number;
}

interface PoolError {
    error: {
        code: string;
        message?: string;
    };
}

interface CoinGeckoPrice {
    [key: string]: {
        usd: number;
        last_updated_at: number;
    };
}

export class PriceService {
    private client: SuiClient;
    private readonly COINGECKO_API = 'https://api.coingecko.com/api/v3';
    private readonly COIN_IDS = {
        // Major cryptocurrencies
        BTC: 'bitcoin',
        ETH: 'ethereum',

        // Sui ecosystem
        SUI: 'sui',
        CETUS: 'cetus',
        SUIA: 'suia',
        MOVE: 'move-network',
        BUCK: 'bucketus',
        NAV: 'nav-coin',
        USDC: 'usd-coin',
        USDT: 'tether',
        WETH: 'weth',
        TURBOS: 'turbos-finance',
        NAVI: 'navi-protocol',
        TOCE: 'tocen',
        SCAL: 'scallop',
        HADES: 'hades',
        SUIP: 'sui-protocol',
        COMETA: 'cometa-finance',
    } as const;

    // Cache prices for 1 minute
    private priceCache: Map<string, { price: number; timestamp: number }> = new Map();
    private readonly CACHE_DURATION = 60 * 1000; // 1 minute in milliseconds

    // Pools and coin types
    private readonly POOLS = {
        SUI_USDC: '0x5eb2dfcdd1b15d2021328258f6d5ec081e9a0cdcfa9e13a0eaeb9b5f7505ca78',
    } as const;

    // Token decimals (verified from chain)
    private readonly DECIMALS = {
        SUI: 9,
        USDC: 6,  // Verified from USDC contract
    } as const;

    constructor() {
        this.client = new SuiClient({
            url: 'https://fullnode.mainnet.sui.io'
        });
    }

    /**
     * Get SUI price from CoinGecko
     */
    async getSuiPrice(): Promise<number> {
        try {
            return await this.getTokenPrice('SUI');
        } catch (error) {
            console.error('Error fetching SUI price:', error);
            throw error;
        }
    }

    /**
     * Get token price for any supported token
     */
    async getTokenPrice(symbol: string): Promise<number> {
        try {
            // Validate input
            if (!symbol) {
                throw new Error('Token symbol is required');
            }

            console.log('Getting price for symbol:', symbol); // Debug log

            // Normalize symbol to uppercase
            const normalizedSymbol = symbol.toUpperCase();

            // Check cache first
            const cached = this.priceCache.get(normalizedSymbol);
            if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
                return cached.price;
            }

            // Convert symbol to CoinGecko ID
            const coinId = this.COIN_IDS[normalizedSymbol as keyof typeof this.COIN_IDS];
            if (!coinId) {
                throw new Error(`Unsupported token: ${normalizedSymbol}`);
            }

            // Fetch price from CoinGecko
            const response = await fetch(
                `${this.COINGECKO_API}/simple/price?ids=${coinId}&vs_currencies=usd&include_last_updated_at=true`
            );

            if (!response.ok) {
                throw new Error(`CoinGecko API error: ${response.status} ${response.statusText}`);
            }

            const data: CoinGeckoPrice = await response.json();

            if (!data[coinId]?.usd) {
                throw new Error(`No price data for ${normalizedSymbol}`);
            }

            const price = data[coinId].usd;

            // Update cache
            this.priceCache.set(normalizedSymbol, {
                price,
                timestamp: Date.now()
            });

            return price;
        } catch (error) {
            console.error('Price service error:', {
                symbol,
                error: error instanceof Error ? error.message : String(error)
            });
            throw error;
        }
    }

    /**
     * Get pool data from DEX
     */
    private async getPoolData(poolAddress: string): Promise<PoolData> {
        try {
            const poolObject = await this.client.getObject({
                id: poolAddress,
                options: { showContent: true }
            });

            // Debug log to verify structure
            console.log('Fetched pool object:', JSON.stringify(poolObject, null, 2));

            // Check for error in response
            if ('error' in poolObject && poolObject.error) {
                const poolError = poolObject as PoolError;
                throw new Error(`Pool error: ${poolError.error.code}${poolError.error.message ? ` - ${poolError.error.message}` : ''}`);
            }

            if (!poolObject.data?.content) {
                throw new Error('Pool data not found');
            }

            // Type guard to ensure we have a MoveObject
            if (!('dataType' in poolObject.data.content) ||
                poolObject.data.content.dataType !== 'moveObject') {
                throw new Error('Invalid pool data type');
            }

            const fields = (poolObject.data.content as SuiMoveObject).fields;

            // Ensure the fields exist and have the correct type
            if (typeof fields !== 'object' ||
                !('sui_reserve' in fields) ||
                !('usdc_reserve' in fields)) {
                throw new Error('Invalid pool data structure');
            }

            return {
                coinInReserve: BigInt(fields.sui_reserve as string),
                coinOutReserve: BigInt(fields.usdc_reserve as string),
                decimalsIn: this.DECIMALS.SUI,
                decimalsOut: this.DECIMALS.USDC
            };
        } catch (error) {
            console.error('Error fetching pool data:', error);
            throw error;
        }
    }
}

// Updated test function
async function testPriceService() {
    const priceService = new PriceService();

    console.log('Starting price service tests...');

    try {
        // Test major cryptocurrencies
        console.log('\nTest 1: Fetching major crypto prices...');
        const btcPrice = await priceService.getTokenPrice('BTC');
        const ethPrice = await priceService.getTokenPrice('ETH');
        console.log('BTC Price:', btcPrice, 'USD');
        console.log('ETH Price:', ethPrice, 'USD');

        // Test Sui ecosystem tokens
        console.log('\nTest 2: Fetching Sui ecosystem prices...');
        const suiPrice = await priceService.getTokenPrice('SUI');
        const cetusPrice = await priceService.getTokenPrice('CETUS');
        const usdcPrice = await priceService.getTokenPrice('USDC');
        console.log('SUI Price:', suiPrice, 'USD');
        console.log('CETUS Price:', cetusPrice, 'USD');
        console.log('USDC Price:', usdcPrice, 'USD');

        // Test caching
        console.log('\nTest 3: Testing cache...');
        const cachedPrice = await priceService.getTokenPrice('BTC');
        console.log('Cached BTC Price:', cachedPrice, 'USD (should be instant)');

        // Test error handling
        console.log('\nTest 4: Testing error handling...');
        try {
            await priceService.getTokenPrice('INVALID');
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.log('Expected error caught:', error.message);
            } else {
                console.log('Expected error caught:', String(error));
            }
        }

    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error('Test failed:', error.message);
        } else {
            console.error('Test failed:', String(error));
        }
    }
}

// Run the tests
if (require.main === module) {
    testPriceService().then(() => process.exit(0));
} 