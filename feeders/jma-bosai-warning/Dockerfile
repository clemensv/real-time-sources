FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/jma-bosai-warning"
LABEL org.opencontainers.image.title="JMA Bosai weather warnings and tsunami alerts bridge"
LABEL org.opencontainers.image.description="Polls Japan Meteorological Agency Bosai weather warning and tsunami alert feeds and forwards CloudEvents to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/jma-bosai-warning/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install ./jma_bosai_warning_producer/jma_bosai_warning_producer_data \
    && pip install ./jma_bosai_warning_producer/jma_bosai_warning_producer_kafka_producer \
    && pip install .

ENV CONNECTION_STRING=""
ENV KAFKA_TOPIC_WARNING="jma-bosai-warning"
ENV KAFKA_TOPIC_TSUNAMI="jma-bosai-tsunami"
ENV POLLING_INTERVAL_WARNING="60"
ENV POLLING_INTERVAL_TSUNAMI="30"
ENV OFFICE_METADATA_REFRESH_HOURS="720"
ENV KAFKA_ENABLE_TLS="true"

CMD ["python", "-m", "jma_bosai_warning", "feed"]
