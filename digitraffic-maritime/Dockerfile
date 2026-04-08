FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/digitraffic-maritime"
LABEL org.opencontainers.image.title="Digitraffic Marine bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams Digitraffic Marine AIS and port-call data to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/digitraffic-maritime/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV DIGITRAFFIC_SUBSCRIBE="location,metadata"
ENV DIGITRAFFIC_FILTER_MMSI=""
ENV DIGITRAFFIC_FLUSH_INTERVAL="1000"

CMD ["python", "-m", "digitraffic_maritime", "stream"]
