FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/hko-hong-kong" \
      org.opencontainers.image.title="HKO Hong Kong Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between Hong Kong Observatory weather data and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/hko-hong-kong/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY hko_hong_kong_producer/ hko_hong_kong_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./hko_hong_kong_producer/hko_hong_kong_producer_data \
    ./hko_hong_kong_producer/hko_hong_kong_producer_kafka_producer

COPY pyproject.toml .
COPY hko_hong_kong_core/ hko_hong_kong_core/
COPY hko_hong_kong/ hko_hong_kong/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./hko_hong_kong_core .

CMD ["python", "-m", "hko_hong_kong", "feed"]
