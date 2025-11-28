# Use Python 3.10 Slim image for a balance of size and compatibility
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies required for Playwright and Python build tools
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Browsers (Chromium is sufficient for this task)
RUN playwright install --with-deps chromium

# Copy the entire project into the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]