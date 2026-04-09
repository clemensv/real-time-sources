# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/airqo-uganda"
LABEL org.opencontainers.image.title="AirQo Uganda Air Quality bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the AirQo Uganda air quality monitoring network and Kafka endpoints. It fetches air quality measurements and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/airqo-uganda/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV STATE_FILE="/mnt/fileshare/airqo_uganda_state.json"
ENV CONNECTION_STRING=""
ENV AIRQO_API_KEY=""

# Run the application
CMD ["python", "-m", "airqo_uganda"]
