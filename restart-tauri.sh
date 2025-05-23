#!/bin/bash

# Restart just the Tauri container after configuration changes
echo "Restarting Tauri container with updated container network configuration..."

# Stop and remove the Tauri container only
docker compose stop tauri
docker compose rm -f tauri

# Rebuild and start the Tauri container
docker compose up -d tauri

echo "Tauri container restarted. Now it should connect to frontend via Docker network."
echo "Frontend Web UI available at: http://localhost:3001"
echo "Backend API available at: http://localhost:8000"
echo "Watching Tauri container logs..."

# Show only Tauri logs
docker compose logs -f tauri
