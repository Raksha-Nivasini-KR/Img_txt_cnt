FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for opencv-python-headless
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Expose port
EXPOSE 5000

# Start app
CMD ["python", "app.py"]
