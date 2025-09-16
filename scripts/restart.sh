#!/bin/bash

echo "🔄 Restarting NILM Container..."

# Stop and start the container
docker-compose down
docker-compose up -d

echo "✅ Container restarted successfully!"
echo "🌐 Web Interface: http://localhost:4444"
