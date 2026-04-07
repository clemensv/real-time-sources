FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/nws-alerts"
LABEL org.opencontainers.image.title="NWS CAP weather alerts bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Polls the US National Weather Service for active alerts and forwards them as CloudEvents."
LABEL org.opencontainers.image.license="MIT"
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .
ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"
CMD ["python", "-m", "nws_alerts"]
