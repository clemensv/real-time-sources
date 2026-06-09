FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/smhi-weather" \
      org.opencontainers.image.title="SMHI Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between SMHI meteorological observations and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/smhi-weather/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY smhi_weather_producer/ smhi_weather_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./smhi_weather_producer/smhi_weather_producer_data \
    ./smhi_weather_producer/smhi_weather_producer_kafka_producer

COPY pyproject.toml .
COPY smhi_weather/ smhi_weather/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir .

CMD ["python", "-m", "smhi_weather", "feed"]
