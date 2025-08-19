#!/usr/bin/env python3
"""
Data Ingestion Script for City Traffic ELK Stack
Sends data directly to Logstash via HTTP for real-time testing.
"""

import json
import time
import requests
import argparse
from data_generator import CityTrafficGenerator

def send_to_logstash(data, logstash_url="http://localhost:5000"):
    """Send data to Logstash via HTTP input."""
    try:
        response = requests.post(
            logstash_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        if response.status_code == 200:
            return True
        else:
            print(f"Error sending data: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False

def ingest_batch(count, interval=1, logstash_url="http://localhost:5000"):
    """Ingest a batch of records to Logstash."""
    generator = CityTrafficGenerator()
    successful = 0
    failed = 0
    
    print(f"Starting batch ingestion of {count} records...")
    print(f"Sending to Logstash at: {logstash_url}")
    print("-" * 50)
    
    for i in range(count):
        record = generator.generate_record()
        
        if send_to_logstash(record, logstash_url):
            successful += 1
            print(f"✓ Record {i+1}/{count} sent successfully")
        else:
            failed += 1
            print(f"✗ Record {i+1}/{count} failed to send")
        
        if i < count - 1:  # Don't sleep after the last record
            time.sleep(interval)
    
    print("-" * 50)
    print(f"Ingestion complete: {successful} successful, {failed} failed")
    return successful, failed

def ingest_continuous(interval=60, logstash_url="http://localhost:5000"):
    """Continuously ingest data to Logstash."""
    generator = CityTrafficGenerator()
    record_count = 0
    
    print(f"Starting continuous ingestion...")
    print(f"Sending to Logstash at: {logstash_url}")
    print(f"Interval: {interval} seconds")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        while True:
            record = generator.generate_record()
            record_count += 1
            
            if send_to_logstash(record, logstash_url):
                print(f"✓ Record {record_count} sent: {record['location']['city']} - {record['traffic_data']['congestion_level']} traffic")
            else:
                print(f"✗ Record {record_count} failed to send")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\nContinuous ingestion stopped. Total records sent: {record_count}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Ingest city traffic data to Logstash")
    parser.add_argument("--count", "-c", type=int, default=100,
                       help="Number of records to ingest (default: 100)")
    parser.add_argument("--interval", "-i", type=int, default=1,
                       help="Interval between records in seconds (default: 1)")
    parser.add_argument("--continuous", "--cont", action="store_true",
                       help="Continuously ingest data")
    parser.add_argument("--logstash-url", "-u", type=str, 
                       default="http://localhost:5000",
                       help="Logstash HTTP input URL (default: http://localhost:5000)")
    
    args = parser.parse_args()
    
    if args.continuous:
        ingest_continuous(args.interval, args.logstash_url)
    else:
        ingest_batch(args.count, args.interval, args.logstash_url)

if __name__ == "__main__":
    main()
