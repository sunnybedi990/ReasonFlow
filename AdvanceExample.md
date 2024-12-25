## Advanced Example: Financial Analysis Workflow

This example demonstrates a multi-step workflow that analyzes financial documents using RAG and multiple LLM providers.

# ReasonFlow Tracking System

## Overview
ReasonFlow provides two tracking options:
1. Basic Tracking (Default)
2. Advanced Tracking (via ReasonTrack)

## Basic Tracking
Built-in tracking system for essential monitoring:

```python
from reasonflow import WorkflowEngine

# Default basic tracking
engine = WorkflowEngine()
```

Features:
- Task status tracking
- Workflow state persistence
- Basic error logging
- JSON-based storage

## Advanced Tracking (ReasonTrack)
Enterprise-grade tracking with comprehensive monitoring:

```python
from reasonflow import WorkflowEngine

config = {
    "event_backend": {
        "type": "kafka",
        "config": {
            "broker_url": "localhost:9092",
            "topic_prefix": "reasonflow_"
        }
    },
    "metrics_backend": {
        "type": "prometheus",
        "config": {
            "pushgateway_url": "localhost:9091",
            "job_name": "reasonflow"
        }
    },
    "alert_config": {
        "storage_path": "alerts",
        "retention_days": 30,
        "backends": {
            "slack": {"webhook_url": "your_webhook_url"},
            "email": {
                "smtp_host": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "alerts@example.com",
                "password": "your_password"
            }
        }
    },
    "state_config": {
        "storage_path": "workflow_states"
    }
}

# Advanced tracking with ReasonTrack
engine = WorkflowEngine(tracker_type="reasontrack", tracker_config=config)
```

Features:
- Real-time event streaming
- Comprehensive metrics collection
- Distributed tracing
- Alert management
- Multiple backend support
- State versioning

## Comparison

| Feature              | Basic Tracking | Advanced Tracking |
|---------------------|----------------|------------------|
| Task Status         | ✅             | ✅               |
| Workflow State      | ✅             | ✅               |
| Error Logging       | ✅             | ✅               |
| Real-time Events    | ❌             | ✅               |
| Metrics Collection  | ❌             | ✅               |
| Alert Management    | ❌             | ✅               |
| Multiple Backends   | ❌             | ✅               |
| State Versioning    | ❌             | ✅               |
| Setup Complexity    | Simple         | Advanced         |

## Configuration Guide
[Detailed configuration options and examples...]

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