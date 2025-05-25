#!/bin/bash

# Check if docker.service is active

echo "Checking if Docker is active..."

# If docker.service is not active, activate it
if ! systemctl is-active --quiet docker.service; then
    sudo systemctl start docker.service
fi

echo "🚀 Starting Poly Micro Manager..."

cd poly-micro-backend 
docker-compose down 
cd ..
cd poly-micro-frontend 
docker-compose down 
cd ..
docker-compose down 
docker-compose up -d --build

echo "🚀 All services are running!"
echo "🖥️ Tauri desktop app should appear on your screen shortly..."
echo ""
echo "📊 If the desktop app doesn't appear, you can access the web version at:"
echo "   http://localhost:3001"
echo ""
echo "📋 View logs with: docker compose logs -f"