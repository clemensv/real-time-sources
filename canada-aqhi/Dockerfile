FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/canada-aqhi"
LABEL org.opencontainers.image.title="Canada AQHI bridge to Kafka"
LABEL org.opencontainers.image.description="Bridges Canada Air Quality Health Index observations and forecasts from Environment and Climate Change Canada to Kafka and CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/canada-aqhi/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install ./canada_aqhi_producer/canada_aqhi_producer_data && \
    pip install ./canada_aqhi_producer/canada_aqhi_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL="3600"
ENV REFERENCE_REFRESH_INTERVAL="86400"
ENV PROVINCES="AB,BC,MB,NB,NL,NS,NT,NU,ON,PE,QC,SK,YT"

CMD ["python", "-m", "canada_aqhi", "feed"]
