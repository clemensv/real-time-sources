FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/cbp-border-wait"
LABEL org.opencontainers.image.title="US CBP Border Wait Times bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the US Customs and Border Protection Border Wait Time API and Kafka endpoints. Fetches wait times at US land border crossings with Canada and Mexico and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/cbp-border-wait/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "cbp_border_wait", "feed"]
