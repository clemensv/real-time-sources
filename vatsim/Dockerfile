# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/vatsim"
LABEL org.opencontainers.image.title="VATSIM Live Data Feed bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the VATSIM virtual aviation network live data feed to Kafka endpoints, emitting pilot positions, controller positions, and network status as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/vatsim/CONTAINER.md"
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
CMD ["python", "-m", "vatsim", "feed"]
