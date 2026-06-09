FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/laqn-london"
LABEL org.opencontainers.image.title="LAQN London Air Quality Network bridge to Kafka"
LABEL org.opencontainers.image.description="This container bridges the London Air Quality Network (LAQN) API operated by King's College London to Kafka, emitting CloudEvents for site metadata, species definitions, hourly measurements, and Daily Air Quality Index (DAQI) values."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/laqn-london/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install laqn_london_producer/laqn_london_producer_data && \
    pip install laqn_london_producer/laqn_london_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "laqn_london", "feed"]
