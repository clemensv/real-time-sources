# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/cdec-reservoirs"
LABEL org.opencontainers.image.title="CDEC California Reservoirs bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the California Data Exchange Center (CDEC) reservoir data API to Kafka endpoints, emitting hourly storage, elevation, inflow, and outflow readings as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/cdec-reservoirs/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "cdec_reservoirs", "feed"]
