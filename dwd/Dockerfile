# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/dwd"
LABEL org.opencontainers.image.title="DWD Open Data bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Aggregates weather observations, station metadata, and alerts from the DWD Climate Data Center and forwards them to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/dwd/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV DWD_MODULES="station_obs_10min,weather_alerts,station_metadata"
ENV DWD_MODULES_DISABLED=""
ENV POLLING_INTERVAL=""
ENV STATE_FILE="/mnt/fileshare/dwd_state.json"

# Run the application
CMD ["python", "-m", "dwd", "feed"]
