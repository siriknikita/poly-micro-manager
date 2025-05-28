from fastapi import FastAPI
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logger = logging.getLogger("x-service")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

# File handler
file_handler = RotatingFileHandler(
    os.path.join(logs_dir, 'service.log'),
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Create FastAPI application
app = FastAPI(title="X-Service API", description="User management microservice")

@app.get("/users")
async def get_users():
    """Get all users in the system"""
    logger.info("Retrieving all users")
    return {"users": [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ]}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user by ID"""
    logger.info(f"Retrieving user with ID: {user_id}")
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

@app.post("/users")
async def create_user(user_data: dict):
    """Create a new user"""
    try:
        # Validate user data
        if not user_data.get("email"):
            logger.error("Cannot create user: missing email")
            raise ValueError("Email is required")
            
        logger.info(f"Creating new user: {user_data}")
        return {"id": 3, "name": user_data.get("name"), "email": user_data.get("email")}
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}")
        raise

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    """Update an existing user"""
    logger.info(f"Updating user with ID {user_id}: {user_data}")
    return {"id": user_id, "name": user_data.get("name"), "email": user_data.get("email")}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    logger.warning(f"Attempting to delete user with ID: {user_id}")
    # Simulating successful deletion
    logger.info(f"User {user_id} deleted successfully")
    return {"status": "success", "message": f"User {user_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting X-Service API server")
    uvicorn.run(app, host="0.0.0.0", port=8001)
