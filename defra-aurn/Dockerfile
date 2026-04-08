FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/defra-aurn"
LABEL org.opencontainers.image.title="Defra AURN air quality bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the UK Defra AURN SOS API and Kafka/Event Hubs/Fabric Event Streams. Emits hourly air quality observations as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/defra-aurn/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install defra_aurn_producer/defra_aurn_producer_data && \
    pip install defra_aurn_producer/defra_aurn_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
CMD ["python", "-m", "defra_aurn", "feed"]
