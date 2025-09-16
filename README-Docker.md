# NILM Container Deployment

## 🚀 Quick Start

```bash
# Start the container
./scripts/start.sh

# Open web interface
open http://localhost:8080
```

## 📋 Available Commands

```bash
./scripts/start.sh    # Start the container
./scripts/stop.sh     # Stop the container  
./scripts/restart.sh  # Restart the container
./scripts/logs.sh     # View container logs
```

## 🌐 Web Interface

- **Main Dashboard**: http://localhost:8080
- **API Status**: http://localhost:8080/api/status
- **Unlabeled Events**: http://localhost:8080/api/events/unlabeled

## 🔧 Features

### Data Collection
- ✅ Start/Stop collection via web interface
- ✅ Real-time status monitoring
- ✅ Automatic event detection

### Event Labeling
- ✅ Web-based labeling interface
- ✅ Batch labeling by power change
- ✅ Confidence scoring (1-5)
- ✅ Real-time statistics

### API Endpoints
- `GET /api/status` - System status
- `POST /api/start_collection` - Start data collection
- `POST /api/stop_collection` - Stop data collection
- `GET /api/events/unlabeled` - Get unlabeled events
- `POST /api/events/label` - Label events
- `GET /api/events/statistics` - Event statistics

## 📊 Usage

1. **Start Container**: `./scripts/start.sh`
2. **Open Web Interface**: http://localhost:8080
3. **Start Collection**: Click "Start Collection" button
4. **Label Events**: Use the web interface to label detected events
5. **Monitor Progress**: View real-time statistics

## 🔍 Troubleshooting

```bash
# Check container status
docker-compose ps

# View logs
./scripts/logs.sh

# Restart if needed
./scripts/restart.sh
```

## 📁 Data Storage

All data is stored inside the container:
- `data/raw/` - Raw power data and events
- `data/processed/` - Processed data and models

## 🔄 Updates

```bash
# Rebuild with latest changes
docker-compose up -d --build
```
