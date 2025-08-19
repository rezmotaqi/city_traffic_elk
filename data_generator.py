#!/usr/bin/env python3
"""
City Traffic Data Generator for ELK Stack
Generates realistic traffic data with time-based patterns and geographic distribution.
"""

import json
import random
import argparse
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CityTrafficGenerator:
    """Generates realistic city traffic data for ELK stack analysis."""
    
    def __init__(self):
        # Major cities with realistic coordinates
        self.cities = {
            "New York": {
                "lat_range": (40.7, 40.8),
                "lon_range": (-74.0, -73.9),
                "streets": ["Broadway", "5th Avenue", "Madison Avenue", "Park Avenue", "Lexington Avenue"],
                "traffic_patterns": "urban"
            },
            "Los Angeles": {
                "lat_range": (34.0, 34.1),
                "lon_range": (-118.3, -118.2),
                "streets": ["Sunset Boulevard", "Wilshire Boulevard", "Santa Monica Boulevard", "Ventura Boulevard"],
                "traffic_patterns": "suburban"
            },
            "Chicago": {
                "lat_range": (41.8, 41.9),
                "lon_range": (-87.7, -87.6),
                "streets": ["Michigan Avenue", "State Street", "Wabash Avenue", "Lake Shore Drive"],
                "traffic_patterns": "urban"
            },
            "Miami": {
                "lat_range": (25.7, 25.8),
                "lon_range": (-80.2, -80.1),
                "streets": ["Biscayne Boulevard", "Collins Avenue", "Ocean Drive", "Lincoln Road"],
                "traffic_patterns": "coastal"
            },
            "Seattle": {
                "lat_range": (47.6, 47.7),
                "lon_range": (-122.4, -122.3),
                "streets": ["Pike Street", "Pine Street", "Stewart Street", "Denny Way"],
                "traffic_patterns": "urban"
            }
        }
        
        # Weather conditions
        self.weather_conditions = ["clear", "cloudy", "rainy", "foggy", "snowy"]
        
        # Vehicle types and their typical distributions
        self.vehicle_types = {
            "car": {"min": 60, "max": 85},
            "truck": {"min": 10, "max": 25},
            "bus": {"min": 5, "max": 15},
            "motorcycle": {"min": 2, "max": 8}
        }
        
        # Congestion levels
        self.congestion_levels = ["low", "medium", "high", "severe"]
        
    def generate_timestamp(self, base_time: datetime = None) -> str:
        """Generate a realistic timestamp with traffic patterns."""
        if base_time is None:
            base_time = datetime.now()
        
        # Add some randomness to the time
        time_offset = random.randint(-300, 300)  # ±5 minutes
        timestamp = base_time + timedelta(seconds=time_offset)
        
        return timestamp.isoformat() + "Z"
    
    def generate_location(self, city: str) -> Dict[str, Any]:
        """Generate realistic geographic coordinates for a city."""
        city_data = self.cities[city]
        
        lat = random.uniform(*city_data["lat_range"])
        lon = random.uniform(*city_data["lon_range"])
        street = random.choice(city_data["streets"])
        
        return {
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "street": street,
            "city": city,
            "country": "USA"
        }
    
    def generate_traffic_data(self, hour: int, city: str) -> Dict[str, Any]:
        """Generate realistic traffic data based on time and city."""
        city_data = self.cities[city]
        
        # Base traffic patterns by hour (rush hours, etc.)
        if hour in [7, 8, 17, 18]:  # Rush hours
            base_vehicles = random.randint(120, 200)
            base_speed = random.randint(15, 25)
            congestion_prob = 0.8
        elif hour in [9, 10, 11, 14, 15, 16]:  # Business hours
            base_vehicles = random.randint(80, 150)
            base_speed = random.randint(25, 35)
            congestion_prob = 0.4
        elif hour in [12, 13]:  # Lunch time
            base_vehicles = random.randint(100, 180)
            base_speed = random.randint(20, 30)
            congestion_prob = 0.6
        else:  # Night hours
            base_vehicles = random.randint(20, 80)
            base_speed = random.randint(35, 50)
            congestion_prob = 0.1
        
        # Adjust for city type
        if city_data["traffic_patterns"] == "urban":
            base_vehicles = int(base_vehicles * 1.2)
            base_speed = int(base_speed * 0.9)
        elif city_data["traffic_patterns"] == "suburban":
            base_vehicles = int(base_vehicles * 0.8)
            base_speed = int(base_speed * 1.1)
        
        # Add some randomness
        vehicle_count = base_vehicles + random.randint(-20, 20)
        average_speed = base_speed + random.randint(-5, 5)
        
        # Determine congestion level
        if random.random() < congestion_prob:
            if vehicle_count > 150:
                congestion_level = random.choice(["high", "severe"])
            elif vehicle_count > 100:
                congestion_level = random.choice(["medium", "high"])
            else:
                congestion_level = random.choice(["low", "medium"])
        else:
            congestion_level = "low"
        
        # Generate vehicle type distribution
        vehicle_types = {}
        remaining = vehicle_count
        
        for vtype, limits in self.vehicle_types.items():
            if remaining <= 0:
                vehicle_types[vtype] = 0
                continue
                
            max_count = min(remaining, random.randint(limits["min"], limits["max"]))
            count = random.randint(0, max_count)
            vehicle_types[vtype] = count
            remaining -= count
        
        # Distribute remaining vehicles randomly
        if remaining > 0:
            vehicle_types["car"] += remaining
        
        return {
            "vehicle_count": vehicle_count,
            "average_speed": average_speed,
            "congestion_level": congestion_level,
            "vehicle_types": vehicle_types
        }
    
    def generate_weather(self) -> Dict[str, Any]:
        """Generate realistic weather data."""
        condition = random.choice(self.weather_conditions)
        
        # Temperature varies by season and time
        if condition == "snowy":
            temperature = random.uniform(-5, 5)
        elif condition == "rainy":
            temperature = random.uniform(5, 25)
        else:
            temperature = random.uniform(10, 30)
        
        return {
            "temperature": round(temperature, 1),
            "conditions": condition,
            "humidity": random.randint(30, 90),
            "wind_speed": random.randint(0, 25)
        }
    
    def generate_record(self, base_time: datetime = None) -> Dict[str, Any]:
        """Generate a complete traffic record."""
        if base_time is None:
            base_time = datetime.now()
        
        hour = base_time.hour
        city = random.choice(list(self.cities.keys()))
        
        record = {
            "timestamp": self.generate_timestamp(base_time),
            "location": self.generate_location(city),
            "traffic_data": self.generate_traffic_data(hour, city),
            "weather": self.generate_weather(),
            "metadata": {
                "source": "synthetic_generator",
                "version": "1.0",
                "generated_at": datetime.now().isoformat()
            }
        }
        
        return record
    
    def generate_batch(self, count: int, output_file: str = None, 
                      real_time: bool = False, interval: int = 1) -> List[Dict[str, Any]]:
        """Generate a batch of traffic records."""
        records = []
        base_time = datetime.now()
        
        logger.info(f"Generating {count} traffic records...")
        
        for i in range(count):
            # Adjust time for each record to create a realistic timeline
            record_time = base_time + timedelta(minutes=i)
            record = self.generate_record(record_time)
            records.append(record)
            
            if real_time:
                # Write to file in real-time
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(json.dumps(record) + '\n')
                
                # Wait for the specified interval
                time.sleep(interval)
                
                # Update progress
                if (i + 1) % 100 == 0:
                    logger.info(f"Generated {i + 1}/{count} records")
        
        # Save to file if not real-time
        if output_file and not real_time:
            with open(output_file, 'w') as f:
                for record in records:
                    f.write(json.dumps(record) + '\n')
            logger.info(f"Saved {len(records)} records to {output_file}")
        
        return records
    
    def generate_continuous(self, output_file: str, interval: int = 60):
        """Generate continuous traffic data in real-time."""
        logger.info(f"Starting continuous data generation to {output_file}")
        logger.info(f"Generating new record every {interval} seconds...")
        
        try:
            while True:
                record = self.generate_record()
                
                with open(output_file, 'a') as f:
                    f.write(json.dumps(record) + '\n')
                
                logger.info(f"Generated record for {record['location']['city']} at {record['timestamp']}")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Continuous generation stopped by user")

def main():
    """Main function to handle command line arguments and run the generator."""
    parser = argparse.ArgumentParser(description="Generate city traffic data for ELK stack")
    parser.add_argument("--count", "-c", type=int, default=1000,
                       help="Number of records to generate (default: 1000)")
    parser.add_argument("--output", "-o", type=str, default="traffic_data.jsonl",
                       help="Output file path (default: traffic_data.jsonl)")
    parser.add_argument("--real-time", "-r", action="store_true",
                       help="Generate data in real-time mode")
    parser.add_argument("--continuous", "--cont", action="store_true",
                       help="Generate continuous data stream")
    parser.add_argument("--interval", "-i", type=int, default=60,
                       help="Interval between records in seconds (default: 60)")
    parser.add_argument("--sample", "-s", action="store_true",
                       help="Show sample record structure")
    
    args = parser.parse_args()
    
    generator = CityTrafficGenerator()
    
    if args.sample:
        # Show sample record
        sample = generator.generate_record()
        print("Sample Traffic Record:")
        print(json.dumps(sample, indent=2))
        return
    
    if args.continuous:
        # Continuous generation
        generator.generate_continuous(args.output, args.interval)
    elif args.real_time:
        # Real-time batch generation
        generator.generate_batch(args.count, args.output, real_time=True, interval=args.interval)
    else:
        # Batch generation
        records = generator.generate_batch(args.count, args.output)
        logger.info(f"Successfully generated {len(records)} traffic records")

if __name__ == "__main__":
    main()
