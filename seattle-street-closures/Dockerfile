FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/seattle-street-closures"
LABEL org.opencontainers.image.title="Seattle street closures bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for the City of Seattle street closures dataset."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/seattle-street-closures/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV SEATTLE_STREET_CLOSURES_STATE_FILE="/mnt/fileshare/seattle_street_closures_state.json"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "seattle_street_closures"]
