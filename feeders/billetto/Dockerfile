# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/billetto"
LABEL org.opencontainers.image.title="Billetto Public Events bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the Billetto public events REST API to Apache Kafka, Azure Event Hubs, and Fabric Event Streams. It polls the Billetto API for new and updated events and emits them as CloudEvents to the configured Kafka topic."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/billetto/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./billetto_producer/billetto_producer_data && \
    pip install --no-cache-dir ./billetto_producer/billetto_producer_kafka_producer && \
    pip install --no-cache-dir .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV BILLETTO_API_KEYPAIR=""
ENV BILLETTO_BASE_URL="https://billetto.dk"
ENV KAFKA_TOPIC="billetto-events"
ENV POLLING_INTERVAL="300"
ENV LOG_LEVEL="INFO"

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'billetto'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "billetto", "feed"]
