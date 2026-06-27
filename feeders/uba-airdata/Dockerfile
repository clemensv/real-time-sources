FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/uba-airdata"
LABEL org.opencontainers.image.title="UBA Germany air quality bridge to Kafka"
LABEL org.opencontainers.image.description="This container bridges the Umweltbundesamt Germany national air quality API to Kafka, emitting CloudEvents for station metadata, component definitions, and hourly measurements."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/uba-airdata/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install uba_airdata_producer/uba_airdata_producer_data && \
    pip install uba_airdata_producer/uba_airdata_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'uba_airdata'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "uba_airdata", "feed"]
