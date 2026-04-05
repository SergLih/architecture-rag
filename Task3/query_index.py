import os
import time
from sentence_transformers import SentenceTransformer
from chromadb import Client, Settings

KNOWLEDGE_BASE_PATH = os.path.join('.', 'Task4-5', 'knowledge_base')
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
CHROMA_PERSIST_DIR = os.path.join('.', 'Task4-5', '.chroma')

model = SentenceTransformer(MODEL_NAME)

chroma_client = Client(Settings(is_persistent=True, persist_directory=CHROMA_PERSIST_DIR))
collection_name = "knowledge_index"
collection = chroma_client.get_or_create_collection(name=collection_name)

# query_text = "Terminator"
query_text = "Суперпароль root"
query_embedding = model.encode(query_text)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

print(f"\nРезультаты поиска по запросу '{query_text}':")
for doc, score in zip(results['documents'][0], results['distances'][0]):
    print(f"\nИсточник: {results['metadatas'][0][0]['source']}")
    print(f"\nРезультат ответа (score: {score:.4f}):")
    print(doc[:500] + ('...' if len(doc) > 500 else ''))