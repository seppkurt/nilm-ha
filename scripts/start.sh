#!/bin/bash

# NILM Container Management Scripts

echo "🚀 Starting NILM Container..."

# Build and start the container
docker-compose up -d --build

# Wait for container to be ready
echo "⏳ Waiting for container to start..."
sleep 10

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Container started successfully!"
    echo "🌐 Web Interface: http://localhost:8080"
    echo "📊 API Status: http://localhost:8080/api/status"
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
