"""
Tool for labeling detected power events after data collection.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_unlabeled_events(data_dir="data/raw"):
    """
    Find all unlabeled events in the data directory.
    
    Args:
        data_dir (str): Directory containing event files
        
    Returns:
        pd.DataFrame: Combined DataFrame of all unlabeled events
    """
    unlabeled_events = []
    
    # Find all device_events files
    for filename in os.listdir(data_dir):
        if filename.startswith("device_events_") and filename.endswith(".csv"):
            filepath = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(filepath)
                # Filter for unlabeled events
                unlabeled = df[df['device_name'] == 'unlabeled'].copy()
                if not unlabeled.empty:
                    unlabeled['source_file'] = filename
                    unlabeled_events.append(unlabeled)
                    logger.info(f"Found {len(unlabeled)} unlabeled events in {filename}")
            except Exception as e:
                logger.warning(f"Error reading {filename}: {e}")
    
    if not unlabeled_events:
        logger.info("No unlabeled events found")
        return pd.DataFrame()
    
    # Combine all unlabeled events
    combined = pd.concat(unlabeled_events, ignore_index=True)
    combined = combined.sort_values('timestamp')
    
    logger.info(f"Total unlabeled events: {len(combined)}")
    return combined

def display_event_summary(events):
    """
    Display a summary of events for labeling.
    
    Args:
        events (pd.DataFrame): DataFrame of events to label
    """
    if events.empty:
        print("No events to label")
        return
    
    print(f"\n=== UNLABELED EVENTS SUMMARY ===")
    print(f"Total events: {len(events)}")
    print(f"Date range: {events['timestamp'].min()} to {events['timestamp'].max()}")
    
    # Group by power change magnitude
    print(f"\nPower change distribution:")
    print(events['power_change'].describe())
    
    # Show unique power changes
    unique_changes = events['power_change'].value_counts().sort_index()
    print(f"\nUnique power changes:")
    for change, count in unique_changes.items():
        print(f"  {change:8.1f}W: {count:3d} events")

def label_events_interactive(events):
    """
    Interactive labeling of events.
    
    Args:
        events (pd.DataFrame): DataFrame of events to label
        
    Returns:
        pd.DataFrame: Events with labels added
    """
    if events.empty:
        return events
    
    labeled_events = events.copy()
    
    # Group events by similar power changes for easier labeling
    unique_changes = events['power_change'].value_counts().sort_index()
    
    print(f"\n=== INTERACTIVE LABELING ===")
    print("You can label events by power change magnitude.")
    print("Enter 'skip' to skip a group, 'quit' to exit early.")
    
    device_mapping = {}  # Store mappings for reuse
    
    for power_change, count in unique_changes.items():
        if count == 0:
            continue
            
        print(f"\n--- Power Change: {power_change:8.1f}W ({count} events) ---")
        
        # Show some examples
        examples = events[events['power_change'] == power_change].head(3)
        print("Example events:")
        for _, event in examples.iterrows():
            timestamp = pd.to_datetime(event['timestamp']).strftime('%H:%M:%S')
            print(f"  {timestamp} - {event['change_type']} - {event['power_before']:.1f}W → {event['power_after']:.1f}W")
        
        # Get user input
        while True:
            device_name = input(f"\nWhat device causes {power_change:8.1f}W change? (or 'skip', 'quit'): ").strip()
            
            if device_name.lower() == 'quit':
                print("Labeling stopped by user")
                return labeled_events
            elif device_name.lower() == 'skip':
                print(f"Skipped {count} events with {power_change:.1f}W change")
                break
            elif device_name:
                # Get confidence
                while True:
                    confidence_input = input(f"How confident are you? (1=unsure, 5=very sure): ").strip()
                    try:
                        confidence = int(confidence_input)
                        if 1 <= confidence <= 5:
                            break
                        else:
                            print("Please enter a number between 1 and 5")
                    except ValueError:
                        print("Please enter a valid number")
                
                # Update all events with this power change
                mask = labeled_events['power_change'] == power_change
                labeled_events.loc[mask, 'device_name'] = device_name
                labeled_events.loc[mask, 'confidence'] = confidence
                
                print(f"Labeled {count} events as '{device_name}' with confidence {confidence}")
                break
            else:
                print("Please enter a device name or 'skip'/'quit'")
    
    return labeled_events

def save_labeled_events(labeled_events, output_dir="data/processed"):
    """
    Save labeled events to processed directory.
    
    Args:
        labeled_events (pd.DataFrame): Labeled events
        output_dir (str): Output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"labeled_events_{timestamp}.csv")
    
    labeled_events.to_csv(output_file, index=False)
    logger.info(f"Saved {len(labeled_events)} labeled events to {output_file}")
    
    # Show summary
    if not labeled_events.empty:
        print(f"\n=== LABELING SUMMARY ===")
        summary = labeled_events.groupby('device_name').agg({
            'power_change': ['count', 'mean', 'std'],
            'confidence': 'mean'
        }).round(2)
        print(summary)

def main():
    """Main function for labeling events."""
    try:
        # Find unlabeled events
        unlabeled_events = find_unlabeled_events()
        
        if unlabeled_events.empty:
            print("No unlabeled events found. Run data collection first.")
            return
        
        # Display summary
        display_event_summary(unlabeled_events)
        
        # Ask if user wants to proceed
        proceed = input(f"\nDo you want to label these {len(unlabeled_events)} events? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Labeling cancelled")
            return
        
        # Label events
        labeled_events = label_events_interactive(unlabeled_events)
        
        # Save results
        if not labeled_events.empty:
            save_labeled_events(labeled_events)
        
        print("\nLabeling completed!")
        
    except Exception as e:
        logger.error(f"Error in labeling: {e}")
        raise

if __name__ == "__main__":
    main()

