# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/gbfs-bikeshare"
LABEL org.opencontainers.image.title="GBFS bikeshare -> Apache Kafka bridge"
LABEL org.opencontainers.image.description="Polls one or more user-configured GBFS bikeshare auto-discovery feeds and publishes reference and telemetry CloudEvents to Kafka-compatible brokers."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/gbfs-bikeshare/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0
COPY . /app

RUN pip install --no-cache-dir ./gbfs_bikeshare_producer/gbfs_bikeshare_producer_data \
 && pip install --no-cache-dir ./gbfs_bikeshare_producer/gbfs_bikeshare_producer_kafka_producer \
 && pip install --no-cache-dir ./gbfs_bikeshare_core \
 && pip install --no-cache-dir ./gbfs_bikeshare_kafka

ENV CONNECTION_STRING=""
ENV GBFS_FEEDS=""
ENV GBFS_API_KEY=""
ENV GBFS_API_KEY_PARAM="acl:consumerKey"
ENV POLL_INTERVAL="60"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'gbfs_bikeshare'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "gbfs_bikeshare", "feed"]
