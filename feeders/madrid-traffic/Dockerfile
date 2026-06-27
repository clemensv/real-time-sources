FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/madrid-traffic"
LABEL org.opencontainers.image.title="Madrid Real-Time Traffic (Informo) bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges traffic sensor data from Madrid's Informo system to Kafka endpoints. It polls the pm.xml feed and forwards measurement point reference data and traffic readings as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/madrid-traffic/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./madrid_traffic_producer/madrid_traffic_producer_data \
 && pip install --no-cache-dir ./madrid_traffic_producer/madrid_traffic_producer_kafka_producer \
 && pip install --no-cache-dir ./madrid_traffic_core \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'madrid_traffic'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "madrid_traffic", "feed"]
