"""
Visualization module for analyzing power consumption data.
"""

import os
import glob
import logging
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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

class VisualizationError(Exception):
    """Raised when there is an error generating visualizations."""
    pass

def load_config():
    """Load configuration from config.yaml."""
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise VisualizationError("config.yaml not found. Please create it first.")
    except yaml.YAMLError as e:
        raise VisualizationError(f"Error parsing config.yaml: {e}")

def load_data():
    """Load and combine all power data files."""
    try:
        # Get all CSV files in data/raw
        files = glob.glob("data/raw/power_data_*.csv")
        if not files:
            raise VisualizationError("No data files found in data/raw/")
        
        # Load and combine all files
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # Accept both 'power' and 'watts' columns
            if 'watts' in df.columns and 'power' not in df.columns:
                df.rename(columns={'watts': 'power'}, inplace=True)
            dfs.append(df)
        
        # Combine and sort by timestamp
        data = pd.concat(dfs, ignore_index=True)
        data = data.sort_values('timestamp')
        
        logger.info(f"Loaded {len(data)} data points")
        logger.info(f"Time range: {data['timestamp'].min()} to {data['timestamp'].max()}")
        logger.info(f"Power range: {data['power'].min():.2f}W to {data['power'].max():.2f}W")
        
        return data
    except Exception as e:
        raise VisualizationError(f"Error loading data: {e}")

def detect_events(data, config):
    """Detect power events using peak detection."""
    try:
        # Calculate power changes
        power_changes = np.diff(data['power'])
        
        # Find peaks (both positive and negative)
        peaks, _ = find_peaks(
            np.abs(power_changes),
            height=config['event_detection']['threshold'],
            distance=config['event_detection']['min_peak_distance']
        )
        
        # Only keep peaks where (peaks + 1) is a valid index
        valid = (peaks + 1) < len(data)
        peaks = peaks[valid]
        
        # If no valid peaks, return empty DataFrame
        if len(peaks) == 0:
            logger.info("No valid events detected.")
            return pd.DataFrame(columns=['timestamp', 'type', 'magnitude', 'power_before', 'power_after'])
        
        # Create event DataFrame
        events = pd.DataFrame({
            'timestamp': data['timestamp'].iloc[peaks + 1].values,
            'type': ['on' if power_changes[i] > 0 else 'off' for i in peaks],
            'magnitude': power_changes[peaks],
            'power_before': data['power'].iloc[peaks].values,
            'power_after': data['power'].iloc[peaks + 1].values
        })
        
        logger.info(f"Detected {len(events)} events")
        logger.info("\nEvent Statistics:")
        logger.info(events.groupby('type').describe())
        
        return events
    except Exception as e:
        raise VisualizationError(f"Error detecting events: {e}")

def create_plots(data, events, config):
    """Create visualization plots."""
    try:
        # Create plots directory
        os.makedirs("plots", exist_ok=True)
        
        # Set plot style
        plt.style.use('ggplot')
        
        # 1. Power Consumption Over Time
        plt.figure(figsize=tuple(config['visualization']['figure_size']))
        plt.plot(data['timestamp'], data['power'], 
                color=config['visualization']['colors']['power'],
                label='Power Consumption')
        
        # Log available color keys for debugging
        logger.info(f"Available event color keys: {list(config['visualization']['colors'].keys())}")
        # Add events
        for event_type in ['on', 'off']:
            event_data = events[events['type'] == event_type]
            color = config['visualization']['colors'].get(event_type, config['visualization']['colors']['events'])
            plt.scatter(event_data['timestamp'], event_data['power_after'],
                       color=color,
                       label=f'{event_type.capitalize()} Events')
        
        plt.xlabel('Time')
        plt.ylabel('Power (W)')
        plt.title('Power Consumption Over Time')
        plt.legend()
        plt.grid(True)
        plt.savefig('plots/power_consumption.png', dpi=config['visualization']['dpi'], bbox_inches='tight')
        plt.close()
        
        # 2. Power Distribution Histogram
        plt.figure(figsize=tuple(config['visualization']['figure_size']))
        plt.hist(data['power'], bins=config['visualization']['histogram']['bins'], 
                alpha=config['visualization']['histogram']['alpha'],
                color=config['visualization']['colors']['power'])
        plt.xlabel('Power (W)')
        plt.ylabel('Frequency')
        plt.title('Power Distribution Histogram')
        plt.grid(True)
        plt.savefig('plots/power_distribution.png', dpi=config['visualization']['dpi'], bbox_inches='tight')
        plt.close()
        
        # 3. Power Changes Over Time
        power_changes = np.diff(data['power'])
        plt.figure(figsize=tuple(config['visualization']['figure_size']))
        plt.plot(data['timestamp'][1:], power_changes,
                color=config['visualization']['colors']['power'],
                label='Power Changes')
        plt.axhline(y=config['event_detection']['threshold'],
                   color=config['visualization']['colors']['threshold'],
                   linestyle='--', label='Threshold')
        plt.axhline(y=-config['event_detection']['threshold'],
                   color=config['visualization']['colors']['threshold'],
                   linestyle='--')
        plt.xlabel('Time')
        plt.ylabel('Power Change (W)')
        plt.title('Power Changes Over Time')
        plt.legend()
        plt.grid(True)
        plt.savefig('plots/power_changes.png', dpi=config['visualization']['dpi'], bbox_inches='tight')
        plt.close()
        
        logger.info("Plots generated successfully")
    except Exception as e:
        raise VisualizationError(f"Error creating plots: {e}")

def main():
    """Main function for visualization."""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Load data
        data = load_data()
        
        # Detect events
        events = detect_events(data, config)
        
        # Create plots
        create_plots(data, events, config)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main() 