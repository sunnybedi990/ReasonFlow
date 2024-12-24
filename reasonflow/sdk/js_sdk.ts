import axios, { AxiosInstance } from 'axios';
import { WorkflowConfig, AgentConfig, DocumentMetadata } from './types';

export class ReasonFlowSDK {
    private client: AxiosInstance;

    constructor(apiKey: string, baseURL: string = process.env.REASONFLOW_BASE_URL || 'https://api.reasonflow.ai') {
        this.client = axios.create({
            baseURL,
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
    }

    private async handleRequest<T>(request: () => Promise<T>): Promise<T> {
        try {
            return await request();
        } catch (error: any) {
            console.error('SDK Request Error:', error.response?.data || error.message);
            throw new Error(error.response?.data?.error || 'An unexpected error occurred');
        }
    }

    async createWorkflow(config: WorkflowConfig): Promise<string> {
        return this.handleRequest(async () => {
            const response = await this.client.post('/workflows', config);
            return response.data.workflow_id;
        });
    }

    async executeWorkflow(workflowId: string): Promise<any> {
        return this.handleRequest(async () => {
            const response = await this.client.post(`/workflows/${workflowId}/execute`);
            return response.data;
        });
    }

    async createAgent(config: AgentConfig): Promise<string> {
        return this.handleRequest(async () => {
            const response = await this.client.post('/agents', config);
            return response.data.agent_id;
        });
    }

    async uploadDocument(file: File, metadata: DocumentMetadata): Promise<string> {
        return this.handleRequest(async () => {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('metadata', JSON.stringify(metadata));
            const response = await this.client.post('/documents/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            return response.data.document_id;
        });
    }

    async searchDocuments(query: string, limit: number = 10): Promise<any[]> {
        return this.handleRequest(async () => {
            const response = await this.client.get('/documents/search', {
                params: { query, limit }
            });
            return response.data.results;
        });
    }
}
