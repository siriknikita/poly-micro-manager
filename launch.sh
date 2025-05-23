#!/bin/bash

# Poly Micro Manager - One-Command Launcher
# This script starts all services and opens the Tauri desktop application

echo "🚀 Starting Poly Micro Manager..."

# Set up Wayland socket for GUI forwarding
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0}

# Stop and remove existing containers
echo "🧹 Cleaning up existing containers..."
docker compose down

# Rebuild and start all containers
echo "🔨 Building and starting all services..."
docker compose up -d --build

echo "⌛ Waiting for services to initialize..."
sleep 5

echo "✅ All services are running!"
echo "🖥️ Tauri desktop app should appear on your screen shortly..."
echo ""
echo "📊 If the desktop app doesn't appear, you can access the web version at:"
echo "   http://localhost:3001"
echo ""
echo "📋 View logs with: docker compose logs -f"
