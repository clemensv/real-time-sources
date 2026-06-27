FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/singapore-nea" \
      org.opencontainers.image.title="Singapore NEA Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Singapore NEA weather data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/singapore-nea/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY singapore_nea_producer/ singapore_nea_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./singapore_nea_producer/singapore_nea_producer_data \
    ./singapore_nea_producer/singapore_nea_producer_kafka_producer

COPY pyproject.toml .
COPY singapore_nea_core/ singapore_nea_core/
COPY singapore_nea/ singapore_nea/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./singapore_nea_core .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'singapore_nea'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "singapore_nea", "feed"]
