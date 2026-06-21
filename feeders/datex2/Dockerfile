# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/datex2" \
      org.opencontainers.image.title="DATEX II -> Kafka bridge" \
      org.opencontainers.image.description="Polls configurable DATEX II XML endpoints and publishes traffic situation, measurement-site, and traffic measurement CloudEvents." \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/datex2/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1 SETUPTOOLS_SCM_PRETEND_VERSION=0 DATEX2_ENDPOINTS="" DATEX2_MOCK="false" POLLING_INTERVAL="300"
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ./datex2_producer/datex2_producer_data \
 && pip install --no-cache-dir ./datex2_producer/datex2_producer_kafka_producer \
 && pip install --no-cache-dir ./datex2_core \
 && pip install --no-cache-dir ./datex2_kafka
CMD ["python", "-m", "datex2_kafka", "feed"]

