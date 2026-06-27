FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/wsdot"
LABEL org.opencontainers.image.title="WSDOT traffic flow bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the WSDOT Traveler Information API and Kafka endpoints. Polls real-time traffic flow readings from approximately 1,000 sensors across Washington State highways and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/wsdot/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./wsdot_producer/wsdot_producer_data \
 && pip install ./wsdot_producer/wsdot_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""
ENV WSDOT_ACCESS_CODE=""

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'wsdot'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "wsdot", "feed"]
