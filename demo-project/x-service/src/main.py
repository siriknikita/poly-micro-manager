from fastapi import FastAPI
import os
import sys

# Add the project root to sys.path to allow importing from app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../poly-micro-backend')))

# Import the logger from the poly-micro-backend
from app.utils.logger import create_logger

# Create FastAPI application
app = FastAPI(title="X-Service API", description="User management microservice")

# Create the logger for this service
project_id = "demo_project"
service_id = "x_service"
logger = create_logger(project_id, service_id)

@app.get("/users")
async def get_users():
    """Get all users in the system"""
    logger.info("Retrieving all users", func_id="get_users")
    return {"users": [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ]}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user by ID"""
    logger.info(f"Retrieving user with ID: {user_id}", func_id="get_user")
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

@app.post("/users")
async def create_user(user_data: dict):
    """Create a new user"""
    try:
        # Validate user data
        if not user_data.get("email"):
            logger.error("Cannot create user: missing email", func_id="create_user")
            raise ValueError("Email is required")
            
        logger.info(f"Creating new user: {user_data}", func_id="create_user")
        return {"id": 3, "name": user_data.get("name"), "email": user_data.get("email")}
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}", func_id="create_user")
        raise

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    """Update an existing user"""
    logger.info(f"Updating user with ID {user_id}: {user_data}", func_id="update_user")
    return {"id": user_id, "name": user_data.get("name"), "email": user_data.get("email")}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    logger.warning(f"Attempting to delete user with ID: {user_id}", func_id="delete_user")
    # Simulating successful deletion
    logger.info(f"User {user_id} deleted successfully", func_id="delete_user")
    return {"status": "success", "message": f"User {user_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting X-Service API server", func_id="main")
    uvicorn.run(app, host="0.0.0.0", port=8001)
