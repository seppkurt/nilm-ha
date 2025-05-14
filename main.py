import time
import requests
import yaml
import pandas as pd
from datetime import datetime
import os

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

HA_URL = config["home_assistant"]["url"]
HA_TOKEN = config["home_assistant"]["token"]
ENTITY_ID = config["home_assistant"]["entity_id"]
POLL_INTERVAL = config["poll_interval"]
STORAGE_PATH = config["storage_path"]

os.makedirs(STORAGE_PATH, exist_ok=True)
csv_path = os.path.join(STORAGE_PATH, "energy_data.csv")

headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

def fetch_energy():
    url = f"{HA_URL}/api/states/{ENTITY_ID}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return float(data["state"])

def main():
    print("Starting NILM data collector...")
    while True:
        try:
            value = fetch_energy()
            now = datetime.now().isoformat()
            print(f"{now}: {value} W")
            # Append to CSV
            df = pd.DataFrame([[now, value]], columns=["timestamp", "watts"])
            df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
        except Exception as e:
            print("Error:", e)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
