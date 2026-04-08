FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/irceline-belgium"
LABEL org.opencontainers.image.title="IRCELINE Belgium air quality bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the IRCELINE Belgium SOS API and Kafka/Event Hubs/Fabric Event Streams. Emits hourly air quality observations as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/irceline-belgium/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install irceline_belgium_producer/irceline_belgium_producer_data && \
    pip install irceline_belgium_producer/irceline_belgium_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
CMD ["python", "-m", "irceline_belgium", "feed"]
