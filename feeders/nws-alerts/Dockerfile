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
CMD ["python", "-m", "nws_alerts", "feed"]
