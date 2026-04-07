FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/irail"
LABEL org.opencontainers.image.title="iRail Belgian railway bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the iRail Belgian railway API and Kafka endpoints. Polls real-time departure boards for approximately 600 NMBS/SNCB stations and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/irail/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "irail", "feed"]
