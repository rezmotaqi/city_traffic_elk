#!/bin/bash

# City Traffic ELK Stack Setup Script
# This script sets up the complete project environment

set -e

echo "🚗 Setting up City Traffic ELK Stack Project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    print_success "All prerequisites are satisfied"
}

# Create project directories
create_directories() {
    print_status "Creating project directories..."
    
    mkdir -p data
    mkdir -p logs
    mkdir -p kibana/dashboards
    mkdir -p elasticsearch/data
    
    print_success "Project directories created"
}

# Set up Python environment
setup_python() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_success "Python dependencies installed"
}

# Generate initial sample data
generate_sample_data() {
    print_status "Generating initial sample data..."
    
    source venv/bin/activate
    
    # Generate 1000 sample records
    python3 data_generator.py --count 1000 --output data/sample_traffic.jsonl
    
    print_success "Sample data generated (1000 records)"
}

# Start ELK stack
start_elk_stack() {
    print_status "Starting ELK stack..."
    
    # Stop any existing containers
    docker-compose down 2>/dev/null || true
    
    # Start services
    docker-compose up -d
    
    print_success "ELK stack started"
    print_status "Waiting for services to be ready..."
    
    # Wait for Elasticsearch to be ready
    echo "Waiting for Elasticsearch..."
    while ! curl -s http://localhost:9200/_cluster/health > /dev/null; do
        sleep 5
    done
    
    # Wait for Logstash to be ready
    echo "Waiting for Logstash..."
    while ! curl -s http://localhost:9600 > /dev/null; do
        sleep 5
    done
    
    # Wait for Kibana to be ready
    echo "Waiting for Kibana..."
    while ! curl -s http://localhost:5601/api/status > /dev/null; do
        sleep 5
    done
    
    print_success "All services are ready!"
}

# Display status and next steps
show_status() {
    print_success "Setup completed successfully!"
    echo
    echo "🌐 Service URLs:"
    echo "  - Elasticsearch: http://localhost:9200"
    echo "  - Kibana: http://localhost:5601"
    echo "  - Logstash: http://localhost:9600"
    echo
    echo "📊 Next steps:"
    echo "  1. Open Kibana at http://localhost:5601"
    echo "  2. Create index pattern: city_traffic-*"
    echo "  3. Explore your traffic data!"
    echo
    echo "🔄 To generate more data:"
    echo "  python3 data_generator.py --count 1000 --output data/more_traffic.jsonl"
    echo
    echo "📈 To start continuous data generation:"
    echo "  python3 data_generator.py --continuous --output data/live_traffic.jsonl"
    echo
    echo "🛑 To stop services:"
    echo "  docker-compose down"
}

# Main setup flow
main() {
    echo "=========================================="
    echo "  City Traffic ELK Stack Setup"
    echo "=========================================="
    echo
    
    check_prerequisites
    create_directories
    setup_python
    generate_sample_data
    start_elk_stack
    show_status
}

# Run setup
main "$@"
