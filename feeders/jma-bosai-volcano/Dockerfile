# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/jma-bosai-volcano"
LABEL org.opencontainers.image.title="JMA Bosai volcanic warnings bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between JMA Bosai volcanic warnings and eruption reports and Kafka-compatible endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/jma-bosai-volcano/CONTAINER.md"
LABEL org.opencontainers.image.license="Japanese government open data"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install jma_bosai_volcano_producer/jma_bosai_volcano_producer_data \
    && pip install jma_bosai_volcano_producer/jma_bosai_volcano_producer_kafka_producer \
 && pip install ./jma_bosai_volcano_core \
    && pip install .

ENV CONNECTION_STRING=""
ENV KAFKA_TOPIC="jma-bosai-volcano"
ENV POLLING_INTERVAL="60"
ENV VOLCANO_METADATA_REFRESH_HOURS="720"
ENV STATE_FILE="./state/jma-bosai-volcano.json"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'jma_bosai_volcano'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "jma_bosai_volcano", "feed"]
