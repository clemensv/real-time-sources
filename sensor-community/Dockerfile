FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/sensor-community"
LABEL org.opencontainers.image.title="Sensor.Community air quality bridge to Kafka"
LABEL org.opencontainers.image.description="This container bridges the Sensor.Community citizen science API to Kafka/CloudEvents, emitting air quality readings and sensor metadata."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/sensor-community/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

RUN pip install ./sensor_community_producer/sensor_community_producer_data && \
    pip install ./sensor_community_producer/sensor_community_producer_kafka_producer && \
    pip install .

ENV CONNECTION_STRING=""
ENV SENSOR_TYPES="SDS011,BME280,SPS30,DHT22,PMS5003,SHT31,BMP280"
ENV POLLING_INTERVAL="300"

CMD ["python", "-m", "sensor_community", "feed"]
