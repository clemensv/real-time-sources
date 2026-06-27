# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/fienta"
LABEL org.opencontainers.image.title="Fienta Public Events bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the Fienta public events API and Kafka endpoints. It polls public ticketed events in Europe and forwards both event reference data and sale-status change events to the configured Kafka topic."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/fienta/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./fienta_producer/fienta_producer_data && \
    pip install ./fienta_producer/fienta_producer_kafka_producer && \
    pip install .

# Define environment variables (default values)
ENV FIENTA_STATE_FILE="/mnt/fileshare/fienta_state.json"
ENV CONNECTION_STRING=""

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'fienta'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "fienta", "feed"]
