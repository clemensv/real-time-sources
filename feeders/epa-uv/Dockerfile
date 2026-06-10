FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/epa-uv"
LABEL org.opencontainers.image.title="EPA UV bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for the US EPA Envirofacts UV Index hourly and daily forecast APIs."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/epa-uv/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./epa_uv_producer/epa_uv_producer_data \
 && pip install ./epa_uv_producer/epa_uv_producer_kafka_producer \
 && pip install .

ENV EPA_UV_STATE_FILE="/mnt/fileshare/epa_uv_state.json"
ENV EPA_UV_LOCATIONS="Seattle,WA"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "epa_uv", "feed"]
