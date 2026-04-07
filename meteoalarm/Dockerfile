FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/meteoalarm"
LABEL org.opencontainers.image.title="Meteoalarm European weather warnings bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Polls Meteoalarm for severe weather warnings from 30+ European national meteorological services and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/meteoalarm/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

CMD ["python", "-m", "meteoalarm"]
