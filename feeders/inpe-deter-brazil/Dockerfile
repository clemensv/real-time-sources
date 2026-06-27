# Use an official Python runtime as a parent image
FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/inpe-deter-brazil"
LABEL org.opencontainers.image.title="INPE DETER Brazil deforestation alerts bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between INPE DETER deforestation alert feeds and Kafka endpoints. It fetches deforestation alerts from Amazon and Cerrado biomes and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/inpe-deter-brazil/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./inpe_deter_brazil_producer/inpe_deter_brazil_producer_data \
 && pip install ./inpe_deter_brazil_producer/inpe_deter_brazil_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'inpe_deter_brazil'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "inpe_deter_brazil", "feed"]
