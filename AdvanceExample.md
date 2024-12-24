## Advanced Example: Financial Analysis Workflow

This example demonstrates a multi-step workflow that analyzes financial documents using RAG and multiple LLM providers.

```python
from reasonflow.orchestrator.workflow_builder import WorkflowBuilder
from reasonflow.integrations.llm_integrations import LLMIntegration
from reasonflow.integrations.rag_integrations import RAGIntegration
from reasonchain.memory import SharedMemory
import os

# Initialize components
shared_memory = SharedMemory()
workflow_builder = WorkflowBuilder()

# Set up RAG for document processing
rag_integration = RAGIntegration(
    db_path="vector_db_tesla.index",
    db_type="faiss",
    embedding_model="all-MiniLM-L6-v2",
    shared_memory=shared_memory
)
rag_integration.add_documents("financial_report.pdf")

# Create LLM agents with different providers
llm_extractor = LLMIntegration(
    provider="openai", 
    model="gpt-4o", 
    api_key=os.getenv("OPENAI_API_KEY")
)
llm_analyzer = LLMIntegration(
    provider="ollama", 
    model="llama3.1:latest"
)
llm_summarizer = LLMIntegration(
    provider="groq", 
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY")
)

# Define workflow configuration
workflow_config = {
    "tasks": {
        "ingest-document": {
            "type": "data_retrieval",
            "config": {
                "agent_config": {
                    "db_path": "vector_db_tesla.index",
                    "db_type": "faiss",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "use_gpu": True,
                    "shared_memory": shared_memory
                },
                "params": {
                    "query": "Retrieve Tesla financial data",
                    "top_k": 20
                }
            }
        },
        "extract-highlights": {
            "type": "llm",
            "config": {
                "agent": llm_extractor,
                "params": {
                    "prompt": """Extract key financial highlights from the following data: 
                    {{ingest-document.output}}
                    
                    Format your response as a bulleted list of the most important financial metrics and findings."""
                }
            }
        },
        "analyze-trends": {
            "type": "llm",
            "config": {
                "agent": llm_analyzer,
                "params": {
                    "prompt": """Analyze the financial trends from these highlights:
                    {{extract-highlights.output}}
                    
                    Focus on:
                    - Revenue growth trends
                    - Profitability metrics
                    - Cash flow patterns
                    - Key business segments performance"""
                }
            }
        },
        "summarize-insights": {
            "type": "llm",
            "config": {
                "agent": llm_summarizer,
                "params": {
                    "prompt": """Provide a concise executive summary of these financial trends:
                    {{analyze-trends.output}}
                    
                    Include:
                    1. Overall financial health
                    2. Key growth indicators
                    3. Risk factors
                    4. Future outlook"""
                }
            }
        }
    },
    "dependencies": [
        {"from": "ingest-document", "to": "extract-highlights"},
        {"from": "extract-highlights", "to": "analyze-trends"},
        {"from": "analyze-trends", "to": "summarize-insights"}
    ]
}

# Create and execute workflow
workflow_id = workflow_builder.create_workflow(workflow_config)
results = workflow_builder.execute_workflow(workflow_id)

# Print results
for task_id, result in results.items():
    print(f"\nTask {task_id}:")
    print(result)
```

This workflow:
1. Ingests financial documents using RAG
2. Extracts key financial highlights using OpenAI
3. Analyzes trends using Ollama's local LLM
4. Generates a summary using Groq's fast inference
5. Demonstrates task dependencies and data flow
6. Shows integration of multiple LLM providers
7. Uses shared memory for state management