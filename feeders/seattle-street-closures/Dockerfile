FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/seattle-street-closures"
LABEL org.opencontainers.image.title="Seattle street closures bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for the City of Seattle street closures dataset."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/seattle-street-closures/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./seattle_street_closures_producer/seattle_street_closures_producer_data \
 && pip install ./seattle_street_closures_producer/seattle_street_closures_producer_kafka_producer \
 && pip install .

ENV SEATTLE_STREET_CLOSURES_STATE_FILE="/mnt/fileshare/seattle_street_closures_state.json"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "seattle_street_closures", "feed"]
