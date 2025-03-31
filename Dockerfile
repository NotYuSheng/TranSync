FROM python:3.10-slim

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Hugging Face model cache
ENV TRANSFORMERS_CACHE=/app/cache

# Copy script and create data folders
COPY translate.py .
RUN mkdir -p /app/data/input /app/data/output

# Run on container start
CMD ["python", "translate.py"]
