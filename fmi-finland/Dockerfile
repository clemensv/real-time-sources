FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/fmi-finland"
LABEL org.opencontainers.image.title="FMI Finland air quality bridge to Kafka"
LABEL org.opencontainers.image.description="Bridges Finnish Meteorological Institute air quality observations from OGC WFS into Kafka and CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/fmi-finland/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install ./fmi_finland_producer/fmi_finland_producer_data && \
    pip install ./fmi_finland_producer/fmi_finland_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="3600"
ENV STATION_REFRESH_INTERVAL="86400"

CMD ["python", "-m", "fmi_finland", "feed"]
