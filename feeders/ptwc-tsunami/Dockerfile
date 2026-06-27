FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources"
LABEL org.opencontainers.image.title="PTWC/NTWC Tsunami Bulletins Bridge"
LABEL org.opencontainers.image.description="Bridges tsunami bulletins from NOAA PTWC/NTWC to Kafka/Event Hubs as CloudEvents"

WORKDIR /app

COPY . /app/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ptwc_tsunami_producer/ptwc_tsunami_producer_data \
    ptwc_tsunami_producer/ptwc_tsunami_producer_kafka_producer \
    ./ptwc_tsunami_core \
    .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'ptwc_tsunami'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "ptwc_tsunami", "feed"]
