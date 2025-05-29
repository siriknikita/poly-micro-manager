# Docker Architecture Diagram

## System Architecture

```mermaid
flowchart TB
    subgraph "User Interaction"
        user[User]
    end

    subgraph "Tauri Application"
        tauri[Tauri App\nContainer]
    end

    subgraph "Frontend Services"
        frontend[Frontend Container]
        nginx[Nginx Web Server]
    end

    subgraph "Backend Services"
        backend[Backend API\nContainer]
    end

    subgraph "Data Storage"
        mongodb[(MongoDB)]
        redis[(Redis Cache)]
    end

    %% External connection
    user -->|interacts with| tauri
    
    %% Tauri connections
    tauri -->|communicates with\nport 3001| frontend
    tauri -->|communicates with\nport 8000| backend
    
    %% Frontend connections
    nginx -->|proxies API requests to\nport 8000| backend
    frontend --> nginx
    
    %% Backend connections
    backend -->|reads/writes to| mongodb
    backend -->|caches in| redis
    backend -->|Docker API| docker[Docker Socket]

    %% Connection styles
    classDef container fill:#b3e5fc,stroke:#0277bd,stroke-width:2px
    classDef database fill:#ffe0b2,stroke:#fb8c00,stroke-width:2px
    classDef webServer fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    classDef user fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    
    class tauri,frontend,backend container
    class mongodb,redis database
    class nginx webServer
    class user user
    class docker container
end
```

## Component Details

### Infrastructure Components
- **Nginx**: Serves the frontend application static files and acts as a reverse proxy for API requests, forwarding them to the backend service
- **MongoDB**: Document database for storing application data
- **Redis**: In-memory cache for improving performance

### Application Components
- **Backend Container**: FastAPI application providing API endpoints, accessing MongoDB for data storage and Redis for caching
- **Frontend Container**: Contains the web application and Nginx web server
- **Tauri App Container**: Desktop application wrapper that communicates with both frontend and backend

### Network Configuration
- All components communicate over the `poly-micro-network` bridge network
- Services expose the following ports:
  - MongoDB: 27019:27017
  - Redis: 6380:6379
  - Backend: 8000:8000
  - Frontend/Nginx: 3001:80
  - Tauri: 6080:3001

### Data Flow
1. Users interact with the Tauri desktop application
2. Tauri communicates with both the frontend and backend
3. Frontend serves UI through Nginx
4. API requests go through Nginx to the backend
5. Backend processes requests, interacting with MongoDB and Redis
6. Backend can also interact with the Docker socket for container management

### Dependencies
- Tauri depends on both frontend and backend
- Frontend depends on backend
- Backend depends on MongoDB and Redis
