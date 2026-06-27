FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/wikimedia-osm-diffs"
LABEL org.opencontainers.image.title="OpenStreetMap Minutely Diffs bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges OpenStreetMap minutely replication diffs into Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/wikimedia-osm-diffs/CONTAINER.md"
LABEL org.opencontainers.image.license="ODbL-1.0"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./wikimedia_osm_diffs_producer/wikimedia_osm_diffs_producer_data \
 && pip install ./wikimedia_osm_diffs_producer/wikimedia_osm_diffs_producer_kafka_producer \
 && pip install ./wikimedia_osm_diffs_core \
 && pip install .

ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'wikimedia_osm_diffs'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "wikimedia_osm_diffs", "feed"]
