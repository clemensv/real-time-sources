# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/uk-bods-siri"
LABEL org.opencontainers.image.title="UK BODS SIRI → Apache Kafka bridge"
LABEL org.opencontainers.image.description="Polls the UK Department for Transport Bus Open Data Service AVL bulk archive, extracts operator reference data and live SIRI-VM vehicle positions, and forwards CloudEvents to Apache Kafka or any Kafka-compatible service."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/uk-bods-siri/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir ./uk_bods_siri_producer/uk_bods_siri_producer_data \
 && pip install --no-cache-dir ./uk_bods_siri_producer/uk_bods_siri_producer_kafka_producer \
 && pip install --no-cache-dir ./uk_bods_siri_core \
 && pip install --no-cache-dir ./uk_bods_siri_kafka

ENV CONNECTION_STRING=""
CMD ["python", "-m", "uk_bods_siri_kafka", "feed"]
