import React, { useState } from 'react';
import ReactFlow, { 
    Node, 
    Edge, 
    Controls, 
    Background,
    useNodesState,
    useEdgesState
} from 'reactflow';
import { ReasonFlowSDK } from '../js_sdk';

interface WorkflowBuilderProps {
    sdk: ReasonFlowSDK;
    onWorkflowCreated: (workflowId: string) => void;
}

export const WorkflowBuilder: React.FC<WorkflowBuilderProps> = ({ sdk, onWorkflowCreated }) => {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);
    
    const onConnect = (params: any) => {
        setEdges((eds) => [...eds, params]);
    };
    
    const onSave = async () => {
        try {
            const workflowConfig = {
                tasks: nodes.reduce((acc: any, node) => {
                    acc[node.id] = {
                        type: node.type,
                        config: node.data
                    };
                    return acc;
                }, {}),
                dependencies: edges.map(edge => ({
                    from: edge.source,
                    to: edge.target
                }))
            };
            
            const workflowId = await sdk.createWorkflow(workflowConfig);
            onWorkflowCreated(workflowId);
        } catch (error) {
            console.error('Error saving workflow:', error);
        }
    };
    
    const onDragOver = (event: React.DragEvent) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    };
    
    const onDrop = (event: React.DragEvent) => {
        event.preventDefault();
        
        const type = event.dataTransfer.getData('application/reasonflow-node');
        const position = {
            x: event.clientX,
            y: event.clientY
        };
        
        const newNode: Node = {
            id: `${type}-${nodes.length + 1}`,
            type,
            position,
            data: { label: `${type} node` }
        };
        
        setNodes((nds) => [...nds, newNode]);
    };
    
    return (
        <div className="h-screen w-full">
            <div className="h-full">
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onDrop={onDrop}
                    onDragOver={onDragOver}
                >
                    <Background />
                    <Controls />
                </ReactFlow>
            </div>
            
            <div className="absolute bottom-4 right-4">
                <button
                    onClick={onSave}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                    Save Workflow
                </button>
            </div>
        </div>
    );
}; 