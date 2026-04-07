FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/bfs-odl"
LABEL org.opencontainers.image.title="BfS ODL Gamma Dose Rate bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the German Federal Office for Radiation Protection (BfS) ODL monitoring network and Kafka endpoints. Fetches ambient gamma dose rate data from approximately 1,700 stations and forwards it as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/bfs-odl/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "bfs_odl", "feed"]
