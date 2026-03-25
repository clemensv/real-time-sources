# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/noaa-nws"
LABEL org.opencontainers.image.title="NOAA NWS Weather Alerts bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the NOAA NWS Weather Alerts API and Kafka endpoints. It fetches active weather alerts from NWS and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/noaa-nws/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV NWS_LAST_POLLED_FILE="/mnt/fileshare/nws_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "noaa_nws"]
