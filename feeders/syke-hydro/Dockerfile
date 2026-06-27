FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/syke-hydro"
LABEL org.opencontainers.image.title="SYKE Hydrology API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Finnish SYKE Hydrology OData API and Kafka endpoints. Fetches water level and discharge data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./syke_hydro_producer/syke_hydro_producer_data \
 && pip install ./syke_hydro_producer/syke_hydro_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'syke_hydro'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "syke_hydro", "feed"]
