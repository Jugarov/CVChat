FROM python:3.11-slim

WORKDIR /app

# Dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . /app

# Exponer puerto FastAPI
EXPOSE 8000

# Ejecutar Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
