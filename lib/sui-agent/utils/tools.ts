export interface ToolParameter {
    name: string;
    type: string;
    description: string;
    required: boolean;
}

export interface Tool {
    name: string;
    description: string;
    parameters: ToolParameter[];
    process: (...args: (string | number | boolean | bigint)[]) => Promise<string>;
}

export class Tools {
    private tools: Map<string, Tool> = new Map();

    constructor(private bearerToken: string) { }

    registerTool(
        name: string,
        description: string,
        parameters: ToolParameter[],
        process: (...args: any[]) => Promise<string>
    ) {
        this.tools.set(name, {
            name,
            description,
            parameters,
            process
        });
    }

    getTool(name: string): Tool | undefined {
        return this.tools.get(name);
    }

    getAllTools(): Tool[] {
        return Array.from(this.tools.values());
    }

    async selectAppropriateTool(prompt: string) {
        const promptLower = prompt.toLowerCase();
        console.log('Checking prompt:', promptLower); // Debug log

        // More specific tool matching
        if (promptLower.match(/balance|portfolio|holdings/)) {
            const address = prompt.match(/0x[a-fA-F0-9]+/)?.[0];
            if (address) {
                console.log('Found balance query for:', address); // Debug log
                return {
                    selected_tool: 'get_wallet_balance',
                    tool_arguments: [address],
                    success: true
                };
            }
        }

        if (promptLower.match(/transfer|send|pay/)) {
            const matches = prompt.match(/(?:transfer|send)\s+(\d+)\s+(\w+)\s+to\s+(0x[a-fA-F0-9]+)/i);
            if (matches) {
                console.log('Found transfer request:', matches); // Debug log
                return {
                    selected_tool: 'prepare_transfer',
                    tool_arguments: [matches[3], matches[1], matches[2]],
                    success: true
                };
            }
        }

        console.log('No matching tool found'); // Debug log
        return {
            selected_tool: null,
            tool_arguments: [],
            success: false
        };
    }

    async processQuery(
        prompt: string,
        toolName: string,
        args: (string | number | boolean | bigint)[]
    ): Promise<string> {
        const tool = this.tools.get(toolName);
        if (!tool) {
            throw new Error(`Tool ${toolName} not found`);
        }
        return await tool.process(...args);
    }
} 