import { Twitter, DiscIcon as DiscordIcon, GithubIcon } from "lucide-react"
import { Button } from "./ui/button"

export function Socials() {
  return (
    <section className="text-center">
      <h2 className="text-3xl font-bold mb-6">Join Our Sui Community</h2>
      <div className="flex justify-center space-x-4">
        <Button variant="outline" size="icon" asChild>
          <a href="https://twitter.com/SuiNetwork" target="_blank" rel="noopener noreferrer">
            <Twitter className="h-5 w-5" />
            <span className="sr-only">Twitter</span>
          </a>
        </Button>
        <Button variant="outline" size="icon" asChild>
          <a href="https://discord.gg/sui" target="_blank" rel="noopener noreferrer">
            <DiscordIcon className="h-5 w-5" />
            <span className="sr-only">Discord</span>
          </a>
        </Button>
        <Button variant="outline" size="icon" asChild>
          <a href="https://github.com/MystenLabs" target="_blank" rel="noopener noreferrer">
            <GithubIcon className="h-5 w-5" />
            <span className="sr-only">GitHub</span>
          </a>
        </Button>
      </div>
    </section>
  )
}

