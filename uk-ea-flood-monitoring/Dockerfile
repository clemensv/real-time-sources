# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/uk-ea-flood-monitoring"
LABEL org.opencontainers.image.title="UK EA Flood Monitoring API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the UK Environment Agency Flood Monitoring API and Kafka endpoints. It fetches flood monitoring data and forwards it to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/uk-ea-flood-monitoring/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "uk_ea_flood_monitoring", "feed"]
