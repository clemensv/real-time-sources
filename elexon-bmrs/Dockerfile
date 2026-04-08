# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/elexon-bmrs"
LABEL org.opencontainers.image.title="Elexon BMRS (GB Electricity Market) bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the Elexon BMRS API (GB electricity market balancing mechanism data) and Kafka endpoints. It fetches generation mix and demand outturn data and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/elexon-bmrs/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV BMRS_LAST_POLLED_FILE="/mnt/fileshare/bmrs_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "elexon_bmrs"]
