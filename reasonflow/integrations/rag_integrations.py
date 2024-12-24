from typing import Dict, List, Optional, Any
from reasonchain.memory import SharedMemory
from reasonchain.rag.rag_main import query_vector_db
from reasonchain.rag.vector.add_to_vector_db import add_pdf_to_vector_db
from reasonflow.config.DBConfigLoader import DBConfigLoader
import os


class RAGIntegration:
    def __init__(
        self,
        db_path: str,
        db_type: str = "faiss",
        embedding_provider: str = "sentence_transformers",
        embedding_model: str = "all-MiniLM-L6-v2",
        config_file: str = "db_config.yaml",
        db_config: Optional[Dict] = None,
        use_gpu: bool = False,
        api_key: Optional[str] = None,
        shared_memory: Optional[SharedMemory] = None,
    ):
        """
        Initialize RAGIntegration with a Vector Database and shared memory.
        :param db_path: Path to the vector database.
        :param db_type: Type of vector database (e.g., "faiss").
        :param embedding_provider: Provider for embedding generation.
        :param embedding_model: Model name for embedding generation.
        :param db_config: Optional configuration for the database.
        :param use_gpu: Whether to use GPU for embedding generation.
        :param api_key: API key for embedding services if required.
        :param shared_memory: Shared memory instance for observability.
        """
        self.shared_memory = shared_memory or SharedMemory()
        self.vector_db_path = db_path
        self.vector_db_type = db_type
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model
        if db_config is None:
            # Load database configuration
            config_loader = DBConfigLoader(config_file)
            self.db_config = config_loader.get_config(db_type)
        else:
            self.db_config = db_config
        self.use_gpu = use_gpu
        self.api_key = api_key

    def add_documents(self, file_path: str) -> bool:
        """
        Add documents to the vector database.
        :param file_path: Path to the PDF file to add.
        :return: True if successful, False otherwise.
        """
        try:
            print(f"\nAttempting to add document: {file_path}")
            print(f"Vector DB Path: {self.vector_db_path}")
            print(f"Vector DB Type: {self.vector_db_type}")
            print(f"Embedding Model: {self.embedding_model}")

            # Log documents to shared memory
            if self.shared_memory:
                self.shared_memory.add_entry("file_path", file_path)

            # Add documents to the vector database
            result = add_pdf_to_vector_db(
                file_path=file_path,
                db_path=self.vector_db_path,
                db_type=self.vector_db_type,
                db_config=self.db_config,
                embedding_provider=self.embedding_provider,
                embedding_model=self.embedding_model,
                use_gpu=self.use_gpu,
                use_llama=False
            )

            # Check if index was created successfully
            if os.path.exists(self.vector_db_path):
                print(f"Vector database file exists at: {self.vector_db_path}")
                print(f"File size: {os.path.getsize(self.vector_db_path)} bytes")
                return True
            else:
                print(f"Vector database file not found at: {self.vector_db_path}")
                return False

        except Exception as e:
            print(f"Error adding document: {str(e)}")
            import traceback
            traceback.print_exc()
            if self.shared_memory:
                self.shared_memory.add_entry("add_documents_error", str(e))
            return False

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search the vector database for the given query."""
        try:
            print(f"\nSearching vector database...")
            print(f"Path: {self.vector_db_path}")
            print(f"Type: {self.vector_db_type}")
            print(f"Query: {query}")
            print(f"Top K: {top_k}")

            # Query the vector database
            results = query_vector_db(
                db_path=self.vector_db_path,
                db_type=self.vector_db_type,
                query=query,
                embedding_provider=self.embedding_provider,
                embedding_model=self.embedding_model,
                top_k=top_k,
                db_config=self.db_config
            )
            
            print(f"\nRaw results from vector DB:")
            print(results)

            # Format results
            formatted_results = []
            for entry in results:
                if isinstance(entry, tuple):
                    if len(entry) >= 2:
                        content, score = entry[:2]
                        metadata = entry[2] if len(entry) > 2 else None
                    else:
                        content = entry[0]
                        score = None
                        metadata = None
                else:
                    content = entry
                    score = None
                    metadata = None

                formatted_results.append({
                    "content": content,
                    "score": score,
                    "metadata": metadata
                })

            print(f"\nFormatted results:")
            for i, result in enumerate(formatted_results):
                print(f"\nResult {i+1}:")
                print(f"Content: {result['content'][:100]}...")
                print(f"Score: {result['score']}")

            return formatted_results

        except Exception as e:
            print(f"Error in search: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def configure_vector_db(self, db_path: str, db_type: str = "faiss"):
        """
        Configure the vector database path and type.
        :param db_path: Path to the vector database.
        :param db_type: Type of vector database (e.g., "faiss").
        """
        self.vector_db_path = db_path
        self.vector_db_type = db_type
