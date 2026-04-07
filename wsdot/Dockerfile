FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/wsdot"
LABEL org.opencontainers.image.title="WSDOT traffic flow bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the WSDOT Traveler Information API and Kafka endpoints. Polls real-time traffic flow readings from approximately 1,000 sensors across Washington State highways and forwards them as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/wsdot/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app

COPY . /app

RUN pip install .

ENV CONNECTION_STRING=""
ENV WSDOT_ACCESS_CODE=""

CMD ["python", "-m", "wsdot", "feed"]
