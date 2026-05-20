FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/nextbus"
LABEL org.opencontainers.image.title="Nextbus bridge to Azure Event Hubs and Fabric Event Streams"
LABEL org.opencontainers.image.description="Bridge for the Nextbus/UMOIQ public XML feed for real-time transit vehicle positions, route configurations, schedules, and service messages."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/nextbus/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV FEED_CONNECTION_STRING=""
ENV FEED_EVENT_HUB_NAME=""
ENV REFERENCE_CONNECTION_STRING=""
ENV REFERENCE_EVENT_HUB_NAME=""
ENV AGENCY=""
ENV ROUTE="*"
ENV POLL_INTERVAL="10"
ENV BACKOFF_INTERVAL="0"

CMD ["python", "-m", "nextbus", "feed"]
