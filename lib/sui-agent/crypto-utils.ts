import { blake2b } from 'blakejs';
import { CryptoUtils } from '../atoma-sdk-patch/crypto_utils';

/**
 * Calculate a cryptographic hash of the input data using BLAKE2b
 * @param data The input data to be hashed
 * @returns A 32-byte hash
 */
export function calculateHash(data: Uint8Array): Uint8Array {
    return blake2b(data, undefined, 32);
}

/**
 * Convert a hex string to Uint8Array
 * @param hex The hex string to convert
 * @returns Uint8Array
 */
export function hexToBytes(hex: string): Uint8Array {
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < hex.length; i += 2) {
        bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
    }
    return bytes;
}

/**
 * Convert Uint8Array to hex string
 * @param bytes The bytes to convert
 * @returns hex string
 */
export function bytesToHex(bytes: Uint8Array): string {
    return Array.from(bytes)
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}

export const generateNonce = async (): Promise<string> => {
    const timestamp = Date.now().toString();
    return await CryptoUtils.hash(timestamp);
};

export const validateSignature = async (
    message: string,
    signature: string,
    publicKey: string
): Promise<boolean> => {
    try {
        // Basic validation for now
        return message.length > 0 && signature.length > 0 && publicKey.length > 0;
    } catch (error) {
        console.error('Signature validation error:', error);
        return false;
    }
}; 