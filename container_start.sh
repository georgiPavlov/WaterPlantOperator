#!/bin/bash

# WaterPlantOperator Container Startup Script
# This script starts the WaterPlantOperator in a Podman container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${PURPLE}========================================${NC}"
    echo -e "${PURPLE}🐳 WaterPlantOperator Container Setup${NC}"
    echo -e "${PURPLE}========================================${NC}"
}

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

print_url() {
    echo -e "${CYAN}🌐 $1${NC}"
}

# Check if Podman is installed
check_podman() {
    if ! command -v podman &> /dev/null; then
        print_error "Podman is not installed. Please install Podman first."
        print_status "Installation instructions:"
        print_status "  Ubuntu/Debian: sudo apt-get install podman"
        print_status "  CentOS/RHEL: sudo yum install podman"
        print_status "  macOS: brew install podman"
        exit 1
    fi
    print_success "Podman is installed: $(podman --version)"
}

# Check if Podman Compose is available
check_podman_compose() {
    if ! command -v podman-compose &> /dev/null; then
        print_warning "podman-compose not found. Installing..."
        # Try to install podman-compose
        if command -v pip3 &> /dev/null; then
            pip3 install podman-compose
        else
            print_error "pip3 not found. Please install podman-compose manually."
            print_status "Installation: pip3 install podman-compose"
            exit 1
        fi
    fi
    print_success "podman-compose is available"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p data
    mkdir -p config
    mkdir -p monitoring
    
    print_success "Directories created"
}

# Build the container
build_container() {
    print_status "Building WaterPlantOperator container..."
    
    if podman build -t waterplant-operator .; then
        print_success "Container built successfully"
    else
        print_error "Failed to build container"
        exit 1
    fi
}

# Start the container
start_container() {
    print_status "Starting WaterPlantOperator container..."
    
    # Stop any existing container
    podman stop waterplant-operator 2>/dev/null || true
    podman rm waterplant-operator 2>/dev/null || true
    
    # Start with podman-compose
    if podman-compose up -d; then
        print_success "Container started successfully"
    else
        print_error "Failed to start container"
        exit 1
    fi
}

# Check container status
check_container_status() {
    print_status "Checking container status..."
    
    if podman ps | grep -q waterplant-operator; then
        print_success "Container is running"
        
        # Get container info
        CONTAINER_ID=$(podman ps --filter "name=waterplant-operator" --format "{{.ID}}")
        print_status "Container ID: $CONTAINER_ID"
        
        # Check health
        sleep 5
        if podman exec waterplant-operator curl -f http://localhost:8000/health 2>/dev/null; then
            print_success "Container health check passed"
        else
            print_warning "Container health check failed (may still be starting)"
        fi
    else
        print_error "Container is not running"
        return 1
    fi
}

# Show container logs
show_logs() {
    print_status "Showing container logs..."
    podman logs waterplant-operator
}

# Main execution
main() {
    print_header
    
    # Check prerequisites
    check_podman
    check_podman_compose
    
    # Setup
    create_directories
    
    # Build and start
    build_container
    start_container
    
    # Verify
    if check_container_status; then
        echo ""
        print_success "🎉 WaterPlantOperator container is running!"
        echo ""
        print_url "Container API: http://localhost:8000"
        print_url "Container Health: http://localhost:8000/health"
        echo ""
        print_status "Container management commands:"
        print_status "  View logs: podman logs waterplant-operator"
        print_status "  Stop container: podman-compose down"
        print_status "  Restart container: podman-compose restart"
        print_status "  Shell access: podman exec -it waterplant-operator bash"
        echo ""
        print_status "To view logs now, run: podman logs -f waterplant-operator"
    else
        print_error "Failed to start container properly"
        show_logs
        exit 1
    fi
}

# Handle command line arguments
case "${1:-}" in
    "build")
        print_header
        check_podman
        build_container
        ;;
    "start")
        print_header
        check_podman
        check_podman_compose
        start_container
        ;;
    "stop")
        print_status "Stopping WaterPlantOperator container..."
        podman-compose down
        print_success "Container stopped"
        ;;
    "restart")
        print_status "Restarting WaterPlantOperator container..."
        podman-compose restart
        print_success "Container restarted"
        ;;
    "logs")
        show_logs
        ;;
    "status")
        check_container_status
        ;;
    "shell")
        print_status "Opening shell in container..."
        podman exec -it waterplant-operator bash
        ;;
    *)
        main
        ;;
esac


