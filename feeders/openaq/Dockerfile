FROM python:3.10-slim
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources" \
      org.opencontainers.image.title="OpenAQ Kafka feeder" \
      org.opencontainers.image.description="Polls OpenAQ API v3 global air-quality locations, sensors, and latest measurements and emits CloudEvents to Kafka/Event Hubs." \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/openaq/CONTAINER.md" \
      org.opencontainers.image.license="MIT"
ENV PYTHONUNBUFFERED=1
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ./openaq_producer/openaq_producer_data \
 && pip install --no-cache-dir ./openaq_producer/openaq_producer_kafka_producer \
 && pip install --no-cache-dir ./openaq_core \
 && pip install --no-cache-dir ./openaq_kafka
CMD ["python", "-m", "openaq", "feed"]


