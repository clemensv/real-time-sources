FROM python:3.12-slim

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir .

ENV KAFKA_TOPIC_SENSORS=digitraffic-road-sensors
ENV KAFKA_TOPIC_MESSAGES=digitraffic-road-messages
ENV KAFKA_TOPIC_MAINTENANCE=digitraffic-road-maintenance

CMD ["python", "-m", "digitraffic_road", "stream"]
