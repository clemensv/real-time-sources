FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/ticketmaster"
LABEL org.opencontainers.image.title="Ticketmaster Discovery API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges Ticketmaster Discovery API v2 data (events, venues, attractions, classifications) to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/ticketmaster/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ticketmaster_producer/ticketmaster_producer_data && \
    pip install --no-cache-dir ticketmaster_producer/ticketmaster_producer_kafka_producer && \
    pip install --no-cache-dir .

ENV CONNECTION_STRING=""
ENV TICKETMASTER_API_KEY=""
ENV COUNTRY_CODES="AU,AT,BE,CA,CZ,DK,FI,FR,DE,GR,HU,IE,IT,MX,NL,NZ,NO,PL,PT,ES,SE,CH,GB,US"
ENV POLL_INTERVAL="300"
ENV REFERENCE_REFRESH="3600"
ENV KAFKA_ENABLE_TLS="true"
ENV LOG_LEVEL="INFO"

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'ticketmaster'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "ticketmaster", "feed"]
