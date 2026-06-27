FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/geosphere-austria"
LABEL org.opencontainers.image.title="GeoSphere Austria TAWES Weather Bridge"
LABEL org.opencontainers.image.description="Bridges 10-minute TAWES weather observations from GeoSphere Austria into Kafka as CloudEvents"
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/geosphere-austria/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0

COPY geosphere_austria_producer/geosphere_austria_producer_data /app/geosphere_austria_producer_data
COPY geosphere_austria_producer/geosphere_austria_producer_kafka_producer /app/geosphere_austria_producer_kafka_producer

RUN pip install --no-cache-dir /app/geosphere_austria_producer_data && \
    pip install --no-cache-dir /app/geosphere_austria_producer_kafka_producer

COPY . /app
RUN pip install --no-cache-dir ./geosphere_austria_core -e .

ENV CONNECTION_STRING=""
ENV POLLING_INTERVAL=600
ENV STATION_REFRESH_INTERVAL=86400

# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'geosphere_austria'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "geosphere_austria", "feed"]
