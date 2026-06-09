FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources"
LABEL org.opencontainers.image.title="PTWC/NTWC Tsunami Bulletins Bridge"
LABEL org.opencontainers.image.description="Bridges tsunami bulletins from NOAA PTWC/NTWC to Kafka/Event Hubs as CloudEvents"

WORKDIR /app

COPY . /app/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ptwc_tsunami_producer/ptwc_tsunami_producer_data \
    ptwc_tsunami_producer/ptwc_tsunami_producer_kafka_producer \
    .

CMD ["python", "-m", "ptwc_tsunami"]
