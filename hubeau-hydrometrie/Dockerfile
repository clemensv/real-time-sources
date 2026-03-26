# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/hubeau-hydrometrie"
LABEL org.opencontainers.image.title="Hub'Eau Hydrométrie API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the French Hub'Eau Hydrométrie API and Kafka endpoints. It fetches hydrometric data and forwards it to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/hubeau-hydrometrie/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
CMD ["python", "-m", "hubeau_hydrometrie", "feed"]
