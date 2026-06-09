FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/bafu-hydro"
LABEL org.opencontainers.image.title="BAFU Hydrology bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Swiss BAFU/FOEN hydrology data (via existenz.ch) and Kafka endpoints. Fetches water level, discharge, and temperature data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "bafu_hydro", "feed"]
