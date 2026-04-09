# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/ireland-opw-waterlevel"
LABEL org.opencontainers.image.title="Ireland OPW waterlevel.ie bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container bridges the Ireland OPW waterlevel.ie GeoJSON API and Kafka endpoints, emitting real-time water level, temperature, and voltage data from Irish hydrometric stations."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/ireland-opw-waterlevel/CONTAINER.md"
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
CMD ["python", "-m", "ireland_opw_waterlevel", "feed"]
