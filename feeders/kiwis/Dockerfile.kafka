# syntax=docker/dockerfile:1.6
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/kiwis"
LABEL org.opencontainers.image.title="KiWIS -> Kafka bridge"
LABEL org.opencontainers.image.description="Polls configurable KISTERS KiWIS hydrological REST endpoints and publishes station, timeseries metadata, and observation CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/kiwis/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0
COPY . /app
RUN pip install --no-cache-dir ./kiwis_producer/kiwis_producer_data \
 && pip install --no-cache-dir ./kiwis_producer/kiwis_producer_kafka_producer \
 && pip install --no-cache-dir ./kiwis_core \
 && pip install --no-cache-dir ./kiwis_kafka
ENV KIWIS_ENDPOINTS=""
ENV KIWIS_MOCK="false"
ENV POLLING_INTERVAL="300"
CMD ["python", "-m", "kiwis_kafka", "feed"]
