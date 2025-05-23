# Poly Micro Manager - Tauri Application

This project integrates the Poly Micro Frontend and Backend into a desktop application using Tauri, all containerized with Docker.

## Project Structure

- `poly-micro-backend/` - FastAPI backend service
- `poly-micro-frontend/` - React frontend application
- `src/` - Tauri wrapper application code
- `src-tauri/` - Tauri configuration and Rust code

## Two Ways to Run the Application

### Option 1: Docker-Only Approach (Recommended)

**Requirements:**
- Only Docker and Docker Compose

**Steps:**

1. Start all services with one of the provided scripts:

```bash
# For a normal startup:
./run.sh

# If you need to fix connectivity issues:
./fix-and-run.sh

# If you need to reset everything:
./force-restart.sh
```

This will start:
- MongoDB database
- Redis cache
- Backend FastAPI service
- Frontend React application
- Tauri container in headless mode

2. The application will be accessible in your browser at:
   - Frontend Web UI: http://localhost:3001
   - Backend API: http://localhost:8000

**Advantages:**
- No local dependencies required
- Consistent environment for all users
- Simpler setup process

### Option 2: Local Tauri Desktop App (For Testing the Native Experience)

**Requirements:**
- Rust and Cargo
- Node.js and npm
- Tauri system dependencies

**Installing Tauri Dependencies on Arch Linux:**

```bash
# Install Rust and Cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install system dependencies
sudo pacman -S webkit2gtk base-devel gtk3 libappindicator-gtk3 librsvg libvips

# For Hyprland/Wayland support
sudo pacman -S libxkbcommon wayland
```

**Building and Running Locally:**

1. Make sure Docker services are running for backend and frontend:

```bash
docker compose up -d mongodb redis backend frontend
```

2. Clone/copy the repository to your local machine

3. Navigate to the Tauri app directory and install dependencies:

```bash
cd poly-micro-tauri
npm install
```

4. Update the src-tauri/tauri.conf.json to use localhost:

```json
"devPath": "http://localhost:3001",
```

5. Update src/App.tsx to use localhost:

```typescript
iframe.src = 'http://localhost:3001';
```

6. Run the Tauri app locally:

```bash
npm run tauri:dev
```

This will open a native desktop window with your application.

## Utility Scripts

- `run.sh` - Start all services and show logs
- `fix-and-run.sh` - Stop existing containers, rebuild them with updated configurations, and start all services
- `force-restart.sh` - Force stop all containers and remove volumes, then rebuild and start all containers
- `restart-tauri.sh` - Restart only the Tauri container after configuration changes

## Configuration

Configuration is managed through environment variables defined in the docker-compose.yml file.

## Troubleshooting

- **GTK errors in Docker**: These are expected and handled by the headless mode
- **Port conflicts**: If ports are already in use, modify them in docker-compose.yml
- **Connectivity issues**: If containers can't connect to each other, use the fix-and-run.sh script
- **Wayland/Hyprland issues**: If you have display issues in local development, check that you have the proper Wayland support packages installed
