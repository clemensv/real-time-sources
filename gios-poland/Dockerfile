# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/gios-poland"
LABEL org.opencontainers.image.title="GIOŚ Poland Air Quality bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the Polish Chief Inspectorate of Environmental Protection (GIOŚ) air quality monitoring network and Kafka endpoints. It fetches station metadata, sensor reference data, hourly measurements, and air quality index values and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/gios-poland/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV GIOS_LAST_POLLED_FILE="/mnt/fileshare/gios_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "gios_poland"]
