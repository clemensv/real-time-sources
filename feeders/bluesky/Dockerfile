# Use an official Python runtime as a parent image
FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/clemensv/real-time-sources/tree/main/feeders/bluesky"
LABEL org.opencontainers.image.title="Bluesky Firehose Producer"
LABEL org.opencontainers.image.description="This container connects to the Bluesky AT Protocol firehose and streams events to Kafka endpoints."
LABEL org.opencontainers.image.documentation="https://github.com/clemensv/real-time-sources/blob/main/feeders/bluesky/CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
ARG SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$SETUPTOOLS_SCM_PRETEND_VERSION
RUN pip install ./bluesky_producer/bluesky_producer_data ./bluesky_producer/bluesky_producer_kafka_producer ./bluesky_core .

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
# Build-time import smoke: fail the image build if the app module (or any
# companion package it imports) is not importable -- closes the "built but
# never ran" gap. PR-time equivalent: tools/ci/import_smoke.py.
RUN python -c "import importlib, importlib.util as _u; _m = 'bluesky'; importlib.import_module(_m + '.app' if _u.find_spec(_m + '.app') else _m)"

CMD ["python", "-m", "bluesky", "stream"]
