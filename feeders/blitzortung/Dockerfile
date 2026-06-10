FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/blitzortung"
LABEL org.opencontainers.image.title="Blitzortung lightning bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams live lightning strokes from the public LightningMaps / Blitzortung websocket feed to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/blitzortung/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./blitzortung_producer/blitzortung_producer_data \
 && pip install ./blitzortung_producer/blitzortung_producer_kafka_producer \
 && pip install .

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
