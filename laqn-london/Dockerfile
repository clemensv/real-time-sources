FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/laqn-london"
LABEL org.opencontainers.image.title="LAQN London Air Quality Network bridge to Kafka"
LABEL org.opencontainers.image.description="This container bridges the London Air Quality Network (LAQN) API operated by King's College London to Kafka, emitting CloudEvents for site metadata, species definitions, hourly measurements, and Daily Air Quality Index (DAQI) values."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/laqn-london/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install laqn_london_producer/laqn_london_producer_data && \
    pip install laqn_london_producer/laqn_london_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "laqn_london", "feed"]
