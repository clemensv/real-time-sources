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
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./nasa_firms_producer/nasa_firms_producer_data \
 && pip install ./nasa_firms_producer/nasa_firms_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV FIRMS_MAP_KEY=""
ENV LOG_LEVEL="INFO"

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'nasa_firms'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "nasa_firms", "feed"]