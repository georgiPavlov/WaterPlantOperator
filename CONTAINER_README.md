# WaterPlantOperator Container Setup

This document describes how to run the WaterPlantOperator in a Podman container to simulate a Raspberry Pi environment.

## 🐳 Overview

The WaterPlantOperator can be run in a containerized environment using Podman and Podman Compose. This setup:

- **Simulates Raspberry Pi hardware** (GPIO, Camera, Sensors)
- **Installs all dependencies** automatically
- **Provides isolated environment** for testing
- **Enables easy deployment** and scaling
- **Supports hardware mocking** for development

## 📋 Prerequisites

### Required Software

1. **Podman** - Container runtime
2. **Podman Compose** - Container orchestration
3. **Git** - For cloning the repository

### Installation

#### Ubuntu/Debian
```bash
# Install Podman
sudo apt-get update
sudo apt-get install podman

# Install Podman Compose
pip3 install podman-compose
```

#### CentOS/RHEL/Fedora
```bash
# Install Podman
sudo dnf install podman

# Install Podman Compose
pip3 install podman-compose
```

#### macOS
```bash
# Install Podman
brew install podman

# Install Podman Compose
pip3 install podman-compose
```

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd WaterPlantOperator
```

### 2. Start Container
```bash
# Make script executable
chmod +x container_start.sh

# Start the container
./container_start.sh
```

### 3. Verify Installation
```bash
# Check container status
./container_start.sh status

# View logs
./container_start.sh logs

# Access container shell
./container_start.sh shell
```

## 📁 Container Structure

```
WaterPlantOperator/
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Docker Compose configuration
├── podman-compose.yml         # Podman Compose configuration
├── container_start.sh         # Container management script
├── requirements.txt           # Python dependencies
├── run/
│   ├── main.py               # Main application
│   └── mock_hardware.py      # Hardware simulation
├── config/
│   └── container_config.py   # Container configuration
├── monitoring/
│   └── monitor.py            # Container monitoring
├── logs/                     # Container logs
├── data/                     # Persistent data
└── CONTAINER_README.md       # This file
```

## 🔧 Configuration

### Environment Variables

The container can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `container` | Environment type |
| `SIMULATION_MODE` | `true` | Enable hardware simulation |
| `LOG_LEVEL` | `INFO` | Logging level |
| `API_HOST` | `0.0.0.0` | API host address |
| `API_PORT` | `8000` | API port |
| `BACKEND_URL` | `http://host.docker.internal:8001` | Backend API URL |
| `MOCK_GPIO` | `true` | Mock GPIO operations |
| `MOCK_CAMERA` | `true` | Mock camera operations |
| `MOCK_SENSORS` | `true` | Mock sensor operations |

### Hardware Simulation

The container includes comprehensive hardware simulation:

#### GPIO Simulation
- **Mock GPIO pins** for pump, valve, and sensor control
- **State tracking** for all GPIO operations
- **Logging** of all GPIO interactions

#### Camera Simulation
- **Mock camera** with image capture capabilities
- **Video recording** simulation
- **Preview functionality** simulation

#### Sensor Simulation
- **Moisture sensor** with realistic readings (0.0-1.0)
- **Temperature sensor** with realistic readings (15-35°C)
- **Humidity sensor** with realistic readings (0.0-1.0)
- **Water level sensor** with realistic readings (0.0-1.0)

## 🛠️ Container Management

### Available Commands

```bash
# Start container
./container_start.sh

# Build container only
./container_start.sh build

# Start container only
./container_start.sh start

# Stop container
./container_start.sh stop

# Restart container
./container_start.sh restart

# View logs
./container_start.sh logs

# Check status
./container_start.sh status

# Access shell
./container_start.sh shell
```

### Manual Podman Commands

```bash
# Build image
podman build -t waterplant-operator .

# Run container
podman run -d --name waterplant-operator \
  -p 8000:8000 \
  -v ./logs:/app/logs \
  -v ./data:/app/data \
  waterplant-operator

# View logs
podman logs waterplant-operator

# Execute commands
podman exec -it waterplant-operator bash

# Stop container
podman stop waterplant-operator

# Remove container
podman rm waterplant-operator
```

## 🌐 API Endpoints

When running in a container, the following API endpoints are available:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | System status |
| `/sensors` | GET | Sensor readings |
| `/relays` | GET/POST | Relay control |
| `/camera/capture` | POST | Take photo |
| `/watering/start` | POST | Start watering |
| `/watering/stop` | POST | Stop watering |

### Example API Calls

```bash
# Health check
curl http://localhost:8000/health

# Get status
curl http://localhost:8000/status

# Get sensor readings
curl http://localhost:8000/sensors

# Control pump
curl -X POST http://localhost:8000/relays \
  -H "Content-Type: application/json" \
  -d '{"relay": "pump", "state": true}'

# Take photo
curl -X POST http://localhost:8000/camera/capture \
  -H "Content-Type: application/json" \
  -d '{"filename": "test_photo.jpg"}'
```

## 📊 Monitoring

### Container Monitoring

The container includes a monitoring service that:

- **Checks health** every 30 seconds
- **Logs system metrics** (CPU, memory, disk)
- **Monitors sensor readings**
- **Tracks relay states**
- **Reports camera status**

### Log Files

Logs are stored in the `logs/` directory:

- `container.log` - Container startup and runtime logs
- `application.log` - Application-specific logs
- `hardware.log` - Hardware simulation logs
- `monitoring.log` - Monitoring service logs

### Viewing Logs

```bash
# View all logs
podman logs waterplant-operator

# Follow logs in real-time
podman logs -f waterplant-operator

# View specific log file
cat logs/application.log

# View monitoring logs
cat logs/monitoring.log
```

## 🔄 Integration with Complete System

### With WaterVue and WaterPlantApp

The containerized WaterPlantOperator integrates seamlessly with the complete system:

1. **Start WaterPlantApp** (Django backend)
2. **Start WaterVue** (Vue.js frontend)
3. **Start WaterPlantOperator** (Containerized hardware)

```bash
# From WaterVue directory
./start_complete_system.sh
```

### Network Configuration

The container is configured to communicate with:

- **WaterPlantApp**: `http://host.docker.internal:8001`
- **WaterVue**: `http://host.docker.internal:3000`
- **External APIs**: Configurable via environment variables

## 🧪 Testing

### Unit Tests

```bash
# Run tests in container
podman exec waterplant-operator python -m pytest tests/

# Run specific test
podman exec waterplant-operator python -m pytest tests/test_hardware.py
```

### Integration Tests

```bash
# Run integration tests
python test_complete_integration.py
```

### Hardware Simulation Tests

```bash
# Test hardware simulation
podman exec waterplant-operator python run/mock_hardware.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check Podman installation
   podman --version
   
   # Check container logs
   podman logs waterplant-operator
   ```

2. **Port conflicts**
   ```bash
   # Check if port is in use
   lsof -i :8000
   
   # Change port in docker-compose.yml
   ```

3. **Permission issues**
   ```bash
   # Make scripts executable
   chmod +x container_start.sh
   
   # Check file permissions
   ls -la
   ```

4. **Network connectivity**
   ```bash
   # Test network connectivity
   podman exec waterplant-operator ping host.docker.internal
   
   # Check DNS resolution
   podman exec waterplant-operator nslookup host.docker.internal
   ```

### Debug Mode

```bash
# Run container in debug mode
podman run -it --rm waterplant-operator bash

# Check container configuration
podman exec waterplant-operator python config/container_config.py
```

## 📈 Performance

### Resource Usage

Typical resource usage for the container:

- **CPU**: 5-15% (idle), 20-40% (active)
- **Memory**: 100-200 MB
- **Disk**: 500 MB (base image + dependencies)
- **Network**: Minimal (API calls only)

### Optimization

To optimize performance:

1. **Use multi-stage builds** for smaller images
2. **Cache dependencies** for faster builds
3. **Limit resource usage** with container limits
4. **Use volume mounts** for persistent data

## 🔒 Security

### Security Considerations

- **Non-root user** in container
- **Limited capabilities** (only SYS_RAWIO for GPIO)
- **Network isolation** via custom network
- **Read-only configuration** mounts
- **Health checks** for monitoring

### Best Practices

1. **Regular updates** of base image
2. **Scan images** for vulnerabilities
3. **Use secrets** for sensitive data
4. **Limit network access** to necessary ports
5. **Monitor container** for anomalies

## 📚 Additional Resources

- [Podman Documentation](https://docs.podman.io/)
- [Podman Compose Documentation](https://github.com/containers/podman-compose)
- [Docker to Podman Migration Guide](https://docs.podman.io/en/latest/markdown/podman-system-service.1.html)
- [Container Security Best Practices](https://docs.podman.io/en/latest/markdown/podman-run.1.html#security-options)

---

**🐳 Happy Containerizing! 🐳**


