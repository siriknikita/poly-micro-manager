# Poly Micro Manager - Tauri Application

This project integrates the Poly Micro Frontend and Backend into a desktop application using Tauri, all containerized with Docker.

## Prerequisites

- Docker and Docker Compose
- Git

## Setup

1. Clone the repository:

```bash
git clone https://github.com/siriknikita/poly-micro-manager-app.git
```

2. Navigate to the root directory:

```bash
cd poly-micro-manager-app
```

3. Initialize submodules:

```bash
git submodule update --init --recursive
```


## Two Ways to Run the Application

### Option 1: Docker-Only Approach (Recommended)

**Requirements:**
- Only Docker and Docker Compose

**Steps:**

1. Start all services with one of the provided scripts:

```bash
# For a normal startup:
./run.sh
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

## Configuration

Configuration is managed through environment variables defined in the docker-compose.yml file.

## Troubleshooting

- **GTK errors in Docker**: These are expected and handled by the headless mode
- **Port conflicts**: If ports are already in use, modify them in docker-compose.yml
- **Wayland/Hyprland issues**: If you have display issues in local development, check that you have the proper Wayland support packages installed
