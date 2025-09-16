#!/bin/bash

# NILM Container Management Scripts

echo "🚀 Starting NILM Container..."

# Build and start the container
docker build -t nilm-ha .
docker run -d --name nilm-ha --env-file .env -p 4444:8080 --restart unless-stopped nilm-ha

# Wait for container to be ready
echo "⏳ Waiting for container to start..."
sleep 10

# Check if container is running
if docker ps | grep -q "nilm-ha"; then
    echo "✅ Container started successfully!"
    echo "🌐 Web Interface: http://localhost:4444"
    echo "📊 API Status: http://localhost:4444/api/status"
    echo ""
    echo "📝 Available commands:"
    echo "  ./scripts/stop.sh     - Stop the container"
    echo "  ./scripts/logs.sh     - View logs"
    echo "  ./scripts/restart.sh  - Restart the container"
else
    echo "❌ Failed to start container"
    echo "📋 Check logs with: ./scripts/logs.sh"
    exit 1
fi
