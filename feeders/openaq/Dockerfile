FROM python:3.10-slim
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources" \
      org.opencontainers.image.title="OpenAQ Kafka feeder" \
      org.opencontainers.image.description="Polls OpenAQ API v3 global air-quality locations, sensors, and latest measurements and emits CloudEvents to Kafka/Event Hubs." \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/openaq/CONTAINER.md" \
      org.opencontainers.image.license="MIT"
ENV PYTHONUNBUFFERED=1
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ./openaq_producer/openaq_producer_data \
 && pip install --no-cache-dir ./openaq_producer/openaq_producer_kafka_producer \
 && pip install --no-cache-dir ./openaq_core \
 && pip install --no-cache-dir ./openaq_kafka
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'openaq'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "openaq", "feed"]


