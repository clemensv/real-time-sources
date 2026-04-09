FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/australia-wildfires"
LABEL org.opencontainers.image.title="Australian State Wildfires bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges live bushfire incident data from NSW RFS, VicEmergency, and QLD Fire Department to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/australia-wildfires/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "australia_wildfires", "feed"]
