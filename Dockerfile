# Use Ubuntu as base image for better GStreamer support
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    pkg-config \
    cmake \
    git \
    wget \
    curl \
    # GStreamer dependencies
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    # OpenCV dependencies
    libopencv-dev \
    python3-opencv \
    # USB device access (for OAK cameras)
    udev \
    libusb-1.0-0-dev \
    # Additional system libraries
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgtk2.0-dev \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    && rm -rf /var/lib/apt/lists/*

# Create a symbolic link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    # Verify critical dependencies are installed
    python -c "import websockets; print('✅ websockets installed')" && \
    python -c "import depthai; print('✅ depthai installed')" && \
    python -c "import cv2; print('✅ opencv installed')" && \
    python -c "import flask; print('✅ flask installed')"

# Copy the application code
COPY . .

# Test that all dependencies are properly installed
RUN python docker/tests/test_docker_deps.py

# Create necessary directories
RUN mkdir -p /app/logs

# Expose ports
EXPOSE 8000 8765 8766 8767

# Create entrypoint script
COPY docker/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/clients/oak_websocket_client.html || exit 1

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python", "start_comprehensive_servers.py"]
