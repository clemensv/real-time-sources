# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/jma-japan"
LABEL org.opencontainers.image.title="JMA Japan Weather Bulletins bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the JMA Japan Weather Bulletins Atom feeds and Kafka endpoints. It fetches weather bulletins from JMA and forwards them to the configured Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/jma-japan/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV JMA_LAST_POLLED_FILE="/mnt/fileshare/jma_last_polled.json"
ENV CONNECTION_STRING=""

# Run the application
CMD ["python", "-m", "jma_japan"]
