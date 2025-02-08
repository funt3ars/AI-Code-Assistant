/**
 * Prompt template for formatting final responses
 */
export const FINAL_ANSWER_PROMPT = `Format the response in this structure:
[{
    "reasoning": string,    // Keep under 50 chars
    "response": string,     // DO NOT prefix with "Midas Rex: "
    "status": "success" | "failure",
    "query": string,        // original query
    "errors": string[]      // brief error messages
}]

IMPORTANT:
- Keep responses concise and clear
- Do not add any name prefix to responses
- One piece of information per message
- Use a professional yet friendly tone
- Skip redundant transaction status messages
- Focus on providing value beyond UI notifications`; 