# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/usgs-geomag"
LABEL org.opencontainers.image.title="USGS Geomagnetism Program bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the USGS Geomagnetism Program real-time geomagnetic field data and Kafka endpoints. It fetches 1-minute variation data from 14 US observatories and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/usgs-geomag/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./usgs_geomag_producer/usgs_geomag_producer_data \
 && pip install ./usgs_geomag_producer/usgs_geomag_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV GEOMAG_LAST_POLLED_FILE="/mnt/fileshare/usgs_geomag_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "usgs_geomag", "feed"]
