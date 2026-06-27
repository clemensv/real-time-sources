FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/hongkong-epd" \
      org.opencontainers.image.title="Hong Kong EPD AQHI Bridge" \
      org.opencontainers.image.description="Bridge between Hong Kong EPD Air Quality Health Index data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/hongkong-epd/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY hongkong_epd_producer/ hongkong_epd_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./hongkong_epd_producer/hongkong_epd_producer_data \
    ./hongkong_epd_producer/hongkong_epd_producer_kafka_producer

COPY pyproject.toml .
COPY hongkong_epd/ hongkong_epd/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'hongkong_epd'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "hongkong_epd", "feed"]
