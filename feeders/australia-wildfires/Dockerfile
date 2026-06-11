FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/australia-wildfires"
LABEL org.opencontainers.image.title="Australian State Wildfires bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges live bushfire incident data from NSW RFS, VicEmergency, and QLD Fire Department to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/australia-wildfires/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./australia_wildfires_producer/australia_wildfires_producer_data \
 && pip install --no-cache-dir ./australia_wildfires_producer/australia_wildfires_producer_kafka_producer \
 && pip install --no-cache-dir .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "australia_wildfires", "feed"]
