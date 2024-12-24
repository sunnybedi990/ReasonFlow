import React, { useState } from 'react';
import { AgentConfig } from '../types';
import { ReasonFlowSDK } from '../js_sdk';

interface AgentBuilderProps {
    sdk: ReasonFlowSDK;
    onAgentCreated: (agentId: string) => void;
}

export const AgentBuilder: React.FC<AgentBuilderProps> = ({ sdk, onAgentCreated }) => {
    const [agentConfig, setAgentConfig] = useState<AgentConfig>({
        type: 'llm',
        name: '',
        description: '',
        config: {}
    });
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const agentId = await sdk.createAgent(agentConfig);
            onAgentCreated(agentId);
        } catch (error) {
            console.error('Error creating agent:', error);
        }
    };
    
    return (
        <div className="p-4 bg-white rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">Create Agent</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">
                        Agent Type
                    </label>
                    <select
                        value={agentConfig.type}
                        onChange={(e) => setAgentConfig({...agentConfig, type: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    >
                        <option value="llm">LLM Agent</option>
                        <option value="data_retrieval">Data Retrieval Agent</option>
                        <option value="custom_task">Custom Task Agent</option>
                        <option value="api_connector">API Connector Agent</option>
                    </select>
                </div>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700">
                        Name
                    </label>
                    <input
                        type="text"
                        value={agentConfig.name}
                        onChange={(e) => setAgentConfig({...agentConfig, name: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                </div>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700">
                        Description
                    </label>
                    <textarea
                        value={agentConfig.description}
                        onChange={(e) => setAgentConfig({...agentConfig, description: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                </div>
                
                <button
                    type="submit"
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                    Create Agent
                </button>
            </form>
        </div>
    );
}; 