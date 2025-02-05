export const isEthereumAvailable = () => {
  return typeof window !== 'undefined' && typeof window.ethereum !== 'undefined'
}

