FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/nve-hydro"
LABEL org.opencontainers.image.title="NVE Hydrology API bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Bridge between the Norwegian NVE HydAPI and Kafka endpoints. Fetches water level and discharge data and forwards it as CloudEvents."
LABEL org.opencontainers.image.license="MIT"

WORKDIR /app
COPY . /app
RUN pip install .

ENV CONNECTION_STRING=""
ENV NVE_API_KEY=""

CMD ["python", "-m", "nve_hydro", "feed"]
