# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables (default values)
ENV NOAA_LAST_POLLED_FILE="/mnt/fileshare/noaa_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "noaa"]