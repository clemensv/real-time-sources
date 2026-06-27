FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/ndw-road-traffic"
LABEL org.opencontainers.image.title="NDW Netherlands Road Traffic Bridge"
LABEL org.opencontainers.image.description="Bridges Dutch NDW road traffic data (speed, travel time, DRIP, MSI, situations) to Kafka via CloudEvents"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/ndw-road-traffic/CONTAINER.md"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ndw_road_traffic_producer/ndw_road_traffic_producer_data \
 && pip install --no-cache-dir ndw_road_traffic_producer/ndw_road_traffic_producer_kafka_producer \
 && pip install --no-cache-dir ./ndw_road_traffic_core \
 && pip install --no-cache-dir .

ENV POLLING_INTERVAL=60

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'ndw_road_traffic'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "ndw_road_traffic"]
