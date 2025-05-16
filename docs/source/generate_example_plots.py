import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Generate sample data
np.random.seed(42)
n_samples = 100
base_power = 100
time = [datetime.now() + timedelta(minutes=i) for i in range(n_samples)]
power = base_power + np.random.normal(0, 5, n_samples)

# Add some events
events = [30, 60, 80]
for event in events:
    power[event:] += np.random.choice([-20, 20])

# Create plots directory if it doesn't exist
import os
os.makedirs('_static/plots', exist_ok=True)

# 1. Power Consumption Over Time
plt.figure(figsize=(12, 8))
plt.plot(time, power, 'b-', label='Power Consumption')
plt.scatter([time[i] for i in events], [power[i] for i in events], 
           c='r', label='Events', zorder=5)
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.title('Power Consumption Over Time')
plt.legend()
plt.grid(True)
plt.savefig('_static/plots/power_consumption.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Power Distribution Histogram
plt.figure(figsize=(12, 8))
plt.hist(power, bins=50, alpha=0.7, color='blue')
plt.xlabel('Power (W)')
plt.ylabel('Frequency')
plt.title('Power Distribution Histogram')
plt.grid(True)
plt.savefig('_static/plots/power_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Power Changes Over Time
power_changes = np.diff(power)
plt.figure(figsize=(12, 8))
plt.plot(time[1:], power_changes, 'g-', label='Power Changes')
plt.axhline(y=20, color='r', linestyle='--', label='Threshold')
plt.axhline(y=-20, color='r', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Power Change (W)')
plt.title('Power Changes Over Time')
plt.legend()
plt.grid(True)
plt.savefig('_static/plots/power_changes.png', dpi=300, bbox_inches='tight')
plt.close() 