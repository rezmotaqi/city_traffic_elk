#!/usr/bin/env python3
"""
Service Monitoring Script for City Traffic ELK Stack
Checks the health and status of all services.
"""

import requests
import json
import time
from datetime import datetime

class ELKMonitor:
    """Monitor ELK stack services."""
    
    def __init__(self):
        self.services = {
            "elasticsearch": {
                "url": "http://localhost:9200",
                "health_endpoint": "/_cluster/health",
                "status_endpoint": "/_cat/indices"
            },
            "logstash": {
                "url": "http://localhost:9600",
                "health_endpoint": "/",
                "status_endpoint": "/_node/pipeline"
            },
            "kibana": {
                "url": "http://localhost:5601",
                "health_endpoint": "/api/status",
                "status_endpoint": "/api/saved_objects/_find"
            }
        }
    
    def check_service_health(self, service_name, service_config):
        """Check if a service is healthy."""
        try:
            health_url = f"{service_config['url']}{service_config['health_endpoint']}"
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                return True, response.json() if response.headers.get('content-type', '').startswith('application/json') else "OK"
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def get_service_status(self, service_name, service_config):
        """Get detailed status of a service."""
        try:
            status_url = f"{service_config['url']}{service_config['status_endpoint']}"
            response = requests.get(status_url, timeout=5)
            
            if response.status_code == 200:
                return response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            else:
                return f"HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return str(e)
    
    def check_elasticsearch_indices(self):
        """Check Elasticsearch indices."""
        try:
            response = requests.get("http://localhost:9200/_cat/indices?format=json", timeout=5)
            if response.status_code == 200:
                indices = response.json()
                return [idx for idx in indices if idx['index'].startswith('city_traffic')]
            else:
                return []
        except:
            return []
    
    def check_logstash_pipeline(self):
        """Check Logstash pipeline status."""
        try:
            response = requests.get("http://localhost:9600/_node/pipeline", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None
    
    def monitor_all_services(self):
        """Monitor all services and display status."""
        print("🔍 ELK Stack Service Monitor")
        print("=" * 50)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_healthy = True
        
        for service_name, service_config in self.services.items():
            print(f"📊 {service_name.upper()}")
            print("-" * 30)
            
            # Check health
            is_healthy, health_info = self.check_service_health(service_name, service_config)
            
            if is_healthy:
                print(f"✅ Status: Healthy")
                if isinstance(health_info, dict):
                    if service_name == "elasticsearch":
                        cluster_status = health_info.get('status', 'unknown')
                        print(f"   Cluster Status: {cluster_status}")
                        print(f"   Number of Nodes: {health_info.get('number_of_nodes', 'N/A')}")
                    elif service_name == "logstash":
                        print(f"   Version: {health_info.get('version', 'N/A')}")
                    elif service_name == "kibana":
                        status = health_info.get('status', {})
                        print(f"   Overall Status: {status.get('overall', {}).get('level', 'N/A')}")
            else:
                print(f"❌ Status: Unhealthy - {health_info}")
                all_healthy = False
            
            print()
        
        # Check specific data
        print("📈 Data Status")
        print("-" * 30)
        
        # Elasticsearch indices
        indices = self.check_elasticsearch_indices()
        if indices:
            print(f"✅ Traffic Data Indices: {len(indices)} found")
            for idx in indices:
                print(f"   - {idx['index']}: {idx['docs.count']} documents")
        else:
            print("❌ No traffic data indices found")
        
        print()
        
        # Logstash pipeline
        pipeline = self.check_logstash_pipeline()
        if pipeline:
            print("✅ Logstash Pipeline: Active")
        else:
            print("❌ Logstash Pipeline: Not accessible")
        
        print()
        print("=" * 50)
        
        if all_healthy:
            print("🎉 All services are healthy!")
        else:
            print("⚠️  Some services have issues. Check the details above.")
        
        return all_healthy
    
    def continuous_monitoring(self, interval=30):
        """Continuously monitor services."""
        print(f"🔄 Starting continuous monitoring (every {interval} seconds)")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                self.monitor_all_services()
                time.sleep(interval)
                print("\n" + "="*80 + "\n")
                
        except KeyboardInterrupt:
            print("\n🛑 Continuous monitoring stopped")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor ELK stack services")
    parser.add_argument("--continuous", "-c", action="store_true",
                       help="Enable continuous monitoring")
    parser.add_argument("--interval", "-i", type=int, default=30,
                       help="Monitoring interval in seconds (default: 30)")
    
    args = parser.parse_args()
    
    monitor = ELKMonitor()
    
    if args.continuous:
        monitor.continuous_monitoring(args.interval)
    else:
        monitor.monitor_all_services()

if __name__ == "__main__":
    main()
