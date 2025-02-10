import { getFullnodeUrl } from '@mysten/sui.js/client';

export const NETWORK_CONFIG = {
    mainnet: {
        url: 'https://fullnode.mainnet.sui.io',
        faucet: undefined,
        aftermathApi: 'https://api.aftermath.finance/v1',
    },
    testnet: {
        url: 'https://fullnode.testnet.sui.io',
        faucet: 'https://faucet.testnet.sui.io/gas',
        aftermathApi: 'https://testnet-api.aftermath.finance/v1',
    }
} as const;

export type NetworkType = keyof typeof NETWORK_CONFIG;

export const DEFAULT_NETWORK: NetworkType = 'mainnet'; 