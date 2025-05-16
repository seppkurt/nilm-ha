"""
Script for training the NILM model using collected power consumption data.
"""

import os
import glob
import logging
import yaml
import pandas as pd
import numpy as np
from models.event_detector import EventDetector
from models.nilm_model import NILMModel

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

def load_config():
    """Load configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

def load_data(data_dir):
    """
    Load and combine power consumption data from CSV files.
    
    Args:
        data_dir (str): Directory containing CSV files
        
    Returns:
        pd.Series: Combined power consumption data
    """
    try:
        # Get all CSV files in the data directory
        csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
        
        if not csv_files:
            raise ValueError(f"No CSV files found in {data_dir}")
        
        # Load and combine data from all files
        dfs = []
        for file in csv_files:
            df = pd.read_csv(file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            dfs.append(df)
        
        # Combine all data
        combined_df = pd.concat(dfs)
        combined_df.sort_index(inplace=True)
        
        logger.info(f"Loaded {len(combined_df)} data points from {len(csv_files)} files")
        logger.info(f"Time range: {combined_df.index.min()} to {combined_df.index.max()}")
        logger.info(f"Power range: {combined_df['watts'].min():.1f}W to {combined_df['watts'].max():.1f}W")
        
        return combined_df['watts']
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def main():
    """Main function for training the NILM model"""
    try:
        # Load configuration
        config = load_config()
        
        # Create necessary directories
        os.makedirs(config['nilm_model']['model_dir'], exist_ok=True)
        
        # Load power consumption data
        power_data = load_data(config['data_collection']['data_dir'])
        
        # Initialize event detector
        event_detector = EventDetector(
            threshold=config['event_detection']['threshold'],
            min_peak_distance=config['event_detection']['min_peak_distance']
        )
        
        # Detect events
        events = event_detector.detect_events(power_data)
        
        if events.empty:
            logger.warning("No events detected. Cannot train model.")
            return
        
        # Initialize and train NILM model
        nilm_model = NILMModel(
            n_appliances=config['nilm_model']['n_appliances']
        )
        
        nilm_model.train(power_data, events)
        
        # Make predictions on training data
        predictions = nilm_model.predict(power_data, events)
        
        # Log prediction results
        logger.info("\nPrediction Results:")
        logger.info(predictions.groupby('appliance').agg({
            'magnitude': ['count', 'mean', 'std'],
            'power_after': ['mean', 'std']
        }))
        
        logger.info("Model training completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise

if __name__ == '__main__':
    main() 