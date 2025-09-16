# Environment Configuration

## 🔧 Setup

1. **Copy the example file:**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` with your values:**
   ```bash
   nano .env
   ```

## 📝 Configuration Variables

### Home Assistant
- `HA_URL` - Your Home Assistant URL (e.g., https://your-ha.com:8123)
- `HA_TOKEN` - Long-lived access token from Home Assistant
- `HA_ENTITY_ID` - Power sensor entity ID (e.g., sensor.power_current_power)

### Event Detection
- `EVENT_THRESHOLD` - Minimum power change to detect as event (default: 20W)
- `MIN_PEAK_DISTANCE` - Minimum samples between events (default: 10)
- `WINDOW_SIZE` - Window size for event feature extraction (default: 30)

### Data Collection
- `SAVE_INTERVAL` - Save data every N samples (default: 100)
- `MAX_SAMPLES` - Maximum samples to collect (default: 10000)
- `COLLECTION_INTERVAL` - Data collection interval in seconds (default: 10)

### NILM Model
- `N_APPLIANCES` - Number of appliances to identify (default: 5)

### Flask
- `FLASK_ENV` - Flask environment (default: production)
- `FLASK_PORT` - Internal Flask port (default: 8080)

## 🔒 Security

- **Never commit `.env` to Git** - it contains sensitive tokens
- **Use `.env.example`** as a template for others
- **Rotate tokens regularly** for security

## 🚀 Usage

After creating `.env`, start the container:
```bash
./scripts/start.sh
```

The container will automatically load your environment variables.
