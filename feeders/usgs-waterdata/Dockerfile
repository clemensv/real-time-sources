FROM python:3.10-slim
ARG PIP_INDEX_URL=https://pypi.org/simple
LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources" \
      org.opencontainers.image.title="USGS Water Data Kafka feeder" \
      org.opencontainers.image.description="Native USGS continuous observations and reference metadata as CloudEvents" \
      org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/usgs-waterdata/CONTAINER.md" \
      org.opencontainers.image.licenses="MIT" \
      com.azure.containerizationassist.createdby="containerization-assist"
ENV PYTHONUNBUFFERED=1 SETUPTOOLS_SCM_PRETEND_VERSION=0.1.0
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ./usgs_waterdata_producer/usgs_waterdata_producer_data \
 && pip install --no-cache-dir ./usgs_waterdata_producer/usgs_waterdata_producer_kafka_producer \
 && pip install --no-cache-dir ./usgs_waterdata_core \
 && pip install --no-cache-dir '.[kafka]' \
 && useradd --create-home --uid 10001 feeder \
 && mkdir /state && chown feeder:feeder /state
USER feeder
# Outbound poller: no listening socket or HTTP health endpoint.
HEALTHCHECK NONE
RUN python -c "import importlib, importlib.util as _u; _m='usgs_waterdata'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m); from usgs_waterdata.transports import generated; generated('kafka')"
CMD ["python", "-m", "usgs_waterdata", "feed"]
