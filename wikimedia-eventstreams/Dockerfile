FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/wikimedia-eventstreams"
LABEL org.opencontainers.image.title="Wikimedia EventStreams bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges Wikimedia's public recentchange EventStreams feed into Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/wikimedia-eventstreams/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

CMD ["python", "-m", "wikimedia_eventstreams", "feed"]
