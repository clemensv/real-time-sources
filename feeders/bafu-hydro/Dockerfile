FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/bafu-hydro"
LABEL org.opencontainers.image.title="BAFU Hydrology bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Swiss BAFU/FOEN hydrology data (via existenz.ch) and Kafka endpoints. Fetches water level, discharge, and temperature data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./bafu_hydro_producer/bafu_hydro_producer_data \
 && pip install ./bafu_hydro_producer/bafu_hydro_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'bafu_hydro'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "bafu_hydro", "feed"]
