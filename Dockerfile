FROM ubuntu:latest

# Set the working directory in the Docker image
WORKDIR /app

# Copy the current directory contents into the Docker image
COPY . /app

# Install python
RUN apt-get update && apt-get install -y python3 python3-pip

# Install any necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 8000 for the app to the Docker host 
EXPOSE 8000

# Start the Uvicorn server
CMD if [ -f "zen_api/manifest.py" ]; then python3 zen_api/manifest.py; fi && exec uvicorn zen_api.main:app --host 0.0.0.0 --port 8000
