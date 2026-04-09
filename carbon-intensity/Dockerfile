# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/carbon-intensity"
LABEL org.opencontainers.image.title="Carbon Intensity UK bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the National Grid ESO Carbon Intensity API and Kafka endpoints. It fetches GB electricity carbon intensity, generation mix, and regional breakdowns and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/carbon-intensity/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV CARBON_INTENSITY_LAST_POLLED_FILE="/mnt/fileshare/carbon_intensity_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "carbon_intensity"]
