"""
Main module for collecting power consumption data from Home Assistant.
"""

import os
import time
import logging
import yaml
import requests
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nilm_ha.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HomeAssistantError(Exception):
    """Raised when there is an error connecting to Home Assistant."""
    pass

class DataCollectionError(Exception):
    """Raised when there is an error collecting data."""
    pass

def load_config():
    """Load configuration from config.yaml."""
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise HomeAssistantError("config.yaml not found. Please create it first.")
    except yaml.YAMLError as e:
        raise HomeAssistantError(f"Error parsing config.yaml: {e}")

def get_power_data(config):
    """Get power data from Home Assistant."""
    url = f"{config['home_assistant']['url']}/api/states/{config['home_assistant']['entity_id']}"
    headers = {
        "Authorization": f"Bearer {config['home_assistant']['token']}",
        "content-type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HomeAssistantError(f"Error connecting to Home Assistant: {e}")

def save_data(data, filename):
    """Save data to CSV file."""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        data.to_csv(filename, index=False)
    except Exception as e:
        raise DataCollectionError(f"Error saving data: {e}")

def main():
    """Main function for data collection."""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")

        # Create data directory
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

        # Initialize data collection
        data = []
        start_time = datetime.now()
        logger.info(f"Starting data collection at {start_time}")

        # Collect data
        while True:
            try:
                # Get power data
                power_data = get_power_data(config)
                
                # Extract relevant information
                timestamp = datetime.fromisoformat(power_data['last_updated'])
                power = float(power_data['state'])
                state = power_data.get('attributes', {}).get('state', 'unknown')
                
                # Add to data list
                data.append({
                    'timestamp': timestamp,
                    'power': power,
                    'state': state
                })
                
                # Save data periodically
                if len(data) % config['data_collection']['save_interval'] == 0:
                    df = pd.DataFrame(data)
                    save_data(df, f"data/raw/power_data_{start_time.strftime('%Y%m%d_%H%M%S')}.csv")
                    logger.info(f"Saved {len(data)} data points")
                
                # Check if we've reached max samples
                if len(data) >= config['data_collection']['max_samples']:
                    break
                
                # Wait for next interval
                time.sleep(config['data_collection']['interval'])
                
            except KeyboardInterrupt:
                logger.info("Data collection interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error during data collection: {e}")
                time.sleep(5)  # Wait before retrying
        
        # Save final data
        if data:
            df = pd.DataFrame(data)
            save_data(df, f"data/raw/power_data_{start_time.strftime('%Y%m%d_%H%M%S')}.csv")
            logger.info(f"Data collection completed. Total points: {len(data)}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
