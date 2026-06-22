FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/nws-forecasts"
LABEL org.opencontainers.image.title="NWS forecast zone bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for NWS forecast zones, land-zone forecasts, and marine forecast bulletins."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/nws-forecasts/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./nws_forecasts_producer/nws_forecasts_producer_data \
 && pip install ./nws_forecasts_producer/nws_forecasts_producer_kafka_producer \
 && pip install ./nws_forecasts_core \
 && pip install .

ENV NWS_FORECAST_ZONES="WAZ312,WAZ315,WAZ316,WAZ317,PZZ130,PZZ131,PZZ132,PZZ133,PZZ134,PZZ135"
ENV NWS_FORECAST_STATE_FILE="/mnt/fileshare/nws_forecasts_state.json"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "nws_forecasts"]
