FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/seattle-911"
LABEL org.opencontainers.image.title="Seattle Fire 911 bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge for the City of Seattle real-time fire 911 dispatch feed."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/seattle-911/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install .

ENV SEATTLE_911_LAST_POLLED_FILE="/mnt/fileshare/seattle_911_last_polled.json"
ENV CONNECTION_STRING=""

CMD ["python", "-m", "seattle_911"]
