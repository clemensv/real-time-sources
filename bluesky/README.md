# Bluesky Firehose Producer

## Overview

**Bluesky Firehose Producer** connects to the Bluesky AT Protocol firehose and streams real-time events (posts, likes, reposts, follows, blocks, and profile updates) to Kafka topics or Microsoft Event Hubs. Events are formatted as CloudEvents for standardized event processing.

## Key Features:
- **Real-time Firehose**: Subscribe to the full Bluesky network activity stream
- **Multiple Event Types**: Posts, likes, reposts, follows, blocks, and profile updates
- **Kafka Integration**: Send events as CloudEvents to Kafka topics, supporting Microsoft Event Hubs and Microsoft Fabric Event Streams
- **Selective Filtering**: Filter by collection types and apply sampling rates
- **Cursor Management**: Resume from last processed event after restarts
- **High Throughput**: Optimized for high-volume event processing

## Installation

The tool is written in Python and requires Python 3.10 or later (up to 3.12). You can download Python from [here](https://www.python.org/downloads/) or get it from the Microsoft Store if you are on Windows.

> **Note**: This project uses `atproto` version 0.0.54, which provides full support for all firehose message types including #account messages, while maintaining Linux container compatibility. Version 0.0.54 (September 2024) is the last stable version before Pydantic compatibility issues appeared in version 0.0.55+.

### Installation Steps

Once Python is installed, you can install the tool from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=bluesky
```

If you clone the repository, you can install the tool as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/bluesky
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `bluesky_firehose` command.

### **Stream Firehose (`stream`)**

Connects to the Bluesky firehose and streams events to a Kafka topic. The events are formatted using CloudEvents structured JSON format and described in [EVENTS.md](EVENTS.md).

- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream [connection string](#connection-string-for-microsoft-event-hubs-or-fabric-event-streams) (overrides other Kafka parameters).
- `--firehose-url`: Bluesky firehose WebSocket URL (default: wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos).
- `--collections`: Comma-separated list of AT Protocol collections to process (default: app.bsky.feed.post,app.bsky.feed.like,app.bsky.feed.repost,app.bsky.graph.follow).
- `--cursor-file`: Path to file for storing firehose cursor position (default: /tmp/bluesky_cursor).
- `--sample-rate`: Sampling rate for high-volume events (0.0-1.0, default: 1.0 for no sampling).

#### Example Usage:

```bash
bluesky_firehose stream --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>"
```

Alternatively, using a connection string for Microsoft Event Hubs or Microsoft Fabric Event Streams:

```bash
bluesky_firehose stream --connection-string "<your_connection_string>"
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

The connection string format is as follows:

```
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

When provided, the connection string is parsed to extract the Kafka configuration parameters:
- **Bootstrap Servers**: Derived from the `Endpoint` value.
- **Kafka Topic**: Derived from the `EntityPath` value.

## Event Types

The firehose produces the following CloudEvents types:

- `Bluesky.Feed.Post`: New posts and replies
- `Bluesky.Feed.Like`: Likes on posts
- `Bluesky.Feed.Repost`: Reposts/shares of posts
- `Bluesky.Graph.Follow`: Follow relationships
- `Bluesky.Graph.Block`: Block relationships
- `Bluesky.Actor.Profile`: Profile updates

See [EVENTS.md](EVENTS.md) for detailed event schema documentation.

## Configuration

### Environment Variables

The following environment variables can be used instead of command-line arguments:

- `BLUESKY_FIREHOSE_URL`: Firehose WebSocket endpoint
- `BLUESKY_COLLECTIONS`: Comma-separated list of collections to process
- `BLUESKY_CURSOR_FILE`: Path to cursor persistence file
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers
- `KAFKA_TOPIC`: Target Kafka topic
- `SASL_USERNAME`: SASL username
- `SASL_PASSWORD`: SASL password
- `EVENTHUB_CONNECTION_STRING`: Event Hubs connection string

### Filtering and Sampling

For high-volume deployments, you can filter collections and apply sampling:

```bash
# Only process posts
bluesky_firehose stream --collections app.bsky.feed.post --connection-string "<conn>"

# Sample 10% of likes
bluesky_firehose stream --sample-rate 0.1 --collections app.bsky.feed.like --connection-string "<conn>"
```

## Deployment

For production deployments, see:
- [CONTAINER.md](CONTAINER.md) - Docker container instructions
- Azure deployment templates in `azure-template.json`

## Data Volume Considerations

The Bluesky firehose delivers the entire network's activity. At current scale (November 2024), this represents:
- ~50-100 posts per second
- ~200-400 likes per second
- ~50-100 follows per second

Plan your infrastructure accordingly and use filtering/sampling for cost-effective deployment.
