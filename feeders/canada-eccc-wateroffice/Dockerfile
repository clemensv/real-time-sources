FROM python:3.10-slim

WORKDIR /app
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/canada-eccc-wateroffice"
LABEL org.opencontainers.image.title="Canada ECCC Water Office Hydrometric Bridge"
LABEL org.opencontainers.image.description="Bridges real-time hydrometric data from ECCC Water Survey of Canada to Apache Kafka as CloudEvents"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/canada-eccc-wateroffice/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

COPY requirements.txt .
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir canada_eccc_wateroffice_producer/canada_eccc_wateroffice_producer_data && \
    pip install --no-cache-dir canada_eccc_wateroffice_producer/canada_eccc_wateroffice_producer_kafka_producer && \
    pip install --no-cache-dir -e .

CMD ["python", "-m", "canada_eccc_wateroffice", "feed"]
