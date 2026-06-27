FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/kmi-belgium" \
      org.opencontainers.image.title="KMI Belgium Weather Observation Bridge" \
      org.opencontainers.image.description="Bridge between KMI/RMI automatic weather station observations and Kafka/Event Hubs endpoints" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/kmi-belgium/CONTAINER.md" \
      org.opencontainers.image.license="MIT"

WORKDIR /app

COPY kmi_belgium_producer/ kmi_belgium_producer/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir \
    ./kmi_belgium_producer/kmi_belgium_producer_data \
    ./kmi_belgium_producer/kmi_belgium_producer_kafka_producer

COPY pyproject.toml .
COPY kmi_belgium_core/ kmi_belgium_core/
COPY kmi_belgium/ kmi_belgium/

ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./kmi_belgium_core .

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'kmi_belgium'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "kmi_belgium", "feed"]
