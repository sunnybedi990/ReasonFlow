from ..agents.data_retrieval_agent import DataRetrievalAgent

# Initialize the Data Retrieval Agent
agent = DataRetrievalAgent(
    db_path="vector_db_tesla.index",
    db_type="faiss",
    embedding_provider="sentence_transformers",
    embedding_model="all-MiniLM-L6-v2",
    use_gpu=True,
)

# Index a document
document = {"content": "Tesla's Q-10 financial highlights"}
if agent.index_document(document):
    print("Document indexed successfully.")

# Search the database
query = "What are Tesla's financial highlights?"
results = agent.search(query=query, top_k=5)
print("Search Results:", results)
