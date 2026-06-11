FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install --no-cache-dir ./waterinfo_vmm_producer/waterinfo_vmm_producer_data \
 && pip install --no-cache-dir ./waterinfo_vmm_producer/waterinfo_vmm_producer_kafka_producer \
 && pip install --no-cache-dir -e .
CMD ["python", "-m", "waterinfo_vmm", "feed"]
