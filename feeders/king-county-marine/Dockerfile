FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/king-county-marine"
LABEL org.opencontainers.image.title="King County marine bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for current King County marine buoy and mooring telemetry datasets."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/king-county-marine/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./king_county_marine_producer/king_county_marine_producer_data \
 && pip install ./king_county_marine_producer/king_county_marine_producer_kafka_producer \
 && pip install .

ENV KING_COUNTY_MARINE_STATE_FILE="/mnt/fileshare/king_county_marine_state.json"
ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'king_county_marine'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "king_county_marine", "feed"]
