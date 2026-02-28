# EcoTrack - Smart Energy Monitoring System

<p align="center">
  <img src="https://img.shields.io/badge/Status-Beta-green" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.12-blue" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-lightgrey" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
</p>

## Overview

**EcoTrack** is a comprehensive smart energy monitoring system designed to help users track, analyze, and optimize their electricity consumption. The system integrates with **Tuya** and **Wipro smart plugs** to provide real-time monitoring of appliances, automatic sleep mode detection, and intelligent cost savings tracking.

---

## Features

### 1. Real-Time Energy Monitoring
- Track power consumption in watts
- Monitor voltage levels
- Detect device modes (Active/Standby/Sleep)
- Support for multiple devices

### 2. Smart Savings Analysis
- Calculate wasted energy costs
- Track savings from automation
- Device-level efficiency scoring
- Net savings calculation

### 3. Device Control
- Toggle devices on/off remotely via Tuya Cloud
- Manual override support
- Auto-control tracking

### 4. Usage Analytics
- Cost analysis by period (Today/Month/Year)
- Usage by room visualization
- Device comparison charts
- Historical data tracking

### 5. Scheduler
- Create device schedules
- Set start/end times
- Configure repeat patterns (Daily/Weekly/Monthly)
- Enable/disable schedules

---

## Three Ways to Run EcoTrack

### Option 1: Demo Mode (No Hardware Required)
Perfect for testing and demonstration without real smart plugs.

```bash
# 1. Navigate to backend folder
cd backend

# 2. Create virtual environment (if not created)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r ../requirements.txt

# 4. Run the main Flask app
python app.py

# 5. In a NEW terminal, generate demo data
cd backend
python demo_data.py

# 6. Open browser
# Visit http://localhost:8000
```

Demo mode generates 30 days of realistic electricity usage data for 8 different devices.

---

### Option 2: Tuya Smart Plug Integration

#### Step 1: Get Tuya Credentials

1. **Create a Tuya Developer Account**
   - Go to [Tuya IoT Platform](https://iot.tuya.com/)
   - Register for a free account
   - Create a new project

2. **Get API Credentials**
   - In your Tuya project, find:
     - `Access ID` (API Key)
     - `Access Secret` (API Secret)
     - `Region` (us, eu, cn, etc.)

3. **Get Your Device ID**
   - Open Tuya Smart Life app
   - Find your smart plug
   - Copy the device ID from device settings

#### Step 2: Configure Tuya

Edit `tinytuya.json` in the project root:

```json
{
    "apiKey": "YOUR_TUYA_ACCESS_ID",
    "apiSecret": "YOUR_TUYA_ACCESS_SECRET",
    "apiRegion": "us",
    "apiDeviceID": "YOUR_DEVICE_ID"
}
```

#### Step 3: Run Tuya Integration

```bash
# Start the backend
cd backend
source venv/bin/activate
python app.py

# In a NEW terminal, run Tuya integration
cd backend
python tuya_integration.py
```

This will:
- Poll your Tuya plug every 30 seconds
- Send readings to the EcoTrack API
- You can view data at http://localhost:8000

---

### Option 3: Wipro Smart Plug Integration

#### Step 1: Get Wipro Plug

1. Purchase a Wipro Smart Plug
2. Download Wipro Smart Home app
3. Set up your plug and note the device ID

#### Step 2: Configure Wipro

Edit `wipro_config.json` in the project root:

```json
{
    "device_id": "YOUR_WIPRO_DEVICE_ID",
    "api_key": "YOUR_WIPRO_API_KEY",
    "local_ip": "192.168.1.100",
    "device_name": "Living Room Plug"
}
```

**Note:** If your Wipro plug supports local API, enter its IP address. Otherwise, it will use simulated data.

#### Step 3: Run Wipro Integration

```bash
# Start the backend
cd backend
source venv/bin/activate
python app.py

# In a NEW terminal, run Wipro integration
cd backend
python wipro_integration.py
```

---

## Quick Start Guide

### Installation

```bash
# Clone or download the project
cd EcoTrack

# Install Python dependencies
cd backend
pip install -r ../requirements.txt
```

### Running the Application

```bash
# Terminal 1: Start Backend
cd backend
python app.py
# Server runs on http://localhost:5000

# Terminal 2: Start Frontend  
cd frontend
python -m http.server 8000
# Open http://localhost:8000 in browser

# Terminal 3 (Optional): Generate Demo Data
cd backend
python demo_data.py
```

---

## Project Structure

```
EcoTrack/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── demo_data.py        # Demo data generator
│   ├── tuya_integration.py # Tuya plug integration
│   ├── wipro_integration.py# Wipro plug integration
│   ├── ecotrack.db        # SQLite database
│   └── venv/              # Python virtual environment
│
├── frontend/
│   ├── index.html         # Main dashboard
│   ├── style.css         # Styling
│   ├── script.js         # Frontend logic
│   └── venv/             # Python virtual environment
│
├── screenshots/          # App screenshots
├── requirements.txt      # Python dependencies
├── tinytuya.json        # Tuya configuration (create this)
├── wipro_config.json     # Wipro configuration (create this)
└── README.md            # This file
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check |
| `/api/electricity/add` | POST | Add electricity reading |
| `/api/electricity/history` | GET | Get electricity history |
| `/api/savings` | GET | Get savings data |
| `/api/devices` | GET | List all devices |
| `/api/devices/<id>/toggle` | POST | Toggle device |
| `/api/device-profile` | POST | Add device profile |
| `/api/rooms/usage` | GET | Get room usage |
| `/api/device-event` | POST | Record device event |

---

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Cost Analysis
![Cost](screenshots/cost.png)

### Appliances
![Appliances](screenshots/appliances.png)

### Scheduler
![Scheduler](screenshots/scheduler.png)

### Usage by Rooms
![Rooms](screenshots/rooms.png)

---

## Configuration Files

### tinytuya.json (for Tuya Integration)
```json
{
    "apiKey": "YOUR_TUYA_ACCESS_ID",
    "apiSecret": "YOUR_TUYA_ACCESS_SECRET", 
    "apiRegion": "us",
    "apiDeviceID": "YOUR_DEVICE_ID"
}
```

### wipro_config.json (for Wipro Integration)
```json
{
    "device_id": "YOUR_WIPRO_DEVICE_ID",
    "api_key": "YOUR_WIPRO_API_KEY",
    "local_ip": "192.168.1.100",
    "device_name": "My Smart Plug"
}
```

---

## Troubleshooting

### Tabs Not Working
1. Open browser console (F12)
2. Check for JavaScript errors
3. Make sure backend is running on port 5000
4. Clear browser cache (Ctrl+F5)

### API Not Connecting
1. Verify backend is running: `curl http://localhost:5000/`
2. Check firewall settings
3. Verify CORS settings in app.py

### Smart Plug Not Responding
- Check internet connection
- Verify device is online in Tuya/Wipro app
- Check API credentials are correct

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12, Flask 3.0 |
| **Database** | SQLite (built-in) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Charts** | Chart.js 4.4.0 |
| **IoT Integration** | Tuya Cloud API, Wipro Smart Home |

---

## License

This project is licensed under the MIT License.

---

## Author

**Ansh Raghav**
- GitHub: [@Anshgrag](https://github.com/Anshgrag)

---

<p align="center">
  Made with ❤️ for a greener future
</p>
