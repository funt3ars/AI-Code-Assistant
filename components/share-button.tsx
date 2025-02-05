import { Share2 } from 'lucide-react'
import { Button } from './ui/button'

type ShareButtonProps = {
  result: string
}

export function ShareButton({ result }: ShareButtonProps) {
  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'AetherMind Search Result',
          text: result,
          url: window.location.href,
        })
      } catch (error) {
        console.error('Error sharing:', error)
      }
    } else {
      // Fallback for browsers that don't support the Web Share API
      alert('Sharing is not supported in this browser')
    }
  }

  return (
    <Button onClick={handleShare} variant="outline" size="sm">
      <Share2 className="mr-2 h-4 w-4" />
      Share
    </Button>
  )
}

