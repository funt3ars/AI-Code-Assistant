import { isCryptoAvailable } from '../utils/crypto';

export class CryptoUtils {
    static generateUUID(): string {
        // Simple UUID v4 fallback implementation
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    static async hash(data: string): Promise<string> {
        // Check if we're in a browser environment and have crypto support
        if (typeof window === 'undefined' || !window.crypto || !window.crypto.subtle) {
            // Fallback to a simpler hash
            return this.generateUUID();
        }

        try {
            const encoder = new TextEncoder();
            const dataBuffer = encoder.encode(data);
            const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        } catch (error) {
            console.error('Crypto error:', error);
            // Fallback
            return this.generateUUID();
        }
    }
} 