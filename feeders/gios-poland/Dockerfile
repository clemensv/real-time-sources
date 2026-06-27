# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/gios-poland"
LABEL org.opencontainers.image.title="GIOŚ Poland Air Quality bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality monitoring network and Kafka endpoints. It fetches station metadata, sensor reference data, hourly measurements, and air quality index values and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/gios-poland/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./gios_poland_producer/gios_poland_producer_data \
 && pip install ./gios_poland_producer/gios_poland_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV GIOS_LAST_POLLED_FILE="/mnt/fileshare/gios_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'gios_poland'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "gios_poland", "feed"]
