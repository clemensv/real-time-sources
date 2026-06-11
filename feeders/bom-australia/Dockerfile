FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/bom-australia"
LABEL org.opencontainers.image.title="BOM Australia Weather Observation bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges real-time weather observations from the Australian Bureau of Meteorology to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/bom-australia/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./bom_australia_producer/bom_australia_producer_data \
 && pip install --no-cache-dir ./bom_australia_producer/bom_australia_producer_kafka_producer \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "bom_australia", "feed"]
