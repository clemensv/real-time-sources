FROM python:3.12-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV KAFKA_TOPIC_FLOW=french-road-traffic-flow
ENV KAFKA_TOPIC_EVENTS=french-road-traffic-events

CMD ["python", "-m", "french_road_traffic", "feed"]
