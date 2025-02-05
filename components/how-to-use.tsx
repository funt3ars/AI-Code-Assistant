import { Search, Zap, Brain, Sparkles } from "lucide-react"
import { motion } from "framer-motion"

const shineEffect = `
  @keyframes shine {
    to {
      background-position: 200% center;
    }
  }
  .shine-on-hover:hover {
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    background-size: 200% 100%;
    animation: shine 1s linear infinite;
  }
`

export function HowToUse() {
  const steps = [
    {
      icon: Search,
      title: "Enter Your Query",
      description: "Start by typing your Sui-related search query into the search box.",
    },
    {
      icon: Zap,
      title: "Instant Processing",
      description: "Our Sui-focused search engine quickly processes your query to find relevant results.",
    },
    {
      icon: Brain,
      title: "Intelligent Results",
      description:
        "Receive curated, relevant results that go beyond simple keyword matching, tailored for the Sui ecosystem.",
    },
    {
      icon: Sparkles,
      title: "Explore and Learn",
      description: "Browse through the search results to find the Sui-related information you need.",
    },
  ]

  return (
    <section className="text-center">
      <h2 className="text-3xl font-bold mb-6">How to Use Our Sui Web Search</h2>
      <p className="mb-8 text-lg text-muted-foreground">
        Experience a powerful web search engine designed to help you find Sui-related information quickly and
        efficiently.
      </p>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            className="bg-card rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 shine-on-hover"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{ position: "relative", overflow: "hidden" }}
          >
            <style jsx>{shineEffect}</style>
            <step.icon className="h-12 w-12 mx-auto mb-4 text-primary" />
            <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
            <p className="text-muted-foreground">{step.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  )
}

