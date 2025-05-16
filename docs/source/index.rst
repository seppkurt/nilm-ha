Welcome to NILM Home Assistant's documentation!
============================================

This project implements Non-Intrusive Load Monitoring (NILM) using data from Home Assistant.
It collects power consumption data, detects events, and provides visualization tools for analysis.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   visualization
   contributing

Installation
-----------

To install the project and its dependencies:

.. code-block:: bash

   git clone <repository-url>
   cd nilm-ha
   ./setup.sh

This will create a virtual environment and install all required packages.

Usage
-----

1. Configure Home Assistant connection in ``config.yaml``
2. Start data collection:

   .. code-block:: bash

      python main.py

3. Visualize the data:

   .. code-block:: bash

      python visualize.py

The plots will be saved in the ``plots/`` directory.

Project Structure
---------------

::

   nilm-ha/
   ├── data/               # Data storage
   │   ├── raw/           # Raw data files
   │   └── processed/     # Processed data files
   ├── models/            # Model implementations
   │   ├── nilm_model.py
   │   └── event_detector.py
   ├── plots/             # Generated plots
   ├── docs/              # Documentation
   ├── main.py           # Data collection script
   ├── visualize.py      # Visualization script
   ├── config.yaml       # Configuration file
   └── requirements.txt  # Project dependencies

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 