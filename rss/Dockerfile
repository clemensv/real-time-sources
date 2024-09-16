# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install rssbridge_producer/rssbridge_producer_data
RUN pip install rssbridge_producer/rssbridge_producer_kafka_producer
RUN pip install .

# Define environment variables (default values)
ENV CONNECTION_STRING=""
# Feed URLs
ENV FEED_URLS=""

# Run the application
CMD ["python", "-m", "rssbridge", "process"]