FROM python:3.12-slim

WORKDIR /app

COPY requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY src ./src

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]