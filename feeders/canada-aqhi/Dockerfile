FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/canada-aqhi"
LABEL org.opencontainers.image.title="Canada AQHI bridge to Kafka"
LABEL org.opencontainers.image.description="Bridges Canada Air Quality Health Index observations and forecasts from Environment and Climate Change Canada to Kafka and CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/canada-aqhi/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"
LABEL org.opencontainers.image.version="0.1.1"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./canada_aqhi_producer/canada_aqhi_producer_data && \
    pip install ./canada_aqhi_producer/canada_aqhi_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="3600"
ENV REFERENCE_REFRESH_INTERVAL="86400"
ENV PROVINCES="AB,BC,MB,NB,NL,NS,NT,NU,ON,PE,QC,SK,YT"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'canada_aqhi'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "canada_aqhi", "feed"]
