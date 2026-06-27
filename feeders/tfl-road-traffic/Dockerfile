FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/tfl-road-traffic"
LABEL org.opencontainers.image.title="TfL Road Traffic bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges road corridor status and disruption data from the Transport for London (TfL) Unified API to Kafka endpoints, emitting CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/tfl-road-traffic/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir tfl_road_traffic_producer/tfl_road_traffic_producer_data \
 && pip install --no-cache-dir tfl_road_traffic_producer/tfl_road_traffic_producer_kafka_producer \
 && pip install --no-cache-dir ./tfl_road_traffic_core \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="60"
ENV REFERENCE_REFRESH_INTERVAL="3600"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'tfl_road_traffic'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "tfl_road_traffic", "feed"]
