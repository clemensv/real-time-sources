FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/geosphere-austria"
LABEL org.opencontainers.image.title="GeoSphere Austria TAWES Weather Bridge"
LABEL org.opencontainers.image.description="Bridges 10-minute TAWES weather observations from GeoSphere Austria into Kafka as CloudEvents"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/geosphere-austria/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY geosphere_austria_producer/geosphere_austria_producer_data /app/geosphere_austria_producer_data
COPY geosphere_austria_producer/geosphere_austria_producer_kafka_producer /app/geosphere_austria_producer_kafka_producer

RUN pip install --no-cache-dir /app/geosphere_austria_producer_data && \
    pip install --no-cache-dir /app/geosphere_austria_producer_kafka_producer

COPY . /app
RUN pip install --no-cache-dir -e .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL=600
ENV STATION_REFRESH_INTERVAL=86400

ENTRYPOINT ["python", "-m", "geosphere_austria", "feed"]
