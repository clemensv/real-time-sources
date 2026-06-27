FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/bom-australia"
LABEL org.opencontainers.image.title="BOM Australia Weather Observation bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges real-time weather observations from the Australian Bureau of Meteorology to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/bom-australia/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./bom_australia_producer/bom_australia_producer_data \
 && pip install --no-cache-dir ./bom_australia_producer/bom_australia_producer_kafka_producer \
 && pip install --no-cache-dir ./bom_australia_core \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'bom_australia'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "bom_australia", "feed"]
