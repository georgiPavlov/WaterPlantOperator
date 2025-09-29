# WaterPlantOperator - Raspberry Pi Simulation Container
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Basic utilities
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    # GPIO and hardware simulation dependencies
    python3-dev \
    python3-pip \
    python3-venv \
    # Camera simulation dependencies
    libcamera-dev \
    libcamera-tools \
    # GPIO simulation
    libgpiod-dev \
    # Network tools
    net-tools \
    iputils-ping \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional hardware simulation packages
RUN pip install --no-cache-dir \
    # GPIO simulation
    gpiozero \
    # Web framework for API
    flask \
    flask-cors \
    # System monitoring
    psutil

# Note: picamera and RPi.GPIO are not installed as they require actual Raspberry Pi hardware
# These will be mocked by our mock_hardware.py module

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Note: Mock hardware setup is handled by mock_hardware.py at runtime
# GPIO and camera devices will be simulated in software

# Set permissions
RUN chmod +x run/container_main.py

# Expose port for API communication
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python3", "run/container_main.py"]
