FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/kystverket-ais"
LABEL org.opencontainers.image.title="Kystverket AIS bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams Norwegian AIS vessel tracking data from Kystverket to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/kystverket-ais/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV AIS_TCP_HOST="153.44.253.27"
ENV AIS_TCP_PORT="5631"
ENV AIS_MESSAGE_TYPES="1,2,3,5,18,19,24,21"
ENV AIS_FLUSH_INTERVAL="1000"

CMD ["python", "-m", "kystverket_ais", "stream"]
