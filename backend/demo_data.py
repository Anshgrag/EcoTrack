"""
Demo Data Generator for EcoTrack
This script generates realistic demo data for testing the application
without needing actual smart plugs connected.
"""

import sqlite3
from datetime import datetime, timedelta
import random

DATABASE = 'ecotrack.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS electricity_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            mode TEXT NOT NULL,
            voltage REAL NOT NULL,
            power_watts REAL NOT NULL,
            timestamp TEXT NOT NULL,
            auto_controlled BOOLEAN DEFAULT FALSE,
            manual_override BOOLEAN DEFAULT FALSE,
            device_type TEXT DEFAULT 'unknown',
            rated_power REAL DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT UNIQUE NOT NULL,
            device_type TEXT NOT NULL,
            rated_power REAL NOT NULL,
            sleep_threshold REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            power_watts REAL NOT NULL,
            duration_minutes INTEGER NOT NULL,
            cost_wasted REAL NOT NULL,
            timestamp TEXT NOT NULL,
            auto_saved BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def add_device_profiles():
    """Add demo device profiles"""
    devices = [
        ("Living Room TV", "tv", 120, 5),
        ("Kitchen Refrigerator", "refrigerator", 150, 10),
        ("Bedroom AC", "ac", 1200, 50),
        ("Office Computer", "computer", 200, 10),
        ("Washing Machine", "appliance", 500, 5),
        ("Microwave", "appliance", 1000, 3),
        ("Router", "network", 20, 2),
        ("Phone Charger", "charger", 20, 1),
    ]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for name, device_type, rated_power, sleep_threshold in devices:
        cursor.execute('''
            INSERT OR REPLACE INTO device_profiles 
            (device_name, device_type, rated_power, sleep_threshold, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, device_type, rated_power, sleep_threshold, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"✅ Added {len(devices)} device profiles")

def generate_demo_data(days=30):
    """Generate demo electricity data for the specified number of days"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get device profiles
    cursor.execute('SELECT device_name, device_type, rated_power, sleep_threshold FROM device_profiles')
    devices = cursor.fetchall()
    
    print(f"Generating demo data for {days} days...")
    
    # Generate data for each hour of each day
    for day in range(days):
        for hour in range(24):
            timestamp = datetime.now() - timedelta(days=day, hours=hour)
            
            for device in devices:
                device_name = device['device_name']
                device_type = device['device_type']
                rated_power = device['rated_power']
                sleep_threshold = device['sleep_threshold']
                
                # Simulate different usage patterns based on time of day
                power_watts = simulate_power_usage(device_name, device_type, rated_power, hour)
                voltage = 220 + random.uniform(-10, 10)
                
                # Determine mode based on power
                if power_watts >= rated_power * 0.8:
                    mode = 'active'
                elif power_watts <= sleep_threshold:
                    mode = 'sleep'
                else:
                    mode = 'standby'
                
                # Randomly set auto_controlled
                auto_controlled = random.choice([True, False])
                
                cursor.execute('''
                    INSERT INTO electricity_data 
                    (device_name, mode, voltage, power_watts, timestamp, auto_controlled, device_type, rated_power)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (device_name, mode, voltage, power_watts, timestamp.isoformat(), 
                      auto_controlled, device_type, rated_power))
    
    conn.commit()
    conn.close()
    print(f"✅ Generated {days * 24 * len(devices)} demo records")

def simulate_power_usage(device_name, device_type, rated_power, hour):
    """Simulate realistic power usage based on device type and time of day"""
    import random
    
    # Usage patterns by hour (0-23)
    # Peak hours: 7-9 (morning), 18-22 (evening)
    # Off hours: 0-6 (night)
    
    if device_type == 'tv':
        if 18 <= hour <= 23 or 7 <= hour <= 9:
            return random.uniform(rated_power * 0.7, rated_power)
        elif 0 <= hour <= 6:
            return random.uniform(0.5, 2)  # Sleep mode
        else:
            return random.uniform(5, 30)  # Standby
    
    elif device_type == 'refrigerator':
        # Refrigerator cycles on and off
        if random.random() > 0.3:
            return rated_power * random.uniform(0.8, 1.0)
        else:
            return random.uniform(1, 5)
    
    elif device_type == 'ac':
        if 12 <= hour <= 18 and random.random() > 0.2:
            return rated_power * random.uniform(0.7, 1.0)
        elif 19 <= hour <= 23 and random.random() > 0.5:
            return rated_power * random.uniform(0.5, 0.8)
        else:
            return random.uniform(0, 30)  # Sleep/standby
    
    elif device_type == 'computer':
        if 9 <= hour <= 18:
            return rated_power * random.uniform(0.6, 1.0)
        else:
            return random.uniform(2, 10)  # Sleep mode
    
    elif device_type == 'appliance':
        # Appliances only used occasionally
        if random.random() > 0.9:
            return rated_power * random.uniform(0.8, 1.0)
        else:
            return random.uniform(0, 3)
    
    elif device_type == 'network':
        # Router runs 24/7
        return rated_power * random.uniform(0.9, 1.0)
    
    elif device_type == 'charger':
        if 18 <= hour <= 23 or 6 <= hour <= 9:
            return random.uniform(rated_power * 0.5, rated_power)
        else:
            return random.uniform(0, 2)
    
    return rated_power * 0.5

def add_demo_events():
    """Add some demo device events"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    events = [
        ("Living Room TV", "left_on", 3, 120, True),
        ("Office Computer", "left_on", 5, 60, False),
        ("Bedroom AC", "auto_off", 50, 30, True),
    ]
    
    for device_name, event_type, power, duration, auto_saved in events:
        cost = (power / 1000) * (duration / 60) * 0.12
        cursor.execute('''
            INSERT INTO device_events 
            (device_name, event_type, power_watts, duration_minutes, cost_wasted, timestamp, auto_saved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (device_name, event_type, power, duration, cost, datetime.now().isoformat(), auto_saved))
    
    conn.commit()
    conn.close()
    print("✅ Added demo events")

def reset_demo_data():
    """Clear existing demo data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM electricity_data')
    cursor.execute('DELETE FROM device_profiles')
    cursor.execute('DELETE FROM device_events')
    
    conn.commit()
    conn.close()
    print("✅ Cleared existing data")

def main():
    print("=== EcoTrack Demo Data Generator ===")
    
    # Reset existing data
    reset_demo_data()
    
    # Initialize database
    init_database()
    
    # Add device profiles
    add_device_profiles()
    
    # Generate demo data (30 days)
    generate_demo_data(days=30)
    
    # Add demo events
    add_demo_events()
    
    print("\n✅ Demo data generation complete!")
    print("You can now view the dashboard at http://localhost:8000")

if __name__ == '__main__':
    main()
