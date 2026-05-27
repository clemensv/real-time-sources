FROM python:3.12-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV KAFKA_TOPIC_SENSORS=digitraffic-road-sensors
ENV KAFKA_TOPIC_MESSAGES=digitraffic-road-messages
ENV KAFKA_TOPIC_MAINTENANCE=digitraffic-road-maintenance

CMD ["python", "-m", "digitraffic_road", "stream"]
