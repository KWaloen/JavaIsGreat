# Dockerfile

# • Start from a slim Python base
FROM python:3.12-slim

# • Set working directory
WORKDIR /app

# • Install system-level dependencies (if any; e.g. for psycopg2, pillow, etc.)
# RUN apt-get update && apt-get install -y build-essential

# • Copy and install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# • Copy app code
COPY . .

# • Expose FastAPI/Uvicorn port
EXPOSE 8000

# • Start Uvicorn with 4 workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
