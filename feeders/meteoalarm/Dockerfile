FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/meteoalarm"
LABEL org.opencontainers.image.title="Meteoalarm European weather warnings bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Polls Meteoalarm for severe weather warnings from 30+ European national meteorological services and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/meteoalarm/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./meteoalarm_producer/meteoalarm_producer_data \
 && pip install --no-cache-dir ./meteoalarm_producer/meteoalarm_producer_kafka_producer \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'meteoalarm'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "meteoalarm", "feed"]
