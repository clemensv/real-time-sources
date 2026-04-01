# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/german-waters"
LABEL org.opencontainers.image.title="German Waters bridge to Kafka endpoints"
LABEL org.opencontainers.image.description="Aggregates water level data from German state flood services and forwards it to Kafka endpoints as CloudEvents."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/german-waters/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
ENV PROVIDERS=""
ENV EXCLUDE_PROVIDERS=""

# Run the application
CMD ["python", "-m", "german_waters", "feed"]
