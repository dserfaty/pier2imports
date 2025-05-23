FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
#RUN apt-get update && apt-get install -y gcc libpq-dev curl unzip && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run migrations and then start the FastAPI server
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload