import os
import uuid
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from chromadb import Client, Settings

KNOWLEDGE_BASE_PATH = os.path.join('..', 'Task2', 'knowledge_base')
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
CHROMA_PERSIST_DIR = './.chroma'

start_time = time.time()

model = SentenceTransformer(MODEL_NAME)

chroma_client = Client(Settings(is_persistent=True, persist_directory=CHROMA_PERSIST_DIR))
collection_name = "knowledge_index"
collection = chroma_client.get_or_create_collection(name=collection_name)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


all_chunks = []

for filename in sorted(os.listdir(KNOWLEDGE_BASE_PATH)):
    filepath = os.path.join(KNOWLEDGE_BASE_PATH, filename)
    if os.path.isfile(filepath) and filename.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            text_content = f.read()

        chunks = text_splitter.split_text(text_content)

        metadatas = []
        embeddings = []
        ids = []

        for idx, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            source_metadata = {
                "source": filename,
                "source_path": filepath,
                "chunk_index": idx,
                "tag": filename.replace('.txt', '').replace('_', ' ').lower()
            }

            embedding = model.encode(chunk)

            metadatas.append(source_metadata)
            embeddings.append(embedding)
            ids.append(chunk_id)

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        all_chunks.extend(chunks)
        print(f"Обработано {len(chunks)} чанков из файла: {filename}")

end_time = time.time()
total_chunks = len(all_chunks)

print(f"\nОбработка завершена за {end_time - start_time:.2f} секунд")
print(f"Общее число чанков в базе: {total_chunks}")
print(f"Название коллекции: {collection_name}")
print(f"Используемая модель эмбеддингов: {MODEL_NAME}")
print(f"Путь к базе данных: {CHROMA_PERSIST_DIR}")

# Запрос к индексу

query_text = "Terminator"
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