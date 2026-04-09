FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/eurdep-radiation"
LABEL org.opencontainers.image.title="EURDEP Radiation bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the EURDEP (European Radiological Data Exchange Platform) ambient gamma dose rate monitoring network and Kafka endpoints. Fetches dose rate data from approximately 5,500 stations across 39 European countries and forwards it as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/eurdep-radiation/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "eurdep_radiation", "feed"]
