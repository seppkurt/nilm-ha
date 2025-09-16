#!/bin/bash

# NILM-HA Container mit Git Repository starten
echo "🚀 Starting NILM-HA Container from Git Repository..."

# Repository URL (anpassen!)
REPO_URL="https://github.com/DEIN-USERNAME/nilm-ha.git"

# Container stoppen falls vorhanden
echo "🛑 Stopping existing container..."
docker stop nilm-ha 2>/dev/null || true
docker rm nilm-ha 2>/dev/null || true

# Image aus Git Repository bauen
echo "🔨 Building image from Git repository..."
docker build -t nilm-ha "$REPO_URL"

# Container starten
echo "▶️ Starting container..."
docker run -d \
    --name nilm-ha \
    --env-file .env \
    -p 4444:8080 \
    --restart unless-stopped \
    nilm-ha

# Status prüfen
echo "✅ Container started!"
echo "🌐 Web Interface: http://localhost:4444"
echo "📊 API Status: http://localhost:4444/api/status"

# Logs anzeigen
echo "📋 Container logs:"
docker logs nilm-ha
