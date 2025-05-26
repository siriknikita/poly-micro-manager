# Demo Microservices Project

This is a demonstration project showcasing a microservice architecture with test parsing functionality for the Poly Micro Manager.

## Project Structure

The demo project follows a clear microservice architecture:

```
demo-project/
├── docker-compose.yml   # Configuration for running all services
├── run.sh               # Script to build and run the project
├── tests/               # Tests directory for all microservices
│   ├── x-service/       # Tests for X-Service
│   └── y-service/       # Tests for Y-Service
├── x-service/           # User management microservice
│   ├── Dockerfile       # Container configuration
│   ├── requirements.txt # Dependencies
│   └── src/             # Source code
└── y-service/           # Product management microservice
    ├── Dockerfile       # Container configuration
    ├── requirements.txt # Dependencies
    └── src/             # Source code
```

## Features

- **Microservice Architecture**: Each service runs in its own Docker container
- **Shared Test Directory**: Tests are organized by service in a central `tests/` directory
- **Custom Logging**: Uses the project's custom logger from `app.utils.logger` module
- **API Testing**: Includes test cases for REST API endpoints
- **Test Discovery**: Works with the Poly Micro Manager to parse and discover tests

## How to Run

1. Make sure Docker and Docker Compose are installed
2. Run the startup script:
   ```
   ./run.sh
   ```
3. The script will:
   - Build and start the Docker containers for all microservices
   - Register the demo project with Poly Micro Manager (if not already registered)

## Services

### X-Service
- User management microservice
- Runs on port 8001
- Provides user CRUD operations

### Y-Service
- Product management microservice
- Runs on port 8002
- Provides product CRUD operations

## Working with Tests

The Poly Micro Manager can:
1. Discover all tests for each microservice using pytest's collection functionality
2. Parse test information and display it in the UI
3. Allow execution of tests
4. Store test results

To view and manage tests:
1. Open the Poly Micro Manager UI
2. Select the "Demo Project" from the project list
3. Navigate to the Testing tab
4. Use the Test Discovery view to see all available tests

## Integration with Poly Micro Manager

This demo project is designed to showcase the test parsing functionality of the Poly Micro Manager. When registered with the tool, it will:

1. Discover the microservices
2. Parse the test structure using `pytest --collect-only -q`
3. Display tests in a hierarchical structure
4. Store test metadata for future use
