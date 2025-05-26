FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Create directory for logs
RUN mkdir -p logs

# Expose port
EXPOSE 8002

# Command to run the application
CMD ["python", "main.py"]
