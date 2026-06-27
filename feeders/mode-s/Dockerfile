# Use an official Python runtime as a parent image
FROM python:3.11-slim

LABEL org.opencontainers.image.source = "https://github.com/clemensv/real-time-sources/tree/main/mode_s"
LABEL org.opencontainers.image.title = "Mode-S Data Poller"
LABEL org.opencontainers.image.description = "This container polls ADS-B data from dump1090 and sends it to Kafka endpoints."
LABEL org.opencontainers.image.documentation = "https://github.com/clemensv/real-time-sources/blob/main/mode_s/CONTAINER.md"
LABEL org.opencontainers.image.license = "MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./mode_s_producer/mode_s_producer_data \
 && pip install ./mode_s_producer/mode_s_producer_kafka_producer \
 && pip install ./mode_s_core \
 && pip install .

# Define environment variables (default values)
ENV DUMP1090_HOST="localhost"
ENV DUMP1090_PORT="30005"
ENV REF_LAT="0"
ENV REF_LON="0"
ENV STATIONID="station1"
ENV KAFKA_BOOTSTRAP_SERVERS=""
ENV KAFKA_TOPIC=""
ENV SASL_USERNAME=""
ENV SASL_PASSWORD=""
ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="60"
ENV LOG_LEVEL="INFO"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'mode_s_kafka_bridge'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

# Run the application
CMD ["mode_s_kafka_bridge", "feed"]
