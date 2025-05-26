#!/bin/bash

# Demo project startup script
echo "Starting Demo Microservices Project..."

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Create logs directories if they don't exist
mkdir -p x-service/logs
mkdir -p y-service/logs

# Build and start the containers
echo "Building and starting Docker containers..."
docker-compose up --build -d

echo "Containers started successfully!"
echo "X-Service is running at http://localhost:8001"
echo "Y-Service is running at http://localhost:8002"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"

# Wait for the poly-micro-manager backend to be ready
echo "Waiting for poly-micro-manager backend to be ready..."
BACKEND_URL="http://backend:8000"
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
  attempt=$((attempt+1))
  echo "Attempt $attempt/$max_attempts: Checking backend availability..."
  if curl -s --head --fail "$BACKEND_URL/api/health" > /dev/null; then
    echo "Backend is ready!"
    break
  fi
  
  if [ $attempt -eq $max_attempts ]; then
    echo "Backend service did not become available in time. Using local registration only."
  else
    echo "Backend not ready yet. Waiting 2 seconds..."
    sleep 2
  fi
done

# Create a project in the poly-micro-manager if it doesn't exist
echo "Checking if demo project exists in poly-micro-manager..."
PROJECT_ID=$(curl -s $BACKEND_URL/api/projects | jq '.[] | select(.name=="Demo Project") | .id' -r)

if [ -z "$PROJECT_ID" ]; then
  echo "Creating demo project in poly-micro-manager..."
  PROJECT_DATA='{
    "name": "Demo Project",
    "path": "'$(pwd)'",
    "tests_dir_path": "tests"
  }'
  
  PROJECT_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "$PROJECT_DATA" \
    $BACKEND_URL/api/projects)
  
  # Debug - print full response
  echo "API Response: $PROJECT_RESPONSE"
  
  # Check if the response contains an ID
  if echo "$PROJECT_RESPONSE" | grep -q "id"; then
    PROJECT_ID=$(echo $PROJECT_RESPONSE | jq '.id' -r)
    echo "Demo project created with ID: $PROJECT_ID"
  else
    echo "Failed to create project. API response: $PROJECT_RESPONSE"
    echo "Using existing project if available..."
  fi
else
  echo "Demo project already exists with ID: $PROJECT_ID"
fi

echo ""
echo "You can now use the poly-micro-manager to manage this project and parse its tests."
echo "Demo setup complete!"
