FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/king-county-marine"
LABEL org.opencontainers.image.title="King County marine bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for current King County marine buoy and mooring telemetry datasets."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/king-county-marine/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV KING_COUNTY_MARINE_STATE_FILE="/mnt/fileshare/king_county_marine_state.json"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "king_county_marine"]
