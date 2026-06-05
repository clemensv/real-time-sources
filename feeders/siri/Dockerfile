# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/siri"
LABEL org.opencontainers.image.title="Generic SIRI → Apache Kafka bridge"
LABEL org.opencontainers.image.description="Polls configurable SIRI-compatible providers, extracts operator reference data and SIRI VehicleActivity telemetry, and forwards CloudEvents to Apache Kafka or any Kafka-compatible service."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/siri/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir ./siri_producer/siri_producer_data \
 && pip install --no-cache-dir ./siri_producer/siri_producer_kafka_producer \
 && pip install --no-cache-dir ./siri_core \
 && pip install --no-cache-dir ./siri_kafka

ENV CONNECTION_STRING=""
CMD ["python", "-m", "siri_kafka", "feed"]
