FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NARRACAO_API_HOST=0.0.0.0 \
    NARRACAO_API_PORT=8787

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY motor/ ./motor/
COPY scripts/narracao_engine.py ./scripts/
COPY frontend/ ./frontend/

EXPOSE 8787

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8787"]