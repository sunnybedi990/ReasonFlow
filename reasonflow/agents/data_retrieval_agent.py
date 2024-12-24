from typing import Dict, List, Optional
import os
import logging

from reasonflow.integrations.rag_integrations import RAGIntegration
from reasonchain.memory import SharedMemory


class DataRetrievalAgent:
    def __init__(
        self,
        db_path: str,
        db_type: str = "faiss",
        embedding_provider: str = "sentence_transformers",
        embedding_model: str = "all-MiniLM-L6-v2",
        use_gpu: bool = False,
        api_key: Optional[str] = None,
        shared_memory: Optional[SharedMemory] = None,
    ):
        self.vector_store_type = db_type
        # Create new SharedMemory instance if none provided or if it's a string
        if shared_memory is None or isinstance(shared_memory, str):
            shared_memory = SharedMemory()
        
        self.shared_memory = shared_memory
        self.rag = RAGIntegration(
            db_path=db_path,
            db_type=db_type,
            embedding_provider=embedding_provider,
            embedding_model=embedding_model,
            use_gpu=use_gpu,
            api_key=api_key,
            shared_memory=self.shared_memory
        )

    def execute(self, query: str = "", top_k: int = 5, **kwargs) -> Dict:
        """
        Execute a search query against the vector database.
        :param query: Search query string
        :param top_k: Number of results to return
        :return: Dictionary containing results or error
        """
        try:
            logging.info(f"Executing search query: {query}")
            results = self.rag.search(query=query, top_k=top_k)
            
            # Format results for output
            formatted_output = "\n\n".join([
                f"Document {i+1}:\n{result['content']}"
                for i, result in enumerate(results)
            ])
            #print(formatted_output)
            
            if self.shared_memory:
                self.shared_memory.add_entry("search_results", results)
                
            return {
                "status": "success",
                "output": formatted_output,  # For LLM consumption
                "results": results,  # Raw results
                "metadata": {
                    "query": query,
                    "top_k": top_k,
                    "num_results": len(results)
                }
            }
        except Exception as e:
            error_msg = f"Error executing search: {str(e)}"
            logging.error(error_msg)
            if self.shared_memory:
                self.shared_memory.add_entry("search_error", error_msg)
            return {
                "status": "error",
                "message": error_msg
            }

    def index_document(self, document: Dict) -> bool:
        """
        Index a document in the vector database.
        :param document: A dictionary containing document data.
        :return: True if successful, False otherwise.
        """
        try:
            # Validate document format
            if not isinstance(document, Dict) or "content" not in document:
                raise ValueError("Invalid document format. Document must include 'content'.")

            logging.info(f"Indexing document in '{self.vector_store_type}' vector store")

            # Use RAGIntegration to add the document
            success = self.rag.add_documents([document])

            if not success:
                raise RuntimeError("Failed to index document.")

            # Log the operation in shared memory
            if self.shared_memory:
                self.shared_memory.store("last_indexed_document", document)

            return True
        except Exception as e:
            if self.shared_memory:
                self.shared_memory.store("index_document_error", str(e))
            logging.error(f"Error indexing document: {str(e)}")
            return False
