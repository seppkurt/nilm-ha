"""
Main module for collecting power consumption data from Home Assistant.
"""

import os
import time
import logging
import yaml
import requests
import pandas as pd
import numpy as np
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
    """Load configuration from config.yaml and environment variables."""
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # Override with environment variables if available
        if 'HA_URL' in os.environ:
            config['home_assistant']['url'] = os.environ['HA_URL']
        if 'HA_TOKEN' in os.environ:
            config['home_assistant']['token'] = os.environ['HA_TOKEN']
        if 'HA_ENTITY_ID' in os.environ:
            config['home_assistant']['entity_id'] = os.environ['HA_ENTITY_ID']
        if 'EVENT_THRESHOLD' in os.environ:
            config['event_detection']['threshold'] = int(os.environ['EVENT_THRESHOLD'])
        if 'MIN_PEAK_DISTANCE' in os.environ:
            config['event_detection']['min_peak_distance'] = int(os.environ['MIN_PEAK_DISTANCE'])
        if 'WINDOW_SIZE' in os.environ:
            config['event_detection']['window_size'] = int(os.environ['WINDOW_SIZE'])
        if 'SAVE_INTERVAL' in os.environ:
            config['data_collection']['save_interval'] = int(os.environ['SAVE_INTERVAL'])
        if 'MAX_SAMPLES' in os.environ:
            config['data_collection']['max_samples'] = int(os.environ['MAX_SAMPLES'])
        if 'COLLECTION_INTERVAL' in os.environ:
            config['data_collection']['interval'] = int(os.environ['COLLECTION_INTERVAL'])
        if 'N_APPLIANCES' in os.environ:
            config['nilm_model']['n_appliances'] = int(os.environ['N_APPLIANCES'])
            
        return config
    except FileNotFoundError:
        raise HomeAssistantError("config.yaml not found. Please create it first.")
    except yaml.YAMLError as e:
        raise HomeAssistantError(f"Error parsing config.yaml: {e}")

def list_power_entities(config):
    """
    List all power-related entities available in Home Assistant.
    
    Args:
        config (dict): Configuration dictionary containing Home Assistant connection details
        
    Returns:
        list: List of dictionaries containing entity information
    """
    url = f"{config['home_assistant']['url']}/api/states"
    headers = {
        "Authorization": f"Bearer {config['home_assistant']['token']}",
        "content-type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        states = response.json()
        
        # Filter for power-related entities
        power_entities = []
        for state in states:
            entity_id = state['entity_id']
            attributes = state.get('attributes', {})
            
            # Check if entity is power-related
            if any(keyword in entity_id.lower() for keyword in ['power', 'energy', 'watt', 'consumption']):
                power_entities.append({
                    'entity_id': entity_id,
                    'name': attributes.get('friendly_name', entity_id),
                    'state': state['state'],
                    'unit': attributes.get('unit_of_measurement', 'unknown'),
                    'device_class': attributes.get('device_class', 'unknown')
                })
        
        return power_entities
        
    except requests.exceptions.RequestException as e:
        raise HomeAssistantError(f"Error connecting to Home Assistant: {e}")

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

def save_data(df, filename):
    """Save data to CSV file."""
    df.to_csv(filename, index=False)
    logger.info(f"Data saved to {filename}")

def detect_power_change(current_power, previous_power, config):
    """
    Detect significant power changes that might indicate device state changes.
    
    Args:
        current_power (float): Current power reading
        previous_power (float): Previous power reading
        config (dict): Configuration dictionary
        
    Returns:
        tuple: (is_significant_change, change_magnitude, change_type)
    """
    power_change = current_power - previous_power
    threshold = config['event_detection']['threshold']
    
    if abs(power_change) >= threshold:
        change_type = 'on' if power_change > 0 else 'off'
        return True, power_change, change_type
    return False, power_change, None

def get_user_feedback(power_change, change_type):
    """
    Get user feedback about a detected power change.
    
    Args:
        power_change (float): Magnitude of power change
        change_type (str): Type of change ('on' or 'off')
        
    Returns:
        dict: User feedback including device name and confidence
    """
    print(f"\nDetected a {change_type} event with power change of {power_change:.1f}W")
    print("Please provide information about this event:")
    
    device_name = input("Which device caused this change? (or 'unknown'): ").strip()
    if device_name.lower() == 'unknown':
        return None
    
    confidence = input("How confident are you about this identification? (1-5): ").strip()
    try:
        confidence = int(confidence)
        if not 1 <= confidence <= 5:
            confidence = 3  # Default to medium confidence if invalid input
    except ValueError:
        confidence = 3
    
    return {
        'device_name': device_name,
        'confidence': confidence,
        'power_change': power_change,
        'change_type': change_type,
        'timestamp': datetime.now().isoformat()
    }

def main():
    """Main function for data collection."""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")

        # List available power entities
        logger.info("Listing available power-related entities...")
        power_entities = list_power_entities(config)
        
        if power_entities:
            logger.info("\nAvailable power-related entities:")
            for entity in power_entities:
                logger.info(f"- {entity['name']} ({entity['entity_id']})")
                logger.info(f"  State: {entity['state']} {entity['unit']}")
                logger.info(f"  Device Class: {entity['device_class']}")
        else:
            logger.warning("No power-related entities found in Home Assistant")
            return

        # Create data directory
        os.makedirs("data/raw", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

        # Initialize data collection
        data = []
        device_events = []  # Store device identification events
        start_time = datetime.now()
        logger.info(f"Starting data collection at {start_time}")
        
        # Get initial power reading
        initial_data = get_power_data(config)
        previous_power = float(initial_data['state'])
        logger.info(f"Initial power reading: {previous_power}W")

        # Collect data
        while True:
            try:
                # Get power data
                power_data = get_power_data(config)
                
                # Extract relevant information
                timestamp = datetime.fromisoformat(power_data['last_updated'])
                current_power = float(power_data['state'])
                
                # Detect power changes
                is_change, power_change, change_type = detect_power_change(
                    current_power, previous_power, config
                )
                
                # If significant change detected, record event without user input
                if is_change:
                    # Record event for later labeling
                    event = {
                        'timestamp': timestamp.isoformat(),
                        'power_change': power_change,
                        'change_type': change_type,
                        'power_before': previous_power,
                        'power_after': current_power,
                        'device_name': 'unlabeled',  # Will be labeled later
                        'confidence': 0  # Will be set during labeling
                    }
                    device_events.append(event)
                    logger.info(f"Event detected: {change_type} event with {power_change:.1f}W change (unlabeled)")
                
                # Add to data list
                data.append({
                    'timestamp': timestamp,
                    'power': current_power,
                    'power_change': power_change
                })
                
                # Save data periodically
                if len(data) % config['data_collection']['save_interval'] == 0:
                    # Save power data
                    df = pd.DataFrame(data)
                    save_data(df, f"data/raw/power_data_{start_time.strftime('%Y%m%d_%H%M%S')}.csv")
                    
                    # Save device events
                    if device_events:
                        events_df = pd.DataFrame(device_events)
                        save_data(events_df, f"data/raw/device_events_{start_time.strftime('%Y%m%d_%H%M%S')}.csv")
                    
                    logger.info(f"Saved {len(data)} data points and {len(device_events)} device events")
                
                # Update previous power
                previous_power = current_power
                
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
            # Save power data
            df = pd.DataFrame(data)
            save_data(df, f"data/raw/power_data_{start_time.strftime('%Y%m%d_%H%M%S')}.csv")
            
            # Save device events
            if device_events:
                events_df = pd.DataFrame(device_events)
                save_data(events_df, f"data/raw/device_events_{start_time.strftime('%Y%m%d_%H%M%S')}.csv")
            
            logger.info(f"Data collection completed. Total points: {len(data)}, Device events: {len(device_events)}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
