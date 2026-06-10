# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/cdec-reservoirs"
LABEL org.opencontainers.image.title="CDEC California Reservoirs bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the California Data Exchange Center (CDEC) reservoir data API to Kafka endpoints, emitting hourly storage, elevation, inflow, and outflow readings as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/cdec-reservoirs/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./cdec_reservoirs_producer/cdec_reservoirs_producer_data \
 && pip install ./cdec_reservoirs_producer/cdec_reservoirs_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "cdec_reservoirs", "feed"]
