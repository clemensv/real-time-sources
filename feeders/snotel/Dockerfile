# Use an official Python runtime as a parent image
FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/snotel"
LABEL org.opencontainers.image.title="USDA NRCS SNOTEL Snow bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between USDA NRCS SNOTEL stations and Kafka endpoints. It fetches hourly snow and weather observations and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/snotel/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the generated producer packages first, then the feeder package.
# The bridge imports snotel_producer_data / snotel_producer_kafka_producer
# at runtime, so they must be present before the wheel is installed.
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./snotel_producer/snotel_producer_data \
    && pip install --no-cache-dir ./snotel_producer/snotel_producer_kafka_producer \
    && pip install --no-cache-dir .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

# Run the application
CMD ["python", "-m", "snotel", "feed"]
