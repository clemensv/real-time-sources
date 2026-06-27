FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/bfs-odl"
LABEL org.opencontainers.image.title="BfS ODL Gamma Dose Rate bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the German Federal Office for Radiation Protection (BfS) ODL monitoring network and Kafka endpoints. Fetches ambient gamma dose rate data from approximately 1,700 stations and forwards it as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/bfs-odl/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./bfs_odl_producer/bfs_odl_producer_data \
 && pip install ./bfs_odl_producer/bfs_odl_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'bfs_odl'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "bfs_odl", "feed"]
