# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/nepal-bipad-hydrology"
LABEL org.opencontainers.image.title="Nepal BIPAD Portal river monitoring bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the Nepal BIPAD Portal river-stations API to Kafka endpoints, emitting river station reference data and real-time water level readings as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/nepal-bipad-hydrology/CONTAINER.md"
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
CMD ["python", "-m", "nepal_bipad_hydrology", "feed"]
