# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# install Git
RUN apt-get update && apt-get install -y git

# Install the required Python packages
RUN pip install gtfs_rt_producer/gtfs_rt_producer_data
RUN pip install gtfs_rt_producer/gtfs_rt_producer_kafka_producer
RUN pip install gtfs_rt_bridge/.

# Define environment variables (default values)

# Azure Event Hubs-style connection string,  supersedes KAFKA_BOOTSTRAP_SERVERS
ENV CONNECTION_STRING=""
# Kafka bootstrap servers
ENV KAFKA_BOOTSTRAP_SERVERS=""
# Kafka topic
ENV KAFKA_TOPIC=""
# Username for SASL PLAIN authentication
ENV SASL_USERNAME=""
# Password for SASL PLAIN authentication
ENV SASL_PASSWORD=""
# Comma separated list of GTFS RT URLs
ENV GTFS_RT_URLS=""
# Comma separated list of GTFS URLs
ENV GTFS_URLS=""
# Route filter
ENV ROUTE=""
# HTTP headers to pass to the GTFS-RT endpoint
ENV GTFS_RT_HEADERS=""
# HTTP headers to pass to the schedule endpoint
ENV GTFS_HEADERS=""
#  Schedule file cache directory
ENV SCHEDULE_CACHE_DIR=""





# Run the application
CMD ["python", "-m", "gtfs_rt_bridge", "feed"]