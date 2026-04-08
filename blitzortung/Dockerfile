FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/blitzortung"
LABEL org.opencontainers.image.title="Blitzortung lightning bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams live lightning strokes from the public LightningMaps / Blitzortung websocket feed to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/blitzortung/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV BLITZORTUNG_WS_URLS="wss://live.lightningmaps.org:443/,wss://live2.lightningmaps.org:443/"
ENV BLITZORTUNG_BBOX="90,180,-90,-180"
ENV BLITZORTUNG_INCLUDE_STATIONS="true"
ENV BLITZORTUNG_SOURCE_MASK="4"
ENV BLITZORTUNG_FLUSH_INTERVAL="250"
ENV BLITZORTUNG_MAX_RETRY_DELAY="60"
ENV BLITZORTUNG_STATE_FILE="/tmp/blitzortung_state.json"
ENV LOG_LEVEL="INFO"

CMD ["python", "-m", "blitzortung", "feed"]
