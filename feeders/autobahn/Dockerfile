FROM python:3.12-slim

WORKDIR /app
COPY . /app
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./autobahn_producer/autobahn_producer_data \
 && pip install --no-cache-dir ./autobahn_producer/autobahn_producer_kafka_producer \
 && pip install --no-cache-dir ./autobahn_core \
 && pip install --no-cache-dir .

CMD ["python", "-m", "autobahn", "feed"]
