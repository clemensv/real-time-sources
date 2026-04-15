FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/nws-forecasts"
LABEL org.opencontainers.image.title="NWS forecast zone bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for NWS forecast zones, land-zone forecasts, and marine forecast bulletins."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/nws-forecasts/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV NWS_FORECAST_ZONES="WAZ312,WAZ315,WAZ316,WAZ317,PZZ130,PZZ131,PZZ132,PZZ133,PZZ134,PZZ135"
ENV NWS_FORECAST_STATE_FILE="/mnt/fileshare/nws_forecasts_state.json"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "nws_forecasts"]
