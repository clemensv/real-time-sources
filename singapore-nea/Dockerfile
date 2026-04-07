FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/singapore-nea" \
      org.opencontainers.image.title="Singapore NEA Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Singapore NEA weather data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/singapore-nea/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY singapore_nea_producer/ singapore_nea_producer/

RUN pip install --no-cache-dir \
    ./singapore_nea_producer/singapore_nea_producer_data \
    ./singapore_nea_producer/singapore_nea_producer_kafka_producer

COPY pyproject.toml .
COPY singapore_nea/ singapore_nea/

RUN pip install --no-cache-dir .

CMD ["python", "-m", "singapore_nea", "feed"]
