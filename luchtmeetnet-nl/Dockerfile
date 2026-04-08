FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/luchtmeetnet-nl"
LABEL org.opencontainers.image.title="Luchtmeetnet Netherlands air quality bridge to Kafka"
LABEL org.opencontainers.image.description="This container bridges the Luchtmeetnet Netherlands national air quality monitoring API to Kafka, emitting CloudEvents for station metadata, component definitions, hourly measurements, and air quality index (LKI) values."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/luchtmeetnet-nl/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install luchtmeetnet_nl_producer/luchtmeetnet_nl_producer_data && \
    pip install luchtmeetnet_nl_producer/luchtmeetnet_nl_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "luchtmeetnet_nl", "feed"]
