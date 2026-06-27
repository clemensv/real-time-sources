FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/hko-hong-kong" \
      org.opencontainers.image.title="HKO Hong Kong Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Hong Kong Observatory weather data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/hko-hong-kong/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY hko_hong_kong_producer/ hko_hong_kong_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./hko_hong_kong_producer/hko_hong_kong_producer_data \
    ./hko_hong_kong_producer/hko_hong_kong_producer_kafka_producer

COPY pyproject.toml .
COPY hko_hong_kong_core/ hko_hong_kong_core/
COPY hko_hong_kong/ hko_hong_kong/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./hko_hong_kong_core .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'hko_hong_kong'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "hko_hong_kong", "feed"]
