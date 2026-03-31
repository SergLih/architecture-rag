from chromadb import Client, Settings
from sentence_transformers import SentenceTransformer
from jinja2 import Template
import os
import requests
import time

CHROMA_PERSIST_DIR_PATH = os.path.join('..', 'Task3', '.chroma')
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:8000/api/v1/generate")
LLM_MAX_TOKENS = 500
LLM_TEMPERATURE = 0.7
LLM_TOP_P=0.9
LLM_TOP_K=50

IS_DEBUG=False

chroma_db = Client(Settings(is_persistent=True, persist_directory=CHROMA_PERSIST_DIR_PATH))
collection = chroma_db.get_collection(name="knowledge_index")

vectorizer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_response(question: str) -> str:
    template_path = os.path.join('prompt.md')

    with open(template_path, 'r') as f:
        template = f.read()

    t = Template(template)
    
    embeddings = vectorizer.encode(question)
    docs = collection.query(query_embeddings=embeddings, n_results=10)['documents'][0]

    prompt = t.render(docs=docs, query=question)

    payload = {
        "prompt": prompt,
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
        "top_p": LLM_TOP_P,
        "top_k": LLM_TOP_K
    }
    response = requests.post(LLM_API_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("generated_text", "").strip()
    else:
        return "Извините, возникла ошибка при обращении к модели."

def main():
    print("RAG-бот запущен. Введите 'exit' для выхода.")
    while True:
        user_input = input("Вопрос: ")
        if user_input.lower() in ('exit', 'quit'):
            break
        if IS_DEBUG:
            start_time = time.time()
        response = get_response(user_input)
        print("Ответ бота: ", response, "\n")
        if IS_DEBUG:
            end_time = time.time()
            print(f'Время выполнения: {end_time-start_time}')

if __name__ == "__main__":
    main()    