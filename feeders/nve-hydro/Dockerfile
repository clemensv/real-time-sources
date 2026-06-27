FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/nve-hydro"
LABEL org.opencontainers.image.title="NVE Hydrology API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Norwegian NVE HydAPI and Kafka endpoints. Fetches water level and discharge data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./nve_hydro_producer/nve_hydro_producer_data \
 && pip install ./nve_hydro_producer/nve_hydro_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""
ENV NVE_API_KEY=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'nve_hydro'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "nve_hydro", "feed"]
