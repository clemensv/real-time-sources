FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/gdacs"
LABEL org.opencontainers.image.title="GDACS Disaster Alert bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the Global Disaster Alert and Coordination System (GDACS) RSS feed to Kafka endpoints. It polls GDACS for disaster alerts and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/gdacs/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV LOG_LEVEL="INFO"

CMD ["python", "-m", "gdacs"]
