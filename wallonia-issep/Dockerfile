FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/wallonia-issep"
LABEL org.opencontainers.image.title="Wallonia ISSeP air quality bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Wallonia ISSeP Opendatasoft API and Kafka/Event Hubs/Fabric Event Streams. Emits near-real-time air quality observations as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/wallonia-issep/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install wallonia_issep_producer/wallonia_issep_producer_data && \
    pip install wallonia_issep_producer/wallonia_issep_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
CMD ["python", "-m", "wallonia_issep", "feed"]
