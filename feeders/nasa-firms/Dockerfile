# Use an official Python runtime as a parent image
FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/nasa-firms"
LABEL org.opencontainers.image.title="NASA FIRMS active-fire bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the NASA FIRMS (Fire Information for Resource Management System) Area API and Kafka endpoints. Polls global VIIRS and MODIS active-fire detections and forwards them as CloudEvents to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/nasa-firms/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV FIRMS_MAP_KEY=""
ENV LOG_LEVEL="INFO"

# Run the application
CMD ["python", "-m", "nasa_firms", "feed"]