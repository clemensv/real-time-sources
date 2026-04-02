# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/entsoe"
LABEL org.opencontainers.image.title="ENTSO-E Transparency Platform bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the ENTSO-E Transparency Platform REST API to Kafka endpoints, emitting delta-only CloudEvents for electricity generation, load, and day-ahead prices across European bidding zones."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/entsoe/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV STATE_FILE="/mnt/fileshare/entsoe_state.json"
ENV CONNECTION_STRING=""
ENV ENTSOE_SECURITY_TOKEN=""

# Run the application
CMD ["python", "-m", "entsoe"]
