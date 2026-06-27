FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/environment-canada" \
      org.opencontainers.image.title="Environment Canada Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Environment Canada SWOB observations and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/environment-canada/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY environment_canada_producer/ environment_canada_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./environment_canada_producer/environment_canada_producer_data \
    ./environment_canada_producer/environment_canada_producer_kafka_producer

COPY pyproject.toml .
COPY environment_canada_core/ environment_canada_core/
COPY environment_canada/ environment_canada/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./environment_canada_core .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'environment_canada'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "environment_canada", "feed"]
