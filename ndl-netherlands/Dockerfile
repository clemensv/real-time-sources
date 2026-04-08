FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/ndl-netherlands"
LABEL org.opencontainers.image.title="NDW Netherlands Road Traffic Bridge"
LABEL org.opencontainers.image.description="Bridges Dutch NDW road traffic data (speed, travel time, situations) to Kafka via CloudEvents"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/ndl-netherlands/CONTAINER.md"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV MEASUREMENTS_TOPIC=ndl-traffic
ENV SITUATIONS_TOPIC=ndl-traffic-situations
ENV POLLING_INTERVAL=60

CMD ["python", "-m", "ndl_netherlands"]
