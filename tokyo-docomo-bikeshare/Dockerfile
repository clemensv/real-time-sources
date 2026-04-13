# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/tokyo-docomo-bikeshare"
LABEL org.opencontainers.image.title="Tokyo Docomo Bikeshare GBFS bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="This container is a bridge between the Tokyo Docomo Bikeshare GBFS 2.3 feed and Kafka endpoints. It polls station information and real-time bike availability from the ODPT platform and forwards them to the configured Kafka topic as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/tokyo-docomo-bikeshare/CONTAINER.md"
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
CMD ["python", "-m", "tokyo_docomo_bikeshare"]
