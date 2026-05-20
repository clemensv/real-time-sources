FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/xceed"
LABEL org.opencontainers.image.title="Xceed nightlife events bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Xceed Open Event API and Kafka endpoints. Polls publicly available European nightlife and live-entertainment events, emitting event schedules and ticket-availability updates as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/xceed/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "xceed", "feed"]
