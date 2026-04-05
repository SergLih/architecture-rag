FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY Task4-5/ .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "llm_server:app", "--host", "0.0.0.0"]