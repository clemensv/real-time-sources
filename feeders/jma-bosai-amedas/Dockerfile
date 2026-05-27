# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/jma-bosai-amedas"
LABEL org.opencontainers.image.title="JMA Bosai AMeDAS bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges Japan Meteorological Agency Bosai AMeDAS station metadata and ten-minute observations to configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/jma-bosai-amedas/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install -e ./jma_bosai_amedas_producer/jma_bosai_amedas_producer_data \
    && pip install -e ./jma_bosai_amedas_producer/jma_bosai_amedas_producer_kafka_producer \
    && pip install -e .

ENV CONNECTION_STRING=""
ENV KAFKA_TOPIC="jma-bosai-amedas"
ENV POLLING_INTERVAL="600"
ENV STATION_METADATA_REFRESH_HOURS="168"
ENV STATE_FILE="./state/jma-bosai-amedas.json"

CMD ["python", "-m", "jma_bosai_amedas", "feed"]
