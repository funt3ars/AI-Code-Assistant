import { Button } from './ui/button'
import { ScrollArea } from './ui/scroll-area'

type SearchHistoryProps = {
  history: string[]
  onSelectHistory: (query: string) => void
}

export function SearchHistory({ history, onSelectHistory }: SearchHistoryProps) {
  return (
    <ScrollArea className="h-[200px] w-full max-w-2xl mx-auto">
      <div className="space-y-2 p-2">
        {history.map((query, index) => (
          <Button
            key={index}
            variant="ghost"
            className="w-full justify-start text-left"
            onClick={() => onSelectHistory(query)}
          >
            {query}
          </Button>
        ))}
      </div>
    </ScrollArea>
  )
}

