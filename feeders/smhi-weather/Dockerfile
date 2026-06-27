FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/smhi-weather" \
      org.opencontainers.image.title="SMHI Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between SMHI meteorological observations and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/smhi-weather/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY smhi_weather_producer/ smhi_weather_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./smhi_weather_producer/smhi_weather_producer_data \
    ./smhi_weather_producer/smhi_weather_producer_kafka_producer

COPY pyproject.toml .
COPY smhi_weather_core/ smhi_weather_core/
COPY smhi_weather/ smhi_weather/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./smhi_weather_core .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'smhi_weather'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "smhi_weather", "feed"]
