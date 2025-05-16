API Reference
=============

This section provides detailed documentation for the project's modules and functions.

Data Collection
--------------

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

Visualization
------------

.. automodule:: visualize
   :members:
   :undoc-members:
   :show-inheritance:

Event Detection
--------------

.. automodule:: models.event_detector
   :members:
   :undoc-members:
   :show-inheritance:

NILM Model
----------

.. automodule:: models.nilm_model
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
------------

The project uses a YAML configuration file (``config.yaml``) with the following structure:

.. code-block:: yaml

   home_assistant:
     url: "http://your-home-assistant:8123"
     token: "your-long-lived-access-token"
     entity_id: "sensor.your_energy_sensor"

   data_collection:
     interval: 1  # seconds
     max_samples: 1000
     save_interval: 100

   visualization:
     threshold: 20  # watts
     min_peak_distance: 10  # samples
     plot_size: [12, 8]
     colors:
       power: "blue"
       events: "red"

Data Structures
--------------

Raw Data Format
~~~~~~~~~~~~~~

.. code-block:: python

   {
       "timestamp": "2024-03-16T13:23:27.565582",
       "power": 120.5,
       "state": "on"
   }

Processed Data Format
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   {
       "timestamp": datetime.datetime(2024, 3, 16, 13, 23, 27, 565582),
       "power": 120.5,
       "events": {
           "type": "on",
           "magnitude": 39.485249
       }
   }

Event Format
~~~~~~~~~~~

.. code-block:: python

   {
       "timestamp": datetime.datetime(2024, 3, 16, 13, 23, 27, 565582),
       "type": "on",
       "magnitude": 39.485249,
       "power_before": 81.013722,
       "power_after": 120.5
   }

Error Handling
-------------

The project uses custom exceptions for error handling:

.. code-block:: python

   class HomeAssistantError(Exception):
       """Raised when there is an error connecting to Home Assistant."""
       pass

   class DataCollectionError(Exception):
       """Raised when there is an error collecting data."""
       pass

   class VisualizationError(Exception):
       """Raised when there is an error generating visualizations."""
       pass

Logging
-------

The project uses Python's built-in logging module with the following configuration:

.. code-block:: python

   import logging

   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('nilm_ha.log'),
           logging.StreamHandler()
       ]
   ) 