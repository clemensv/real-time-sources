FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/ndw-road-traffic"
LABEL org.opencontainers.image.title="NDW Netherlands Road Traffic Bridge"
LABEL org.opencontainers.image.description="Bridges Dutch NDW road traffic data (speed, travel time, DRIP, MSI, situations) to Kafka via CloudEvents"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/ndw-road-traffic/CONTAINER.md"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ndw_road_traffic_producer/ndw_road_traffic_producer_data && \
    pip install --no-cache-dir ndw_road_traffic_producer/ndw_road_traffic_producer_kafka_producer && \
    pip install --no-cache-dir .

ENV KAFKA_TOPIC=ndw-road-traffic
ENV POLLING_INTERVAL=60

CMD ["python", "-m", "ndw_road_traffic"]
