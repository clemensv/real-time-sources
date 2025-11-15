# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/bluesky"
LABEL org.opencontainers.image.title="Bluesky Firehose Producer"
LABEL org.opencontainers.image.description="This container connects to the Bluesky AT Protocol firehose and streams events to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/bluesky/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install --only-binary=:all: .

# Define environment variables (default values)
ENV PYTHONUNBUFFERED=1
ENV BLUESKY_FIREHOSE_URL="wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos"
ENV BLUESKY_COLLECTIONS="app.bsky.feed.post,app.bsky.feed.like,app.bsky.feed.repost,app.bsky.graph.follow"
ENV BLUESKY_CURSOR_FILE="/tmp/bluesky_cursor"
ENV KAFKA_BOOTSTRAP_SERVERS=""
ENV KAFKA_TOPIC=""
ENV SASL_USERNAME=""
ENV SASL_PASSWORD=""
ENV CONNECTION_STRING=""
ENV SAMPLE_RATE="1.0"
ENV LOG_LEVEL="INFO"

# Run the application using Python module
CMD ["python", "-m", "bluesky", "stream"]
