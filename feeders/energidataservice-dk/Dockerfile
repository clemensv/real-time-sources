# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/energidataservice-dk"
LABEL org.opencontainers.image.title="Energi Data Service (Energinet) Denmark bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the Energi Data Service (Energinet) API for the Danish power system and Kafka endpoints. It fetches power system snapshots and spot prices and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/energidataservice-dk/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./energidataservice_dk_producer/energidataservice_dk_producer_data \
 && pip install ./energidataservice_dk_producer/energidataservice_dk_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV EDS_LAST_POLLED_FILE="/mnt/fileshare/eds_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "energidataservice_dk", "feed"]
