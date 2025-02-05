import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'

type ProviderSelectProps = {
  value: string
  onChange: (value: string) => void
}

export function ProviderSelect({ value, onChange }: ProviderSelectProps) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-[200px]">
        <SelectValue placeholder="Select AI Provider" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="openai">OpenAI</SelectItem>
        <SelectItem value="azure">Azure OpenAI</SelectItem>
        <SelectItem value="anthropic">Anthropic</SelectItem>
        <SelectItem value="google">Google Generative AI</SelectItem>
      </SelectContent>
    </Select>
  )
}

