FROM python:3.10-slim
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources" \
      org.opencontainers.image.title="CAP Alerts Kafka feeder" \
      org.opencontainers.image.description="Generalized CAP 1.2 alerts to Kafka CloudEvents" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/cap-alerts/CONTAINER.md" \
      org.opencontainers.image.license="MIT"
ENV PYTHONUNBUFFERED=1
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ./cap_alerts_producer/cap_alerts_producer_data && \
    pip install --no-cache-dir ./cap_alerts_producer/cap_alerts_producer_kafka_producer && \
    pip install --no-cache-dir ./cap_alerts_core && \
    pip install --no-cache-dir ./cap_alerts_kafka
ENV CAP_SOURCES='' POLL_INTERVAL=300 REFERENCE_REFRESH_INTERVAL=21600
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'cap_alerts'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "cap_alerts", "feed"]


