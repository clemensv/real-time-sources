FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/kmi-belgium" \
      org.opencontainers.image.title="KMI Belgium Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between KMI/RMI automatic weather station observations and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/kmi-belgium/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY kmi_belgium_producer/ kmi_belgium_producer/

RUN pip install --no-cache-dir \
    ./kmi_belgium_producer/kmi_belgium_producer_data \
    ./kmi_belgium_producer/kmi_belgium_producer_kafka_producer

COPY pyproject.toml .
COPY kmi_belgium/ kmi_belgium/

RUN pip install --no-cache-dir .

CMD ["python", "-m", "kmi_belgium", "feed"]
