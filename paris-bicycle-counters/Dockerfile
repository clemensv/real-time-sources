# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/paris-bicycle-counters"
LABEL org.opencontainers.image.title="Paris Bicycle Counters bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between Paris Open Data bicycle counting stations and Kafka endpoints. It fetches hourly bicycle counts and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/paris-bicycle-counters/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV PARIS_VELO_LAST_POLLED_FILE="/mnt/fileshare/paris_velo_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "paris_bicycle_counters"]
