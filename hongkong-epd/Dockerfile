FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/hongkong-epd" \
      org.opencontainers.image.title="Hong Kong EPD AQHI Bridge" \
      org.opencontainers.image.description="Bridge between Hong Kong EPD Air Quality Health Index data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/hongkong-epd/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY hongkong_epd_producer/ hongkong_epd_producer/

RUN pip install --no-cache-dir \
    ./hongkong_epd_producer/hongkong_epd_producer_data \
    ./hongkong_epd_producer/hongkong_epd_producer_kafka_producer

COPY pyproject.toml .
COPY hongkong_epd/ hongkong_epd/

RUN pip install --no-cache-dir .

CMD ["python", "-m", "hongkong_epd", "feed"]
