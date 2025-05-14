# NILM Home Assistant Companion

This project collects energy data from a Home Assistant entity and stores it for NILM (Non-Intrusive Load Monitoring) analysis.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Edit `config.yaml` with your Home Assistant URL, token, and energy entity ID.

3. Run the collector:
   ```
   python main.py
   ```

Data will be stored in `./data/energy_data.csv`.

## Next Steps

- Event detection and clustering
- Human-in-the-loop labeling
- Device classification
