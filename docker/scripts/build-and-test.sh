#!/bin/bash

# Docker Build and Test Script for WebRTC OAK Server

set -e

echo "🐳 WebRTC OAK Camera Server - Docker Build & Test"
echo "=================================================="

# Get the script directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Check if docker compose is available
if ! docker compose version >/dev/null 2>&1; then
    print_error "docker compose is not installed. Please install Docker Compose."
    exit 1
fi

print_status "docker compose is available"

# Build the Docker image
echo "🔨 Building Docker image..."
if docker compose -f docker/compose/docker-compose.yml build; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Start the services
echo "🚀 Starting services..."
if docker compose -f docker/compose/docker-compose.yml up -d; then
    print_status "Services started successfully"
else
    print_error "Failed to start services"
    exit 1
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Test if the main client is accessible
echo "🧪 Testing main client endpoint..."
if curl -f -s http://localhost:8000/clients/oak_websocket_client.html >/dev/null; then
    print_status "Main client is accessible at http://localhost:8000/clients/oak_websocket_client.html"
else
    print_warning "Main client endpoint test failed - checking service status..."
    docker compose ps
    docker compose logs --tail=20 webrtc-oak-server
fi

# Test WebSocket endpoints
echo "🔌 Testing WebSocket endpoints..."

# Check if ports are listening
if nc -z localhost 8765; then
    print_status "WebSocket signaling server is listening on port 8765"
else
    print_warning "WebSocket signaling server port 8765 not accessible"
fi

if nc -z localhost 8766; then
    print_status "OAK camera bridge is listening on port 8766"
else
    print_warning "OAK camera bridge port 8766 not accessible"
fi

if nc -z localhost 8768; then
    print_status "Video file bridge is listening on port 8768"
else
    print_warning "Video file bridge port 8768 not accessible"
fi

# Check container health
echo "🏥 Checking container health..."
if docker inspect webrtc-oak-server --format='{{.State.Health.Status}}' 2>/dev/null | grep -q "healthy"; then
    print_status "Container is healthy"
else
    print_warning "Container health check not yet complete or failed"
    echo "📋 Container logs:"
    docker compose -f docker/compose/docker-compose.yml logs --tail=10 webrtc-oak-server
fi

# Check for OAK camera support
echo "🔶 Checking OAK camera support..."
if docker exec webrtc-oak-server lsusb 2>/dev/null | grep -i movidius >/dev/null; then
    print_status "OAK camera detected"
elif docker exec webrtc-oak-server ls /dev/bus/usb/ >/dev/null 2>&1; then
    print_warning "USB access available but no OAK cameras detected"
else
    print_warning "No USB device access - OAK cameras will not be available"
fi

echo ""
echo "🎉 Docker setup complete!"
echo ""
echo "📱 Access your WebRTC application at:"
echo "   Main Client: http://localhost:8000/clients/oak_websocket_client.html"
echo "   Legacy Client: http://localhost:8000/oak"
echo ""
echo "🔧 Service endpoints:"
echo "   HTTP Server: http://localhost:8000"
echo "   WebSocket Signaling: ws://localhost:8765"
echo "   OAK Camera Bridge: ws://localhost:8766"
echo "   Video File Bridge: ws://localhost:8768"
echo ""
echo "📊 Management commands:"
echo "   View logs: docker compose -f docker/compose/docker-compose.yml logs -f"
echo "   Stop services: docker compose -f docker/compose/docker-compose.yml down"
echo "   Restart: docker compose -f docker/compose/docker-compose.yml restart"
echo "   Shell access: docker exec -it webrtc-oak-server /bin/bash"
echo ""
print_status "All tests completed!"
