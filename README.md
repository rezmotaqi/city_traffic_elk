# City Traffic ELK Stack Project 🚗📊

A comprehensive ELK (Elasticsearch + Logstash + Kibana) stack implementation for analyzing city traffic data. This project demonstrates real-world data pipeline skills and provides valuable insights into urban traffic patterns.

## 🎯 Project Goals

- **Data Collection**: Gather and process city traffic data
- **Real-time Analysis**: Monitor traffic patterns and congestion
- **Visualization**: Create interactive dashboards in Kibana
- **Learning**: Demonstrate ELK stack best practices

## 🏗️ Architecture

```
[Data Sources] → [Logstash] → [Elasticsearch] → [Kibana]
     ↓              ↓              ↓              ↓
  Traffic Data   Processing    Storage &      Visualization
  (Real/Gen)     Pipeline     Indexing       & Analytics
```

## 📊 Data Sources

### 1. **Synthetic Data Generator** (Included)
- Realistic traffic patterns with time-based variations
- Geographic coordinates for mapping
- Multiple data types: vehicle counts, speeds, congestion levels

### 2. **Free Public Datasets**
- **NYC Taxi & Limousine Commission**: Trip records, traffic patterns
- **Open Traffic Data**: Real-time traffic flow data
- **City of Chicago**: Traffic crash data, congestion metrics
- **OpenStreetMap**: Road network data

### 3. **Data Structure**
```json
{
  "timestamp": "2024-01-15T08:30:00Z",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060,
    "street": "Broadway",
    "city": "New York"
  },
  "traffic_data": {
    "vehicle_count": 150,
    "average_speed": 25.5,
    "congestion_level": "medium",
    "vehicle_types": {"car": 80, "truck": 20, "bus": 10}
  },
  "weather": {
    "temperature": 15.2,
    "conditions": "clear"
  }
}
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- 8GB+ RAM available

### 1. Clone & Setup
```bash
git clone <your-repo>
cd city_traffic_elk
```

### 2. Start ELK Stack
```bash
docker-compose up -d
```

### 3. Generate Sample Data
```bash
python data_generator.py --count 1000
```

### 4. Access Kibana
- Open: http://localhost:5601
- Default credentials: `elastic` / `changeme`

## 📁 Project Structure

```
city_traffic_elk/
├── docker-compose.yml          # ELK stack orchestration
├── data_generator.py           # Synthetic data generator
├── logstash/                   # Logstash configuration
│   ├── pipeline.yml
│   └── city_traffic.conf
├── kibana/                     # Kibana dashboards
│   └── dashboards/
├── elasticsearch/              # ES configuration
│   └── elasticsearch.yml
└── README.md
```

## 🔧 Configuration

### Elasticsearch
- Port: 9200
- Memory: 2GB
- Index: `city_traffic`

### Logstash
- Port: 5044
- Input: File, HTTP, Beats
- Output: Elasticsearch

### Kibana
- Port: 5601
- Index pattern: `city_traffic*`

## 📈 Sample Dashboards

1. **Traffic Overview**
   - Real-time vehicle counts
   - Congestion heatmap
   - Speed distribution

2. **Time Analysis**
   - Hourly traffic patterns
   - Day-of-week trends
   - Seasonal variations

3. **Geographic Analysis**
   - Traffic density by location
   - Route optimization
   - Hotspot identification

## 🎓 Learning Objectives

- **Data Pipeline Design**: End-to-end data flow
- **ELK Stack Configuration**: Production-ready setup
- **Data Modeling**: Efficient Elasticsearch indexing
- **Visualization**: Kibana dashboard creation
- **Real-time Monitoring**: Live data analysis

## 🔍 Sample Queries

### Find High Congestion Areas
```json
GET city_traffic/_search
{
  "query": {
    "range": {
      "traffic_data.congestion_level": {
        "gte": "high"
      }
    }
  }
}
```

### Traffic by Hour
```json
GET city_traffic/_search
{
  "aggs": {
    "traffic_by_hour": {
      "date_histogram": {
        "field": "timestamp",
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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📚 Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)

## 📄 License

MIT License - see LICENSE file for details

---

**Happy Learning! 🎉**
Transform your traffic data into actionable insights with the power of ELK stack.
