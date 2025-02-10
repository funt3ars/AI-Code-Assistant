export interface AgentResponse {
    reasoning: string;
    response: string;
    status: 'success' | 'failure';
    query: string;
    errors: string[];
}

export interface ToolDefinition {
    name: string;
    description: string;
    parameters: {
        name: string;
        type: string;
        description: string;
        required: boolean;
    }[];
    process: Function;
} 