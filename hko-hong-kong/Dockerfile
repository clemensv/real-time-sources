FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/hko-hong-kong" \
      org.opencontainers.image.title="HKO Hong Kong Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Hong Kong Observatory weather data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/hko-hong-kong/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY hko_hong_kong_producer/ hko_hong_kong_producer/

RUN pip install --no-cache-dir \
    ./hko_hong_kong_producer/hko_hong_kong_producer_data \
    ./hko_hong_kong_producer/hko_hong_kong_producer_kafka_producer

COPY pyproject.toml .
COPY hko_hong_kong/ hko_hong_kong/

RUN pip install --no-cache-dir .

CMD ["python", "-m", "hko_hong_kong", "feed"]
