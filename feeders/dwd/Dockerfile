# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/dwd"
LABEL org.opencontainers.image.title="DWD Open Data bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Aggregates weather observations, station metadata, and alerts from the DWD Climate Data Center and forwards them to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/dwd/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# libeccodes-dev provides the GRIB2 decoder used by the optional icond2_grid module.
RUN set -eux; \
    for i in 1 2 3 4 5; do \
        apt-get update && \
        apt-get install -y --no-install-recommends --fix-missing \
            libeccodes-dev \
        && break || \
        { echo "apt attempt $i failed, retrying..."; sleep $((i*5)); }; \
    done; \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./dwd_producer/dwd_producer_data \
 && pip install ./dwd_producer/dwd_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV DWD_MODULES="station_obs_10min,weather_alerts,station_metadata"
ENV DWD_MODULES_DISABLED=""
ENV POLLING_INTERVAL=""
ENV STATE_FILE="/mnt/fileshare/dwd_state.json"

# Run the application
CMD ["python", "-m", "dwd", "feed"]
