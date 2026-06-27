FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/nws-alerts"
LABEL org.opencontainers.image.title="NWS CAP weather alerts bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Polls the US National Weather Service for active alerts and forwards them as CloudEvents."
LABEL org.opencontainers.image.license="MIT"
WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./nws_alerts_producer/nws_alerts_producer_data \
 && pip install --no-cache-dir ./nws_alerts_producer/nws_alerts_producer_kafka_producer \
 && pip install --no-cache-dir ./nws_alerts_core \
 && pip install --no-cache-dir .
ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'nws_alerts'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "nws_alerts", "feed"]
