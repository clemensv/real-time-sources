# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/energy-charts"
LABEL org.opencontainers.image.title="Energy-Charts European electricity data bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the Energy-Charts API (Fraunhofer ISE) for European electricity generation, prices, and grid carbon signals to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/energy-charts/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV ENERGY_CHARTS_LAST_POLLED_FILE="/mnt/fileshare/energy_charts_last_polled.json"
ENV CONNECTION_STRING=""
ENV COUNTRY="de"
ENV BIDDING_ZONE="DE-LU"

# Run the application
CMD ["python", "-m", "energy_charts"]
