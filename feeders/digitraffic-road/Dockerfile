FROM python:3.12-slim

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./digitraffic_road_producer/digitraffic_road_producer_data \
 && pip install --no-cache-dir ./digitraffic_road_producer/digitraffic_road_producer_kafka_producer \
 && pip install --no-cache-dir ./digitraffic_road_core \
 && pip install --no-cache-dir .

ENV KAFKA_TOPIC_SENSORS=digitraffic-road-sensors
ENV KAFKA_TOPIC_MESSAGES=digitraffic-road-messages
ENV KAFKA_TOPIC_MAINTENANCE=digitraffic-road-maintenance

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'digitraffic_road'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "digitraffic_road", "stream"]
