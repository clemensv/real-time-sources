FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/uba-airdata"
LABEL org.opencontainers.image.title="UBA Germany air quality bridge to Kafka"
LABEL org.opencontainers.image.description="This container bridges the Umweltbundesamt Germany national air quality API to Kafka, emitting CloudEvents for station metadata, component definitions, and hourly measurements."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/uba-airdata/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install uba_airdata_producer/uba_airdata_producer_data && \
    pip install uba_airdata_producer/uba_airdata_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "uba_airdata", "feed"]
