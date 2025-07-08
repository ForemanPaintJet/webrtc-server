#!/bin/bash

# Quick Docker setup script for WebRTC OAK Server
# This is a convenience wrapper for the organized Docker scripts

set -e

echo "🚀 WebRTC OAK Server - Quick Docker Setup"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

case "${1:-help}" in
"build" | "start" | "up")
    echo "🔨 Building and starting services..."
    docker compose -f docker/compose/docker-compose.yml up --build -d
    echo ""
    echo "✅ Services started! Access your application at:"
    echo "   🌐 http://localhost:8000/clients/oak_websocket_client.html"
    ;;

"dev")
    echo "🛠️ Starting development environment..."
    docker compose -f docker/compose/docker-compose.dev.yml up --build
    ;;

"test")
    echo "🧪 Running build and test script..."
    ./docker/scripts/build-and-test.sh
    ;;

"stop" | "down")
    echo "🛑 Stopping services..."
    docker compose -f docker/compose/docker-compose.yml down
    docker compose -f docker/compose/docker-compose.dev.yml down 2>/dev/null || true
    ;;

"logs")
    echo "📋 Showing logs..."
    docker compose -f docker/compose/docker-compose.yml logs -f
    ;;

"shell")
    echo "💻 Opening shell in container..."
    docker exec -it webrtc-oak-server /bin/bash
    ;;

"clean")
    echo "🧹 Cleaning up Docker resources..."
    docker compose -f docker/compose/docker-compose.yml down -v
    docker compose -f docker/compose/docker-compose.dev.yml down -v 2>/dev/null || true
    docker system prune -f
    ;;

"help" | *)
    echo "📖 Usage: $0 <command>"
    echo ""
    echo "Available commands:"
    echo "  build    - Build and start production services"
    echo "  dev      - Start development environment with live reload"
    echo "  test     - Run comprehensive build and test script"
    echo "  stop     - Stop all services"
    echo "  logs     - Show service logs"
    echo "  shell    - Open shell in running container"
    echo "  clean    - Stop services and clean up Docker resources"
    echo "  help     - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build    # Quick start production"
    echo "  $0 dev      # Development with live reload"
    echo "  $0 test     # Full build and test"
    echo "  $0 logs     # Monitor application logs"
    echo ""
    echo "📁 For more details, see: docker/README.md"
    ;;
esac
