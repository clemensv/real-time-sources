# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/ireland-opw-waterlevel"
LABEL org.opencontainers.image.title="Ireland OPW waterlevel.ie bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the Ireland OPW waterlevel.ie GeoJSON API and Kafka endpoints, emitting real-time water level, temperature, and voltage data from Irish hydrometric stations."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/ireland-opw-waterlevel/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./ireland_opw_waterlevel_producer/ireland_opw_waterlevel_producer_data \
 && pip install ./ireland_opw_waterlevel_producer/ireland_opw_waterlevel_producer_kafka_producer \
 && pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""

# Run the application
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'ireland_opw_waterlevel'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "ireland_opw_waterlevel", "feed"]
