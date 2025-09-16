#!/bin/bash

# NILM-HA Setup mit Git Repository
echo "🚀 Setting up NILM-HA from Git Repository..."

# Repository URL
REPO_URL="https://github.com/seppkurt/nilm-ha.git"
PROJECT_DIR="nilm-ha"

# Prüfen ob Git installiert ist
if ! command -v git &> /dev/null; then
    echo "❌ Git ist nicht installiert. Bitte installiere Git:"
    echo "   sudo apt update && sudo apt install git"
    exit 1
fi

# Verzeichnis erstellen und Repository klonen
echo "📁 Creating project directory..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "📥 Cloning repository..."
git clone "$REPO_URL" .

# .env Datei erstellen falls nicht vorhanden
if [ ! -f ".env" ]; then
    echo "⚠️  .env Datei nicht gefunden. Erstelle Beispiel..."
    cp env.example .env
    echo "📝 Bitte .env Datei mit deinen Home Assistant Daten anpassen!"
fi

# Container starten
echo "🔨 Building and starting container..."
docker compose up -d --build

echo "✅ Setup complete!"
echo "🌐 Web Interface: http://localhost:4444"
echo "📊 API Status: http://localhost:4444/api/status"
