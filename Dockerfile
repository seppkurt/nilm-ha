FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add Flask for web interface
RUN pip install --no-cache-dir flask

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/raw data/processed

# Expose port for web interface
EXPOSE 8080

# Create startup script
RUN echo '#!/bin/bash\npython main.py &\npython app.py' > /app/start.sh && chmod +x /app/start.sh

# Default command (can be overridden)
CMD ["/app/start.sh"]
