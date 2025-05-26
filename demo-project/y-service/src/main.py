from fastapi import FastAPI
import os
import sys

# Add the project root to sys.path to allow importing from app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../poly-micro-backend')))

# Import the logger from the poly-micro-backend
from app.utils.logger import create_logger

# Create FastAPI application
app = FastAPI(title="Y-Service API", description="Product management microservice")

# Create the logger for this service
project_id = "demo_project"
service_id = "y_service"
logger = create_logger(project_id, service_id)

@app.get("/products")
async def get_products():
    """Get all products in the system"""
    logger.info("Retrieving all products", func_id="get_products")
    return {"products": [
        {"id": 1, "name": "Laptop", "price": 999.99, "inventory": 50},
        {"id": 2, "name": "Smartphone", "price": 599.99, "inventory": 100}
    ]}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    logger.info(f"Retrieving product with ID: {product_id}", func_id="get_product")
    return {"id": product_id, "name": "Laptop", "price": 999.99, "inventory": 50}

@app.post("/products")
async def create_product(product_data: dict):
    """Create a new product"""
    try:
        # Validate product data
        if not product_data.get("name") or product_data.get("price") is None:
            logger.error("Cannot create product: missing required fields", func_id="create_product")
            raise ValueError("Name and price are required")
            
        logger.info(f"Creating new product: {product_data}", func_id="create_product")
        return {"id": 3, "name": product_data.get("name"), "price": product_data.get("price"), "inventory": product_data.get("inventory")}
    except Exception as e:
        logger.error(f"Failed to create product: {str(e)}", func_id="create_product")
        raise

@app.put("/products/{product_id}")
async def update_product(product_id: int, product_data: dict):
    """Update an existing product"""
    logger.info(f"Updating product with ID {product_id}: {product_data}", func_id="update_product")
    return {"id": product_id, "name": product_data.get("name"), "price": product_data.get("price"), "inventory": product_data.get("inventory")}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Delete a product"""
    logger.warning(f"Attempting to delete product with ID: {product_id}", func_id="delete_product")
    # Simulating successful deletion
    logger.info(f"Product {product_id} deleted successfully", func_id="delete_product")
    return {"status": "success", "message": f"Product {product_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Y-Service API server", func_id="main")
    uvicorn.run(app, host="0.0.0.0", port=8002)
