Installation
============

This guide will help you set up the NILM Home Assistant project on your system.

Prerequisites
------------

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Home Assistant instance with energy monitoring capabilities

Step-by-Step Installation
------------------------

1. Clone the repository:

   .. code-block:: bash

      git clone <repository-url>
      cd nilm-ha

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Linux/Mac
      # or
      .\venv\Scripts\activate  # On Windows

3. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

Configuration
------------

1. Create a ``config.yaml`` file in the project root:

   .. code-block:: yaml

      home_assistant:
        url: "http://your-home-assistant:8123"
        token: "your-long-lived-access-token"
        entity_id: "sensor.your_energy_sensor"

2. Replace the placeholder values with your Home Assistant details:
   - ``url``: Your Home Assistant instance URL
   - ``token``: A long-lived access token from your Home Assistant profile
   - ``entity_id``: The entity ID of your energy monitoring sensor

Verification
-----------

To verify the installation:

1. Activate the virtual environment if not already activated:

   .. code-block:: bash

      source venv/bin/activate  # On Linux/Mac
      # or
      .\venv\Scripts\activate  # On Windows

2. Run the data collection script:

   .. code-block:: bash

      python main.py

3. Check if data is being collected in the ``data/raw/`` directory.

Troubleshooting
--------------

Common issues and solutions:

1. **Connection Error**
   - Verify your Home Assistant URL and token
   - Check if your Home Assistant instance is accessible
   - Ensure the entity ID exists and is accessible

2. **Package Installation Errors**
   - Update pip: ``pip install --upgrade pip``
   - Try installing packages one by one
   - Check Python version compatibility

3. **Permission Issues**
   - Ensure you have write permissions in the project directory
   - Check virtual environment activation
   - Verify file permissions for data storage 