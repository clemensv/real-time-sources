FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/wikimedia-osm-diffs"
LABEL org.opencontainers.image.title="OpenStreetMap Minutely Diffs bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges OpenStreetMap minutely replication diffs into Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/wikimedia-osm-diffs/CONTAINER.md"
LABEL org.opencontainers.image.license="ODbL-1.0"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

CMD ["python", "-m", "wikimedia_osm_diffs", "feed"]
