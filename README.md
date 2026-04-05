# RAG Bot для QuantumForge Software

## Запуск бота

### Настройка окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Создание базы знаний, построение векторного индекса, docker-контейнера с запуском llm-сервера

```bash
./run_scripts.sh
```

### Взаимодействие с ботом

```bash
docker exec -it rag-bot python3 rag.py
```