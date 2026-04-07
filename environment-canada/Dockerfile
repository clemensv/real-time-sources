FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/environment-canada" \
      org.opencontainers.image.title="Environment Canada Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Environment Canada SWOB observations and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/environment-canada/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY environment_canada_producer/ environment_canada_producer/

RUN pip install --no-cache-dir \
    ./environment_canada_producer/environment_canada_producer_data \
    ./environment_canada_producer/environment_canada_producer_kafka_producer

COPY pyproject.toml .
COPY environment_canada/ environment_canada/

RUN pip install --no-cache-dir .

CMD ["python", "-m", "environment_canada", "feed"]
