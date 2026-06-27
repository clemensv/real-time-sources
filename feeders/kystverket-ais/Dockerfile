FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/kystverket-ais"
LABEL org.opencontainers.image.title="Kystverket AIS bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams Norwegian AIS vessel tracking data from Kystverket to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/kystverket-ais/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./kystverket_ais_producer/kystverket_ais_producer_data \
 && pip install ./kystverket_ais_producer/kystverket_ais_producer_kafka_producer \
 && pip install ./kystverket_ais_core \
 && pip install .

ENV CONNECTION_STRING=""
ENV AIS_TCP_HOST="153.44.253.27"
ENV AIS_TCP_PORT="5631"
ENV AIS_MESSAGE_TYPES="1,2,3,5,18,19,24,21"
ENV AIS_FLUSH_INTERVAL="1000"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'kystverket_ais'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "kystverket_ais", "stream"]
