Usage Guide
===========

This guide explains how to use the NILM Home Assistant project for data collection, analysis, and visualization.

Data Collection
--------------

1. Start the data collection script:

   .. code-block:: bash

      python main.py

   This will:
   - Connect to your Home Assistant instance
   - Start collecting power consumption data
   - Save raw data to ``data/raw/`` directory
   - Process and save processed data to ``data/processed/`` directory

2. Monitor the collection:
   - Check the console output for connection status
   - Verify data files are being created
   - Monitor the data collection rate

Data Visualization
----------------

1. Generate visualizations:

   .. code-block:: bash

      python visualize.py

   This will create three plots in the ``plots/`` directory:
   - Power consumption over time
   - Power distribution histogram
   - Power changes over time

2. View the plots:
   - Open the generated PNG files in the ``plots/`` directory
   - Analyze the power consumption patterns
   - Identify potential appliance events

Event Detection
-------------

The system automatically detects power events using the following parameters:

- Threshold: 20W (minimum power change to consider as an event)
- Minimum peak distance: 10 samples

You can adjust these parameters in ``visualize.py``:

.. code-block:: python

   # Event detection parameters
   THRESHOLD = 20  # Watts
   MIN_PEAK_DISTANCE = 10  # samples

Data Analysis
------------

1. Raw Data Format:
   - Timestamp: ISO format
   - Power: Watts
   - State: On/Off (if available)

2. Processed Data:
   - Timestamp: Datetime object
   - Power: Float values
   - Events: Detected state changes
   - Statistics: Mean, std, min, max

Best Practices
-------------

1. Data Collection:
   - Run collection during typical usage patterns
   - Collect data for at least 24 hours
   - Monitor system resources

2. Visualization:
   - Generate plots after significant data collection
   - Compare plots across different time periods
   - Look for patterns in power consumption

3. Event Detection:
   - Adjust threshold based on your appliances
   - Consider noise levels in your measurements
   - Validate detected events manually

Troubleshooting
--------------

1. **Data Collection Issues**
   - Check Home Assistant connection
   - Verify entity ID is correct
   - Monitor system resources

2. **Visualization Problems**
   - Ensure data files exist
   - Check file permissions
   - Verify plot parameters

3. **Event Detection Issues**
   - Adjust threshold if too many/few events
   - Check for noise in measurements
   - Verify data quality 