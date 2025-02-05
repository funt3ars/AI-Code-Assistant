import { Card } from './ui/card'

type SearchResultsProps = {
  results: any[]
}

export function SearchResults({ results }: SearchResultsProps) {
  if (!results || results.length === 0) return null

  return (
    <Card className="p-6 mt-6 w-full max-w-3xl">
      <h3 className="text-xl font-semibold mb-4">Search Results</h3>
      <ul className="space-y-4">
        {results.map((result, index) => (
          <li key={index} className="border-b pb-4 last:border-b-0">
            <a href={result.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
              {result.title}
            </a>
            <p className="text-sm text-gray-600">{result.snippet}</p>
          </li>
        ))}
      </ul>
    </Card>
  )
}

