FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install necessary build tools for numpy
RUN apk add --no-cache gcc g++ musl-dev libffi-dev

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
