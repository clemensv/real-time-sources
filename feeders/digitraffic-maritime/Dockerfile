FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/digitraffic-maritime"
LABEL org.opencontainers.image.title="Digitraffic Marine bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Streams Digitraffic Marine AIS and port-call data to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/digitraffic-maritime/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./digitraffic_maritime_producer/digitraffic_maritime_producer_data \
 && pip install ./digitraffic_maritime_producer/digitraffic_maritime_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""
ENV DIGITRAFFIC_SUBSCRIBE="location,metadata"
ENV DIGITRAFFIC_FILTER_MMSI=""
ENV DIGITRAFFIC_FLUSH_INTERVAL="1000"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'digitraffic_maritime'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "digitraffic_maritime", "stream"]
