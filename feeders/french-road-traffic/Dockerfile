FROM python:3.12-slim

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir .

ENV KAFKA_TOPIC_FLOW=french-road-traffic-flow
ENV KAFKA_TOPIC_EVENTS=french-road-traffic-events

CMD ["python", "-m", "french_road_traffic", "feed"]
