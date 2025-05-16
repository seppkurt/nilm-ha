# NILM-HA: Non-Intrusive Load Monitoring for Home Assistant

A Python-based Non-Intrusive Load Monitoring (NILM) system that uses power consumption data from Home Assistant to identify individual appliances and their energy usage patterns.

## Features

- Real-time power consumption data collection from Home Assistant
- Event detection for power state changes
- Appliance identification using machine learning
- Data visualization and analysis
- Configurable parameters for data collection, event detection, and visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nilm-ha.git
cd nilm-ha
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Home Assistant:
   - Create a long-lived access token in Home Assistant
   - Update the `config.yaml` file with your Home Assistant URL and token
   - Set the correct entity ID for your power consumption sensor

## Usage

1. Start data collection:
```bash
python main.py
```

2. Generate visualizations:
```bash
python visualize.py
```

3. Train the NILM model:
```bash
python train_model.py
```

## Configuration

The `config.yaml` file contains all configurable parameters:

- Home Assistant connection settings
- Data collection intervals
- Event detection thresholds
- NILM model parameters
- Visualization settings
- Logging configuration

## Project Structure

```
nilm-ha/
├── config.yaml           # Configuration file
├── main.py              # Main data collection script
├── visualize.py         # Data visualization script
├── models/
│   ├── event_detector.py # Event detection module
│   └── nilm_model.py    # NILM model implementation
├── data/
│   └── raw/            # Raw power consumption data
├── plots/              # Generated plots
└── docs/               # Documentation
```

## Documentation

Detailed documentation is available in the `docs` directory:

- Installation guide
- Usage instructions
- API reference
- Configuration guide
- Contributing guidelines

## Contributing

Contributions are welcome! Please read the contributing guidelines in `docs/contributing.rst` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Home Assistant for providing the power consumption data
- The NILM research community for their work on non-intrusive load monitoring
- All contributors who have helped improve this project
