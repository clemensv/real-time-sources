# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/dwd-pollenflug"
LABEL org.opencontainers.image.title="DWD Pollenflug (German Pollen Forecast) bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the DWD Pollenflug (German pollen forecast) API and Kafka endpoints. It fetches daily pollen forecasts for 27 German regions and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/dwd-pollenflug/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV DWD_POLLENFLUG_LAST_POLLED_FILE="/mnt/fileshare/dwd_pollenflug_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "dwd_pollenflug"]
