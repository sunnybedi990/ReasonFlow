# ReasonFlow

A powerful workflow orchestration framework for LLM applications with built-in RAG support, agent management, and multi-modal processing capabilities.

## Features

### Core Components
- **Workflow Orchestration**
  - DAG-based workflow execution
  - Dynamic task scheduling with priority management
  - State persistence and versioning
  - Real-time status tracking
  - Error handling and retry mechanisms

- **Agent System**
  - Multiple LLM providers (OpenAI, Groq, Ollama, Anthropic)
  - RAG integration with vector databases
  - Custom task execution
  - API connector agents
  - Dynamic agent creation and configuration

- **Document Management**
  - PDF processing and text extraction
  - Vector database integration (FAISS)
  - Document versioning
  - Full-text search capabilities
  - Multiple storage backends (S3, MinIO)

### Integrations
- **LLM Providers**
  - OpenAI (gpt-4o, gpt-4o-mini)
  - Groq (gemma, llama)
  - Ollama (local models)
  - Anthropic (claude)
  - ReasonChain

- **Vector Databases**
  - FAISS (CPU/GPU)
  - Pinecone
  - Milvus
  - Qdrant
  - Weaviate

- **Storage Solutions**
  - Firebase
  - AWS S3
  - MinIO
  - Local storage

## Installation

### Basic Installation (CPU)
```bash
pip install reasonflow
```

### GPU Support (Recommended for large-scale deployments)
```bash
# Create conda environment
conda create -n reasonflow python=3.10
conda activate reasonflow

# Install FAISS GPU
conda install -c conda-forge faiss-gpu

# Install ReasonFlow
pip install reasonflow
```

### Development Installation
```bash
git clone https://github.com/yourusername/reasonflow.git
cd reasonflow
pip install -e ".[dev]"
```

## Quick Start

### 1. Configure Environment
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
VECTOR_DB_PATH=vector_dbs/
```

### 2. Create a Simple Workflow
```python
from reasonflow.orchestrator.workflow_builder import WorkflowBuilder
from reasonflow.integrations.llm_integrations import LLMIntegration
import os

# Initialize components
workflow_builder = WorkflowBuilder()

# Create LLM agent
llm = LLMIntegration(
    provider="openai",
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define workflow
workflow_config = {
    "tasks": {
        "analyze": {
            "type": "llm",
            "config": {
                "agent": llm,
                "params": {"prompt": "Analyze this text"}
            }
        }
    }
}

# Create and execute workflow
workflow_id = workflow_builder.create_workflow(workflow_config)
results = workflow_builder.execute_workflow(workflow_id)
```

### 3. RAG Integration Example
```python
from reasonflow.integrations.rag_integrations import RAGIntegration

# Initialize RAG
rag = RAGIntegration(
    db_path="my_vectors.index",
    db_type="faiss",
    embedding_model="all-MiniLM-L6-v2"
)

# Add documents
rag.add_documents("document.pdf")

# Search
results = rag.search("What is the revenue growth?", top_k=5)
```

## Project Structure
```
reasonflow/
├── agents/                 # Agent implementations
├── config/                 # Configuration files
├── integrations/          # External service integrations
├── orchestrator/          # Workflow management
├── persistence/           # State and data persistence
├── sdk/                   # Python and JavaScript SDKs
└── tasks/                 # Task management
```

## Development

### Running Tests
```bash
pytest tests/
```

### Building Package
```bash
python build.py
```

### Code Style
```bash
black reasonflow/
isort reasonflow/
flake8 reasonflow/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License - see [LICENSE](LICENSE) for details.

## Support
- Documentation: [docs.reasonflow.ai](https://docs.reasonflow.ai)
- Issues: [GitHub Issues](https://github.com/yourusername/reasonflow/issues)
- Discord: [Join our community](https://discord.gg/reasonflow)