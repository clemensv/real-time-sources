FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/tfl-road-traffic"
LABEL org.opencontainers.image.title="TfL Road Traffic bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges road corridor status and disruption data from the Transport for London (TfL) Unified API to Kafka endpoints, emitting CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/tfl-road-traffic/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir tfl_road_traffic_producer/tfl_road_traffic_producer_data && \
    pip install --no-cache-dir tfl_road_traffic_producer/tfl_road_traffic_producer_kafka_producer && \
    pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="60"
ENV REFERENCE_REFRESH_INTERVAL="3600"

CMD ["python", "-m", "tfl_road_traffic", "feed"]
