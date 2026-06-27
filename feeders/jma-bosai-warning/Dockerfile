FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/jma-bosai-warning"
LABEL org.opencontainers.image.title="JMA Bosai weather warnings and tsunami alerts bridge"
LABEL org.opencontainers.image.description="Polls Japan Meteorological Agency Bosai weather warning and tsunami alert feeds and forwards CloudEvents to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/jma-bosai-warning/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./jma_bosai_warning_producer/jma_bosai_warning_producer_data \
    && pip install ./jma_bosai_warning_producer/jma_bosai_warning_producer_kafka_producer \
    && pip install .

ENV CONNECTION_STRING=""
ENV KAFKA_TOPIC_WARNING="jma-bosai-warning"
ENV KAFKA_TOPIC_TSUNAMI="jma-bosai-tsunami"
ENV POLLING_INTERVAL_WARNING="60"
ENV POLLING_INTERVAL_TSUNAMI="30"
ENV OFFICE_METADATA_REFRESH_HOURS="720"
ENV KAFKA_ENABLE_TLS="true"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'jma_bosai_warning'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "jma_bosai_warning", "feed"]
