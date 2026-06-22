FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/cbp-border-wait"
LABEL org.opencontainers.image.title="US CBP Border Wait Times bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the US Customs and Border Protection Border Wait Time API and Kafka endpoints. Fetches wait times at US land border crossings with Canada and Mexico and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/cbp-border-wait/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./cbp_border_wait_producer/cbp_border_wait_producer_data \
 && pip install ./cbp_border_wait_producer/cbp_border_wait_producer_kafka_producer \
 && pip install ./cbp_border_wait_core \
 && pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "cbp_border_wait", "feed"]
