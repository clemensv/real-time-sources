# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/aviationweather"
LABEL org.opencontainers.image.title="AviationWeather.gov METAR/SIGMET bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the NOAA AviationWeather.gov API (METAR observations, SIGMET advisories, station data) and Kafka endpoints. It polls aviation weather data and forwards it to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/aviationweather/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV AVIATIONWEATHER_LAST_POLLED_FILE="/mnt/fileshare/aviationweather_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "aviationweather"]
