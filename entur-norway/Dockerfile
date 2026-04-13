FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/entur-norway"
LABEL org.opencontainers.image.title="Entur Norway SIRI real-time bridge to Kafka"
LABEL org.opencontainers.image.description="Bridge between Entur Norway SIRI real-time feeds (ET, VM, SX) and Apache Kafka. Emits DatedServiceJourney reference data, EstimatedVehicleJourney predictions, MonitoredVehicleJourney positions, and PtSituationElement alerts as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/entur-norway/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install ./entur_norway_producer/entur_norway_producer_data \
    && pip install ./entur_norway_producer/entur_norway_producer_kafka_producer \
    && pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "entur_norway", "feed"]
