#!/bin/bash

echo "🔄 Restarting NILM Container..."

# Stop and start the container
docker stop nilm-ha
docker rm nilm-ha
docker build -t nilm-ha .
docker run -d --name nilm-ha --env-file .env -p 4444:8080 --restart unless-stopped nilm-ha

echo "✅ Container restarted successfully!"
echo "🌐 Web Interface: http://localhost:4444"
