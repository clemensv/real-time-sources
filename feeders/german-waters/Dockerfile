# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/german-waters"
LABEL org.opencontainers.image.title="German Waters bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Aggregates water level data from German state flood services and forwards it to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/german-waters/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./german_waters_producer/german_waters_producer_data \
 && pip install ./german_waters_producer/german_waters_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV PROVIDERS=""
ENV EXCLUDE_PROVIDERS=""

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'german_waters'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "german_waters", "feed"]
