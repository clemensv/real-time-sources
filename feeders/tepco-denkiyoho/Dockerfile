FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/tepco-denkiyoho"
LABEL org.opencontainers.image.title="TEPCO Denki Yoho bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for TEPCO Electricity Supply and Demand (Denki Yoho) Shift-JIS CSV data to Kafka, Event Hubs, and Fabric Event Streams."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/tepco-denkiyoho/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./tepco_denkiyoho_producer/tepco_denkiyoho_producer_data \
    && pip install ./tepco_denkiyoho_producer/tepco_denkiyoho_producer_kafka_producer \
    && pip install .

ENV CONNECTION_STRING=""
ENV KAFKA_TOPIC="tepco-denkiyoho"
ENV POLLING_INTERVAL="300"
ENV STATE_FILE="./state/tepco-denkiyoho.json"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'tepco_denkiyoho'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "tepco_denkiyoho", "feed"]
