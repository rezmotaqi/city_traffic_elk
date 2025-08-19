# 🚀 Quick Start Guide

Get your City Traffic ELK Stack running in minutes!

## ⚡ Super Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd city_traffic_elk

# 2. Run the setup script
./setup.sh
```

That's it! The script will:
- ✅ Check prerequisites
- ✅ Create directories
- ✅ Set up Python environment
- ✅ Generate sample data
- ✅ Start ELK stack
- ✅ Wait for services to be ready

## 🔍 Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Prerequisites
```bash
# Install Docker and Docker Compose
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Install Python 3
sudo apt-get install python3 python3-venv python3-pip
```

### 2. Project Setup
```bash
# Create directories
mkdir -p data logs kibana/dashboards elasticsearch/data

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Generate Data
```bash
# Generate sample data
python3 data_generator.py --count 1000 --output data/sample_traffic.jsonl

# Or generate continuous data
python3 data_generator.py --continuous --output data/live_traffic.jsonl
```

### 4. Start ELK Stack
```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## 🌐 Access Your Services

| Service | URL | Description |
|---------|-----|-------------|
| **Kibana** | http://localhost:5601 | Main dashboard interface |
| **Elasticsearch** | http://localhost:9200 | Data storage and search |
| **Logstash** | http://localhost:9600 | Data processing pipeline |

## 📊 First Steps in Kibana

1. **Open Kibana**: http://localhost:5601
2. **Create Index Pattern**:
   - Go to Stack Management → Index Patterns
   - Create pattern: `city_traffic-*`
   - Set time field: `@timestamp`
3. **Explore Data**:
   - Go to Discover
   - Select your index pattern
   - Start exploring!

## 🔄 Data Generation Options

### Batch Generation
```bash
# Generate 1000 records
python3 data_generator.py --count 1000

# Generate 5000 records to specific file
python3 data_generator.py --count 5000 --output data/large_dataset.jsonl
```

### Real-time Generation
```bash
# Generate 100 records with 2-second intervals
python3 data_generator.py --count 100 --real-time --interval 2

# Continuous generation (runs forever)
python3 data_generator.py --continuous --interval 30
```

### Sample Data Structure
```bash
# View sample record structure
python3 data_generator.py --sample
```

## 🛠️ Useful Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs elasticsearch
docker-compose logs logstash
docker-compose logs kibana

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Remove everything (including data)
docker-compose down -v
```

## 📈 Sample Queries

### Find High Congestion Areas
```json
GET city_traffic-*/_search
{
  "query": {
    "range": {
      "traffic_severity_score": {
        "gte": 3
      }
    }
  }
}
```

### Traffic by Hour
```json
GET city_traffic-*/_search
{
  "aggs": {
    "traffic_by_hour": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "1h"
      },
      "aggs": {
        "avg_vehicles": {
          "avg": {
            "field": "traffic_data.vehicle_count"
          }
        }
      }
    }
  }
}
```

### Weather Impact Analysis
```json
GET city_traffic-*/_search
{
  "query": {
    "term": {
      "weather_impact": "adverse"
    }
  },
  "aggs": {
    "avg_speed": {
      "avg": {
        "field": "traffic_data.average_speed"
      }
    }
  }
}
```

## 🚨 Troubleshooting

### Services Not Starting
```bash
# Check Docker status
docker ps -a

# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Data Not Appearing
```bash
# Check Logstash status
curl http://localhost:9600

# Check Elasticsearch indices
curl http://localhost:9200/_cat/indices

# Check Logstash pipeline
curl http://localhost:9600/_node/pipeline
```

### Memory Issues
```bash
# Check system resources
docker stats

# Adjust memory in docker-compose.yml
# ES_JAVA_OPTS: "-Xms512m -Xmx1g"
```

## 🎯 Next Steps

1. **Create Dashboards**: Build visualizations in Kibana
2. **Set Up Alerts**: Configure alerts for high congestion
3. **Add Real Data**: Integrate with actual traffic APIs
4. **Scale Up**: Add more nodes for production use

## 📚 Learning Resources

- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)

---

**Need Help?** Check the main README.md for detailed documentation!
