"""
NILM Web Application - Simple web interface for data collection and labeling.
"""

import os
import json
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import threading
import time

app = Flask(__name__)

# Global variables for process management
collection_process = None
collection_status = "stopped"

@app.route('/')
def index():
    """Main dashboard."""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current system status."""
    # Container is running = data collection is running
    collection_status = "running"
    
    # Get data statistics
    stats = get_data_stats()
    
    return jsonify({
        'collection_status': collection_status,
        'stats': stats
    })


@app.route('/api/events/unlabeled')
def get_unlabeled_events():
    """Get all unlabeled events."""
    try:
        events = find_unlabeled_events()
        if events.empty:
            return jsonify({'events': []})
        
        # Convert to list of dicts
        events_list = events.to_dict('records')
        return jsonify({'events': events_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events/label', methods=['POST'])
def label_events():
    """Label events."""
    try:
        data = request.json
        power_change = data.get('power_change')
        device_name = data.get('device_name')
        confidence = data.get('confidence', 3)
        
        if not power_change or not device_name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Update events in CSV files
        update_events_in_files(power_change, device_name, confidence)
        
        return jsonify({'message': 'Events labeled successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events/statistics')
def get_event_statistics():
    """Get event statistics."""
    try:
        events = find_unlabeled_events()
        if events.empty:
            return jsonify({'statistics': {}})
        
        # Group by power change
        stats = events['power_change'].value_counts().to_dict()
        return jsonify({'statistics': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/power')
def get_power_data():
    """Get all power data."""
    try:
        power_data = []
        data_dir = "data/raw"
        
        if not os.path.exists(data_dir):
            return jsonify({'data': []})
        
        for filename in os.listdir(data_dir):
            if filename.startswith("power_data_") and filename.endswith(".csv"):
                filepath = os.path.join(data_dir, filename)
                try:
                    df = pd.read_csv(filepath)
                    # Convert to list of dicts
                    data_list = df.to_dict('records')
                    power_data.extend(data_list)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        # Sort by timestamp
        power_data.sort(key=lambda x: x.get('timestamp', ''))
        return jsonify({'data': power_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/events')
def get_all_events():
    """Get all events (labeled and unlabeled)."""
    try:
        all_events = []
        data_dir = "data/raw"
        
        if not os.path.exists(data_dir):
            return jsonify({'data': []})
        
        for filename in os.listdir(data_dir):
            if filename.startswith("device_events_") and filename.endswith(".csv"):
                filepath = os.path.join(data_dir, filename)
                try:
                    df = pd.read_csv(filepath)
                    # Convert to list of dicts
                    data_list = df.to_dict('records')
                    all_events.extend(data_list)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        # Sort by timestamp
        all_events.sort(key=lambda x: x.get('timestamp', ''))
        return jsonify({'data': all_events})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def find_unlabeled_events():
    """Find all unlabeled events."""
    unlabeled_events = []
    data_dir = "data/raw"
    
    if not os.path.exists(data_dir):
        return pd.DataFrame()
    
    for filename in os.listdir(data_dir):
        if filename.startswith("device_events_") and filename.endswith(".csv"):
            filepath = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(filepath)
                unlabeled = df[df['device_name'] == 'unlabeled'].copy()
                if not unlabeled.empty:
                    unlabeled['source_file'] = filename
                    unlabeled_events.append(unlabeled)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    if not unlabeled_events:
        return pd.DataFrame()
    
    return pd.concat(unlabeled_events, ignore_index=True)

def update_events_in_files(power_change, device_name, confidence):
    """Update events in CSV files."""
    data_dir = "data/raw"
    
    for filename in os.listdir(data_dir):
        if filename.startswith("device_events_") and filename.endswith(".csv"):
            filepath = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(filepath)
                # Update matching events
                mask = (df['power_change'] == power_change) & (df['device_name'] == 'unlabeled')
                df.loc[mask, 'device_name'] = device_name
                df.loc[mask, 'confidence'] = confidence
                df.to_csv(filepath, index=False)
            except Exception as e:
                print(f"Error updating {filename}: {e}")

def get_data_stats():
    """Get data collection statistics."""
    stats = {
        'total_events': 0,
        'unlabeled_events': 0,
        'labeled_events': 0,
        'last_update': None
    }
    
    try:
        events = find_unlabeled_events()
        stats['unlabeled_events'] = len(events)
        
        # Count all events
        data_dir = "data/raw"
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.startswith("device_events_") and filename.endswith(".csv"):
                    filepath = os.path.join(data_dir, filename)
                    try:
                        df = pd.read_csv(filepath)
                        stats['total_events'] += len(df)
                        stats['labeled_events'] += len(df[df['device_name'] != 'unlabeled'])
                    except:
                        pass
        
        # Get last update time
        if os.path.exists("data/raw"):
            files = [f for f in os.listdir("data/raw") if f.endswith('.csv')]
            if files:
                latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join("data/raw", x)))
                stats['last_update'] = datetime.fromtimestamp(
                    os.path.getmtime(os.path.join("data/raw", latest_file))
                ).isoformat()
    
    except Exception as e:
        print(f"Error getting stats: {e}")
    
    return stats

if __name__ == '__main__':
    # Create templates directory and basic template
    os.makedirs('templates', exist_ok=True)
    
    # Create basic HTML template
    template_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>NILM Data Collection</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .status { padding: 15px; border-radius: 5px; margin: 20px 0; }
        .status.running { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.stopped { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .controls { margin: 20px 0; }
        button { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-secondary { background: #6c757d; color: white; }
        .events-section { margin-top: 30px; }
        .event-group { margin: 15px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .event-group h4 { margin: 0 0 10px 0; color: #333; }
        .event-list { margin: 10px 0; }
        .event-item { padding: 8px; background: #f8f9fa; margin: 5px 0; border-radius: 3px; }
        .form-group { margin: 10px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; font-size: 14px; }
        .data-section { margin-top: 30px; }
        .tabs { margin: 20px 0; }
        .tab-btn { padding: 10px 20px; margin-right: 5px; border: 1px solid #ddd; background: #f8f9fa; cursor: pointer; border-radius: 4px 4px 0 0; }
        .tab-btn.active { background: white; border-bottom: 1px solid white; }
        .tab-content { border: 1px solid #ddd; border-top: none; padding: 20px; background: white; }
        .data-table-container { max-height: 400px; overflow-y: auto; border: 1px solid #ddd; }
        .data-table { width: 100%; border-collapse: collapse; }
        .data-table th, .data-table td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }
        .data-table th { background: #f8f9fa; font-weight: bold; position: sticky; top: 0; }
        .data-table tr:hover { background: #f5f5f5; }
        .data-table tr.unlabeled { background: #fff3cd; }
        .data-table tr.labeled { background: #d4edda; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔌 NILM Data Collection</h1>
            <p>Non-Intrusive Load Monitoring System</p>
            <p><small>💡 Container läuft = Datensammlung läuft | Container stoppen = Datensammlung stoppen</small></p>
        </div>
        
        <div id="status" class="status running">
            Status: <span id="status-text">Running</span>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-events">0</div>
                <div class="stat-label">Total Events</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="unlabeled-events">0</div>
                <div class="stat-label">Unlabeled</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="labeled-events">0</div>
                <div class="stat-label">Labeled</div>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn-secondary" onclick="refreshData()">🔄 Refresh</button>
        </div>
        
        <div class="events-section">
            <h3>📝 Event Labeling</h3>
            <div id="events-container">
                <p>Loading events...</p>
            </div>
        </div>
        
        <div class="data-section">
            <h3>📊 Data View</h3>
            <div class="tabs">
                <button class="tab-btn active" onclick="showTab('power')">Power Data</button>
                <button class="tab-btn" onclick="showTab('events')">All Events</button>
            </div>
            
            <div id="power-tab" class="tab-content">
                <h4>Power Consumption Data</h4>
                <div class="data-table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Power (W)</th>
                                <th>Change (W)</th>
                            </tr>
                        </thead>
                        <tbody id="power-data-body">
                            <tr><td colspan="3">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div id="events-tab" class="tab-content" style="display: none;">
                <h4>All Events (Labeled & Unlabeled)</h4>
                <div class="data-table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Device</th>
                                <th>Type</th>
                                <th>Power Change (W)</th>
                                <th>Confidence</th>
                            </tr>
                        </thead>
                        <tbody id="events-data-body">
                            <tr><td colspan="5">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    // Always show running since container is running
                    const statusEl = document.getElementById('status');
                    const statusText = document.getElementById('status-text');
                    
                    statusText.textContent = 'Running';
                    statusEl.className = 'status running';
                    
                    document.getElementById('total-events').textContent = data.stats.total_events || 0;
                    document.getElementById('unlabeled-events').textContent = data.stats.unlabeled_events || 0;
                    document.getElementById('labeled-events').textContent = data.stats.labeled_events || 0;
                });
        }
        
        function loadEvents() {
            fetch('/api/events/unlabeled')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('events-container');
                    
                    if (data.events.length === 0) {
                        container.innerHTML = '<p>No unlabeled events found.</p>';
                        return;
                    }
                    
                    // Group events by power change
                    const grouped = {};
                    data.events.forEach(event => {
                        const key = event.power_change;
                        if (!grouped[key]) {
                            grouped[key] = [];
                        }
                        grouped[key].push(event);
                    });
                    
                    let html = '';
                    Object.keys(grouped).forEach(powerChange => {
                        const events = grouped[powerChange];
                        const count = events.length;
                        const changeType = events[0].change_type;
                        const timestamp = new Date(events[0].timestamp).toLocaleString();
                        
                        html += `
                            <div class="event-group">
                                <h4>${powerChange}W ${changeType} (${count} events)</h4>
                                <div class="event-list">
                                    <div class="event-item">
                                        <strong>Time:</strong> ${timestamp}<br>
                                        <strong>Type:</strong> ${changeType}<br>
                                        <strong>Count:</strong> ${count} similar events
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label>Device Name:</label>
                                    <input type="text" id="device-${powerChange}" placeholder="e.g., Wasserkocher, TV, etc.">
                                </div>
                                <div class="form-group">
                                    <label>Confidence (1-5):</label>
                                    <select id="confidence-${powerChange}">
                                        <option value="1">1 - Unsure</option>
                                        <option value="2">2 - Somewhat sure</option>
                                        <option value="3" selected>3 - Moderately sure</option>
                                        <option value="4">4 - Pretty sure</option>
                                        <option value="5">5 - Very sure</option>
                                    </select>
                                </div>
                                <button class="btn-primary" onclick="labelEvents(${powerChange})">Label Events</button>
                            </div>
                        `;
                    });
                    
                    container.innerHTML = html;
                });
        }
        
        
        function labelEvents(powerChange) {
            const deviceName = document.getElementById(`device-${powerChange}`).value;
            const confidence = document.getElementById(`confidence-${powerChange}`).value;
            
            if (!deviceName.trim()) {
                alert('Please enter a device name');
                return;
            }
            
            fetch('/api/events/label', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    power_change: powerChange,
                    device_name: deviceName,
                    confidence: parseInt(confidence)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('Events labeled successfully!');
                    loadEvents();
                    updateStatus();
                }
            });
        }
        
        function refreshData() {
            updateStatus();
            loadEvents();
            loadPowerData();
            loadAllEvents();
        }
        
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').style.display = 'block';
            event.target.classList.add('active');
        }
        
        function loadPowerData() {
            fetch('/api/data/power')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('power-data-body');
                    if (data.data.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="3">No power data available</td></tr>';
                        return;
                    }
                    
                    let html = '';
                    data.data.forEach(row => {
                        const timestamp = new Date(row.timestamp).toLocaleString();
                        const power = parseFloat(row.power).toFixed(1);
                        const change = parseFloat(row.power_change).toFixed(1);
                        html += `<tr>
                            <td>${timestamp}</td>
                            <td>${power}</td>
                            <td>${change}</td>
                        </tr>`;
                    });
                    tbody.innerHTML = html;
                });
        }
        
        function loadAllEvents() {
            fetch('/api/data/events')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.getElementById('events-data-body');
                    if (data.data.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="5">No events available</td></tr>';
                        return;
                    }
                    
                    let html = '';
                    data.data.forEach(row => {
                        const timestamp = new Date(row.timestamp).toLocaleString();
                        const device = row.device_name || 'unlabeled';
                        const type = row.change_type || '';
                        const change = parseFloat(row.power_change).toFixed(1);
                        const confidence = row.confidence || 0;
                        
                        const deviceClass = device === 'unlabeled' ? 'unlabeled' : 'labeled';
                        html += `<tr class="${deviceClass}">
                            <td>${timestamp}</td>
                            <td>${device}</td>
                            <td>${type}</td>
                            <td>${change}</td>
                            <td>${confidence}</td>
                        </tr>`;
                    });
                    tbody.innerHTML = html;
                });
        }
        
        // Auto-refresh every 30 seconds
        setInterval(updateStatus, 30000);
        
        // Initial load
        updateStatus();
        loadEvents();
        loadPowerData();
        loadAllEvents();
    </script>
</body>
</html>
    '''
    
    with open('templates/index.html', 'w') as f:
        f.write(template_content)
    
    app.run(host='0.0.0.0', port=8080, debug=False)
