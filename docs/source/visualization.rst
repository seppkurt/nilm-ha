Visualization
=============

The visualization module provides tools to analyze power consumption data and detect events.

Plots
-----

The module generates three types of plots:

1. Power Consumption Over Time
   - Shows the raw power consumption data
   - Marks detected events (on/off) with different colors
   - Saved as ``plots/plot1.png``

   .. image:: _static/plots/power_consumption.png
      :alt: Power Consumption Over Time
      :width: 800px
      :align: center

2. Power Distribution Histogram
   - Shows the distribution of power values
   - Helps identify typical power levels
   - Saved as ``plots/plot2.png``

   .. image:: _static/plots/power_distribution.png
      :alt: Power Distribution Histogram
      :width: 800px
      :align: center

3. Power Changes Over Time
   - Shows the rate of change in power consumption
   - Helps identify sudden changes
   - Saved as ``plots/plot3.png``

   .. image:: _static/plots/power_changes.png
      :alt: Power Changes Over Time
      :width: 800px
      :align: center

Event Detection
--------------

Events are detected using the following parameters:

- Threshold: 20W (minimum power change to consider as an event)
- Minimum peak distance: 10 samples

Example Output
-------------

.. code-block:: text

   Loading data...
   Loaded 112 data points
   Time range: 2025-05-16 13:23:27.565582 to 2025-05-16 13:43:38.381192
   Power range: 84.95W to 140.05W

   Detecting events...
   Detected 2 events

   Event Statistics:
         count       mean  std        min        25%        50%        75%        max
   type                                                                              
   off     1.0 -21.566527  NaN -21.566527 -21.566527 -21.566527 -21.566527 -21.566527
   on      1.0  39.485249  NaN  39.485249  39.485249  39.485249  39.485249  39.485249

Usage
-----

To generate the plots:

.. code-block:: bash

   python visualize.py

The plots will be saved in the ``plots/`` directory.

Customization
------------

You can customize the visualization by modifying the following parameters in ``visualize.py``:

- Event detection threshold
- Plot sizes and colors
- Number of histogram bins
- Plot titles and labels

Example Configuration
-------------------

.. code-block:: python

   # Event detection parameters
   THRESHOLD = 20  # Watts
   MIN_PEAK_DISTANCE = 10  # samples

   # Plot parameters
   PLOT_SIZE = (12, 8)
   COLORS = {
       'power': 'blue',
       'events': 'red',
       'on': 'green',
       'off': 'orange'
   }

   # Histogram parameters
   BINS = 50
   ALPHA = 0.7 