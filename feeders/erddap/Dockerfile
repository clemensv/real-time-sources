FROM python:3.10-slim
LABEL source="erddap" \
      title="ERDDAP ERDDAP_KAFKA feeder" \
      description="Config-driven ERDDAP tabledap CloudEvents feeder" \
      documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/erddap/CONTAINER.md" \
      license="MIT"
ENV PYTHONUNBUFFERED=1
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ./erddap_producer/erddap_producer_data \
 && pip install --no-cache-dir ./erddap_producer/erddap_producer_kafka_producer \
 && pip install --no-cache-dir ./erddap_core \
 && pip install --no-cache-dir ./erddap_kafka
CMD ["python", "-m", "erddap_kafka", "feed"]

