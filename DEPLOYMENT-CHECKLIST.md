# 🚀 Server Deployment Checklist

## 📁 Notwendige Dateien für den Server

### ✅ **Pflicht-Dateien (MUSS hochgeladen werden):**

1. **`Dockerfile`** - Container-Definition
2. **`compose.yml`** - Container-Konfiguration  
3. **`.env`** - Environment Variables (mit deinen Werten)
4. **`requirements.txt`** - Python-Abhängigkeiten
5. **`app.py`** - Flask Web-Interface
6. **`main.py`** - Daten-Sammlung
7. **`config.yaml`** - Konfiguration
8. **`models/event_detector.py`** - Event Detection Model
9. **`models/nilm_model.py`** - NILM Model

### 📋 **Optionale Dateien:**
- `label_events.py` - Event Labeling Tool
- `train_model.py` - Model Training
- `visualize.py` - Visualization Tools
- `README.md` - Dokumentation

## 🔧 **Server-Setup Schritte:**

### 1. **Dateien hochladen:**
```bash
# Alle Pflicht-Dateien in ein Verzeichnis auf dem Server
mkdir nilm-ha
cd nilm-ha

# Dateien hochladen (FTP, SCP, etc.)
```

### 2. **Environment konfigurieren:**
```bash
# .env Datei anpassen
nano .env
```

### 3. **Container starten:**
```bash
# Mit Docker Compose
docker compose up -d --build

# Oder mit direkten Docker Befehlen
docker build -t nilm-ha .
docker run -d --name nilm-ha --env-file .env -p 4444:8080 --restart unless-stopped nilm-ha
```

## ⚠️ **Häufige Probleme:**

### **"unable to prepare context" Fehler:**
- ✅ **Alle Dateien** im gleichen Verzeichnis?
- ✅ **Dockerfile** vorhanden?
- ✅ **Rechte** korrekt gesetzt?

### **"lstat /volume1/docker" Fehler:**
- ✅ **Pfad-Probleme** - alle Dateien im Build-Kontext?
- ✅ **Symlinks** - keine gebrochenen Links?

## 🔍 **Verifikation:**

```bash
# Container Status prüfen
docker ps

# Logs anzeigen
docker logs nilm-ha

# Web Interface testen
curl http://localhost:4444/api/status
```

## 📞 **Support:**

Bei Problemen:
1. **Logs prüfen:** `docker logs nilm-ha`
2. **Container Status:** `docker ps`
3. **Dateien prüfen:** `ls -la`
4. **Build testen:** `docker build -t nilm-ha .`
