FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/madrid-traffic"
LABEL org.opencontainers.image.title="Madrid Real-Time Traffic (Informo) bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges traffic sensor data from Madrid's Informo system to Kafka endpoints. It polls the pm.xml feed and forwards measurement point reference data and traffic readings as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/madrid-traffic/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "madrid_traffic"]
