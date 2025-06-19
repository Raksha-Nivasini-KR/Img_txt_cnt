# Build the image
docker build -t image-to-text-app .

# Run the container
docker run -p 5000:5000 image-to-text-app

# (Optional) Check running containers
docker ps

# (Optional) Stop a running container
docker stop <container_id>
