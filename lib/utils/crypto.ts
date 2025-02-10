export const isCryptoAvailable = () => {
    return typeof window !== 'undefined' &&
        window.crypto &&
        window.crypto.subtle;
} 