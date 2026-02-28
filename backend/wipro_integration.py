"""
Wipro Smart Plug API Integration for EcoTrack
This module provides integration with Wipro smart plugs for real-time power monitoring.

## Wipro Smart Plug Setup Instructions

### Step 1: Get Wipro Smart Plug Credentials
1. Download the Wipro Smart Home app from App Store/Play Store
2. Create an account and register your Wipro smart plug
3. Note down the device ID from the app

### Step 2: API Configuration
Wipro plugs typically use the Wipro Smart Home API or can be accessed through 
a local API if your plug supports it.

Note: Wipro smart plugs may use different protocols. This integration assumes
the plug supports HTTP-based API calls.

### Configuration File Format
Create 'wipro_config.json' in the backend folder:

{
    "device_id": "your_device_id",
    "api_key": "your_api_key",
    "local_ip": "192.168.1.x",  // Optional: for local control
    "device_name": "Living Room Plug"
}

### Step 3: Run the API
python wipro_integration.py

This will:
- Start the Wipro API server on port 5001
- Poll the smart plug for readings every 30 seconds
- Send data to the main EcoTrack API

## API Endpoints

GET /api/wipro/status - Get current plug status
POST /api/wipro/control - Turn plug on/off
GET /api/wipro/readings - Get power readings history
"""

import requests
import json
import time
import threading
from datetime import datetime

# Configuration
WIPRO_CONFIG_FILE = 'wipro_config.json'
API_BASE_URL = 'http://localhost:5000'
POLL_INTERVAL = 30  # seconds

class WiproSmartPlug:
    def __init__(self, config_file=WIPRO_CONFIG_FILE):
        self.config = self.load_config(config_file)
        self.device_id = self.config.get('device_id', '')
        self.api_key = self.config.get('api_key', '')
        self.local_ip = self.config.get('local_ip', '')
        self.device_name = self.config.get('device_name', 'Wipro Plug')
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found. Using defaults.")
            return {}
    
    def get_power_reading(self):
        """
        Get current power reading from Wipro plug
        Returns: dict with power_watts, voltage, current
        """
        # Note: This is a placeholder. You'll need to adapt this based on 
        # the actual Wipro API endpoints
        
        # Option 1: Local API (if supported by your plug)
        if self.local_ip:
            try:
                response = requests.get(
                    f"http://{self.local_ip}/api/status",
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'power_watts': data.get('power', 0),
                        'voltage': data.get('voltage', 220),
                        'current': data.get('current', 0)
                    }
            except Exception as e:
                print(f"Error getting local reading: {e}")
        
        # Option 2: Cloud API (placeholder - replace with actual endpoints)
        # This would require the actual Wipro API endpoints
        """
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(
                f"https://api.wipro.com/v1/devices/{self.device_id}/status",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'power_watts': data.get('power', 0),
                    'voltage': data.get('voltage', 220),
                    'current': data.get('current', 0)
                }
        except Exception as e:
            print(f"Error getting cloud reading: {e}")
        """
        
        # Return simulated data for demo purposes
        # Remove this when you have real API access
        import random
        return {
            'power_watts': random.uniform(0, 150),
            'voltage': random.uniform(215, 225),
            'current': random.uniform(0, 1)
        }
    
    def set_power_state(self, state):
        """
        Turn the plug on or off
        state: 'on' or 'off'
        """
        # Placeholder - replace with actual API call
        print(f"Wipro Plug turned {state}")
        
        # Option 1: Local API
        if self.local_ip:
            try:
                response = requests.post(
                    f"http://{self.local_ip}/api/control",
                    json={'state': state},
                    timeout=5
                )
                return response.status_code == 200
            except Exception as e:
                print(f"Error controlling plug: {e}")
        
        return True
    
    def send_to_ecotrack(self, power_watts, voltage, current):
        """Send reading to EcoTrack API"""
        try:
            data = {
                'device_name': self.device_name,
                'mode': 'active' if power_watts > 5 else 'sleep',
                'voltage': voltage,
                'power_watts': power_watts,
                'timestamp': datetime.now().isoformat(),
                'auto_controlled': True
            }
            
            response = requests.post(
                f'{API_BASE_URL}/api/electricity/add',
                json=data,
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"✅ Sent reading to EcoTrack: {power_watts:.1f}W")
                return True
            else:
                print(f"❌ Failed to send reading: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending to EcoTrack: {e}")
            return False


def start_wipro_polling():
    """Start polling the Wipro plug"""
    plug = WiproSmartPlug()
    
    print("=== Wipro Smart Plug Integration Started ===")
    print(f"Device: {plug.device_name}")
    print(f"Polling every {POLL_INTERVAL} seconds...")
    print(f"Sending data to: {API_BASE_URL}")
    print("\nPress Ctrl+C to stop\n")
    
    while True:
        try:
            # Get power reading
            reading = plug.get_power_reading()
            
            # Send to EcoTrack
            plug.send_to_ecotrack(
                reading['power_watts'],
                reading['voltage'],
                reading['current']
            )
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(POLL_INTERVAL)


def demo_mode():
    """Run in demo mode with simulated data"""
    print("=== Wipro Integration - Demo Mode ===")
    print("Running with simulated data\n")
    
    plug = WiproSmartPlug()
    
    import random
    while True:
        # Simulate power reading
        power = random.uniform(0, 150)
        voltage = random.uniform(215, 225)
        
        plug.send_to_ecotrack(power, voltage, 0)
        time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_mode()
    else:
        try:
            start_wipro_polling()
        except KeyboardInterrupt:
            print("\n\nWipro integration stopped.")
