# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/fdsn-seismology"
LABEL org.opencontainers.image.title="FDSN Seismology → Kafka bridge"
LABEL org.opencontainers.image.description="Polls eight pre-configured FDSN Event service nodes for earthquake detections and publishes node reference records plus earthquake CloudEvents to Kafka-compatible endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/fdsn-seismology/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0

COPY . /app

RUN pip install --no-cache-dir ./fdsn_seismology_producer/fdsn_seismology_producer_data \
 && pip install --no-cache-dir ./fdsn_seismology_producer/fdsn_seismology_producer_kafka_producer \
 && pip install --no-cache-dir ./fdsn_seismology_core \
 && pip install --no-cache-dir ./fdsn_seismology_kafka

ENV CONNECTION_STRING=""
CMD ["python", "-m", "fdsn_seismology", "feed"]
