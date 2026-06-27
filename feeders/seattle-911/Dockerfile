FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/seattle-911"
LABEL org.opencontainers.image.title="Seattle Fire 911 bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for the City of Seattle real-time fire 911 dispatch feed."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/seattle-911/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./seattle_911_producer/seattle_911_producer_data \
 && pip install ./seattle_911_producer/seattle_911_producer_kafka_producer \
 && pip install ./seattle_911_core \
 && pip install .

ENV SEATTLE_911_LAST_POLLED_FILE="/mnt/fileshare/seattle_911_last_polled.json"
ENV CONNECTION_STRING=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'seattle_911'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "seattle_911"]
