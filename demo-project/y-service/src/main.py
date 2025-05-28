from fastapi import FastAPI
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logger = logging.getLogger("y-service")
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
app = FastAPI(title="Y-Service API", description="Product management microservice")

@app.get("/products")
async def get_products():
    """Get all products in the system"""
    logger.info("Retrieving all products")
    return {"products": [
        {"id": 1, "name": "Laptop", "price": 999.99, "inventory": 50},
        {"id": 2, "name": "Smartphone", "price": 599.99, "inventory": 100}
    ]}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    logger.info(f"Retrieving product with ID: {product_id}")
    return {"id": product_id, "name": "Laptop", "price": 999.99, "inventory": 50}

@app.post("/products")
async def create_product(product_data: dict):
    """Create a new product"""
    try:
        # Validate product data
        if not product_data.get("name") or product_data.get("price") is None:
            logger.error("Cannot create product: missing required fields")
            raise ValueError("Name and price are required")
            
        logger.info(f"Creating new product: {product_data}")
        return {"id": 3, "name": product_data.get("name"), "price": product_data.get("price"), "inventory": product_data.get("inventory")}
    except Exception as e:
        logger.error(f"Failed to create product: {str(e)}")
        raise

@app.put("/products/{product_id}")
async def update_product(product_id: int, product_data: dict):
    """Update an existing product"""
    logger.info(f"Updating product with ID {product_id}: {product_data}")
    return {"id": product_id, "name": product_data.get("name"), "price": product_data.get("price"), "inventory": product_data.get("inventory")}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Delete a product"""
    logger.warning(f"Attempting to delete product with ID: {product_id}")
    # Simulating successful deletion
    logger.info(f"Product {product_id} deleted successfully")
    return {"status": "success", "message": f"Product {product_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Y-Service API server")
    uvicorn.run(app, host="0.0.0.0", port=8002)
