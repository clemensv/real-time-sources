FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/syke-hydro"
LABEL org.opencontainers.image.title="SYKE Hydrology API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Finnish SYKE Hydrology OData API and Kafka endpoints. Fetches water level and discharge data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""

CMD ["python", "-m", "syke_hydro", "feed"]
