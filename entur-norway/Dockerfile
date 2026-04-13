FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources"
LABEL org.opencontainers.image.title="Entur Norway SIRI Bridge"
LABEL org.opencontainers.image.description="Entur Norway national real-time transit SIRI bridge to Apache Kafka"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/entur-norway/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir \
    ./entur_norway_producer/entur_norway_producer_data \
    && pip install --no-cache-dir \
    ./entur_norway_producer/entur_norway_producer_kafka_producer \
    && pip install --no-cache-dir -e .

CMD ["python", "-m", "entur_norway", "feed"]
