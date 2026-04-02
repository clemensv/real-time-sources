FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/aisstream"
LABEL org.opencontainers.image.title="AISstream.io bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams global AIS vessel tracking data from AISstream.io to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/aisstream/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV AISSTREAM_API_KEY=""
ENV AISSTREAM_BOUNDING_BOXES="-90,-180,90,180"
ENV AISSTREAM_MESSAGE_TYPES=""
ENV AISSTREAM_FILTER_MMSI=""
ENV AISSTREAM_FLUSH_INTERVAL="1000"

CMD ["python", "-m", "aisstream", "stream"]
