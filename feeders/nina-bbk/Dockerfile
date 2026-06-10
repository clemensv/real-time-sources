FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources"
LABEL org.opencontainers.image.title="NINA/BBK German Civil Protection Warnings Bridge"
LABEL org.opencontainers.image.description="Bridges civil protection warnings from Germany's NINA/BBK system to Kafka/Event Hubs as CloudEvents"

WORKDIR /app

COPY . /app/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    nina_bbk_producer/nina_bbk_producer_data \
    nina_bbk_producer/nina_bbk_producer_kafka_producer \
    .

CMD ["python", "-m", "nina_bbk", "feed"]
