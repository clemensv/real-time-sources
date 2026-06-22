FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/aisstream"
LABEL org.opencontainers.image.title="AISstream.io bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams global AIS vessel tracking data from AISstream.io to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/aisstream/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./aisstream_producer/aisstream_producer_data \
 && pip install --no-cache-dir ./aisstream_producer/aisstream_producer_kafka_producer \
 && pip install --no-cache-dir ./aisstream_core \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV AISSTREAM_API_KEY=""
ENV AISSTREAM_BOUNDING_BOXES="-90,-180,90,180"
ENV AISSTREAM_MESSAGE_TYPES=""
ENV AISSTREAM_FILTER_MMSI=""
ENV AISSTREAM_FLUSH_INTERVAL="1000"

CMD ["python", "-m", "aisstream", "stream"]
