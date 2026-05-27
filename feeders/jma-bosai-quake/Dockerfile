FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/jma-bosai-quake"
LABEL org.opencontainers.image.title="JMA Bosai earthquake bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Polls JMA Bosai earthquake and seismic intensity reports and forwards new reports to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/jma-bosai-quake/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install ./jma_bosai_quake_producer/jma_bosai_quake_producer_data \
    && pip install ./jma_bosai_quake_producer/jma_bosai_quake_producer_kafka_producer \
    && pip install .

ENV CONNECTION_STRING=""
ENV KAFKA_TOPIC="jma-bosai-quake"
ENV POLLING_INTERVAL="60"
ENV STATE_FILE=".\\state\\jma-bosai-quake.json"

CMD ["python", "-m", "jma_bosai_quake", "feed"]
