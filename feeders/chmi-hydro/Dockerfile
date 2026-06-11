FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./chmi_hydro_producer/chmi_hydro_producer_data \
 && pip install --no-cache-dir ./chmi_hydro_producer/chmi_hydro_producer_kafka_producer \
 && pip install --no-cache-dir -e .

CMD ["python", "-m", "chmi_hydro", "feed"]
