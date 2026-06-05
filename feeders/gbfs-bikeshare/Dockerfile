# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/gbfs-bikeshare"
LABEL org.opencontainers.image.title="GBFS bikeshare -> Apache Kafka bridge"
LABEL org.opencontainers.image.description="Polls one or more user-configured GBFS bikeshare auto-discovery feeds and publishes reference and telemetry CloudEvents to Kafka-compatible brokers."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/gbfs-bikeshare/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir ./gbfs_bikeshare_producer/gbfs_bikeshare_producer_data \
 && pip install --no-cache-dir ./gbfs_bikeshare_producer/gbfs_bikeshare_producer_kafka_producer \
 && pip install --no-cache-dir ./gbfs_bikeshare_core \
 && pip install --no-cache-dir ./gbfs_bikeshare_kafka

ENV CONNECTION_STRING=""
ENV GBFS_FEEDS=""
ENV POLL_INTERVAL="60"

CMD ["python", "-m", "gbfs_bikeshare", "feed"]
