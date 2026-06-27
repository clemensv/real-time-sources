FROM python:3.12-slim

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./french_road_traffic_producer/french_road_traffic_producer_data \
 && pip install --no-cache-dir ./french_road_traffic_producer/french_road_traffic_producer_kafka_producer \
 && pip install --no-cache-dir ./french_road_traffic_core \
 && pip install --no-cache-dir .

ENV KAFKA_TOPIC_FLOW=french-road-traffic-flow
ENV KAFKA_TOPIC_EVENTS=french-road-traffic-events

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'french_road_traffic'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "french_road_traffic", "feed"]
