# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/hubeau-hydrometrie"
LABEL org.opencontainers.image.title="Hub'Eau Hydrométrie API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the French Hub'Eau Hydrométrie API and Kafka endpoints. It fetches hydrometric data and forwards it to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/hubeau-hydrometrie/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./hubeau_hydrometrie_producer/hubeau_hydrometrie_producer_data \
 && pip install ./hubeau_hydrometrie_producer/hubeau_hydrometrie_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'hubeau_hydrometrie'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "hubeau_hydrometrie", "feed"]
