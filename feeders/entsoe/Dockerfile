FROM python:3.10-slim
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/entsoe" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/entsoe/CONTAINER.md" \
      org.opencontainers.image.license="MIT" \
      org.opencontainers.image.title="ENTSO-E Kafka feeder" \
      org.opencontainers.image.description="Publishes ENTSO-E Transparency Platform market, load, generation and cross-border flow CloudEvents to Kafka-compatible endpoints."
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir 'avro>=1.11.3' \
 && pip install --no-cache-dir ./entsoe_producer/entsoe_producer_data \
 && pip install --no-cache-dir ./entsoe_producer/entsoe_producer_kafka_producer \
 && pip install --no-cache-dir ./entsoe_core \
 && pip install --no-cache-dir ./entsoe_kafka
ENV STATE_FILE="/mnt/fileshare/entsoe_state.json" CONNECTION_STRING="" ENTSOE_SECURITY_TOKEN=""
CMD ["python", "-m", "entsoe_kafka", "feed"]
