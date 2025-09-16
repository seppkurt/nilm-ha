#!/bin/bash

echo "🛑 Stopping NILM Container..."

# Stop and remove the container
docker stop nilm-ha
docker rm nilm-ha

echo "✅ Container stopped successfully!"
