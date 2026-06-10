# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/noaa-ndbc"
LABEL org.opencontainers.image.title="NOAA NDBC Buoy Observations bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the NOAA National Data Buoy Center (NDBC) latest observations and Kafka endpoints. It fetches buoy observations and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/noaa-ndbc/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./noaa_ndbc_producer/noaa_ndbc_producer_data \
 && pip install ./noaa_ndbc_producer/noaa_ndbc_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV NDBC_LAST_POLLED_FILE="/mnt/fileshare/ndbc_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "noaa_ndbc"]
