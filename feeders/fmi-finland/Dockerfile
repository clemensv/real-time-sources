FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/fmi-finland"
LABEL org.opencontainers.image.title="FMI Finland air quality bridge to Kafka"
LABEL org.opencontainers.image.description="Bridges Finnish Meteorological Institute air quality observations from OGC WFS into Kafka and CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/fmi-finland/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./fmi_finland_producer/fmi_finland_producer_data && \
    pip install ./fmi_finland_producer/fmi_finland_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="3600"
ENV STATION_REFRESH_INTERVAL="86400"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'fmi_finland'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "fmi_finland", "feed"]
