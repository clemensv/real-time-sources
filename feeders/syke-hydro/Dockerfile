FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/syke-hydro"
LABEL org.opencontainers.image.title="SYKE Hydrology API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Finnish SYKE Hydrology OData API and Kafka endpoints. Fetches water level and discharge data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./syke_hydro_producer/syke_hydro_producer_data \
 && pip install ./syke_hydro_producer/syke_hydro_producer_kafka_producer \
 && pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "syke_hydro", "feed"]
