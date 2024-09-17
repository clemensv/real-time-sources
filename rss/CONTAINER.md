# RSS/Atom Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between RSS and Atom feeds and Apache
Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge fetches entries
from specified feeds and forwards them to the configured Kafka endpoints.

The bridge can be configured with a list of RSS feed URLs or OPML file URLs.

The most convenient way to manage a list of RSS feeds is to use an
[OPML](https://en.wikipedia.org/wiki/OPML) file that contains a list of feeds
and is available via HTTP. The bridge can fetch the OPML file and extract the
feed URLs from it. If the OPML file shall not be public, you can host it on a
cloud storage service like Azure Blob Storage or AWS S3 and provide the URL
including an access token.

An example OPML file is part of the repository and can be found at
[world_news.opml](opml/world_news.opml). If you want to reference it directly from the container, you need
to use the ["raw" URL](https://raw.githubusercontent.com/clemensv/real-time-sources/main/rss/opml/world_news.opml)

## Functionality

The bridge retrieves data from RSS and Atom feeds and writes the entries to a
Kafka topic as [CloudEvents](https://cloudevents.io/) in a JSON format, which is
documented in [EVENTS.md](EVENTS.md). You can specify multiple feed URLs by
providing them in the configuration.

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-rss:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-rss:latest
```

## Using the Container Image

The container defines a command that starts the bridge, reading data from the
specified RSS and Atom feeds and writing it to Kafka, Azure Event Hubs, or
Fabric Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e FEED_URLS='<feed-urls>' \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, Azure CLI, or the "custom endpoint" of
a Fabric Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e FEED_URLS='<feed-urls>' \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

### Preserving State Between Restarts

To preserve the state between restarts and avoid reprocessing feed entries,
mount a volume to the container and set the `STATE_FILE` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/state \
    -e STATE_FILE='/mnt/state/rssbridge_state.json' \
    ... other args ... \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams. This replaces the need for `KAFKA_BOOTSTRAP_SERVERS`,
`SASL_USERNAME`, and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port
pairs (e.g., `broker1:9092,broker2:9092`). The client communicates with
TLS-enabled Kafka brokers.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. Ensure your Kafka brokers support SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `FEED_URLS`

A comma-separated list of RSS or Atom feed URLs to fetch entries from.

### `STATE_FILE`

The file path where the bridge stores the state of processed entries. This helps
in resuming data fetching without duplication after restarts. Default is
`/mnt/state/rssbridge_state.json`.

## Deploying into Azure Container Instances

You can deploy the RSS/Atom bridge as a container directly to Azure Container
Instances providing the information explained above. Just click the button below and go.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Frss%2Fazure-template.json)

## Additional Information

- **Source Code**: [GitHub Repository](https://github.com/clemensv/real-time-sources/tree/main/rss)
- **Documentation**: Refer to [EVENTS.md](EVENTS.md) for the JSON event format.
- **License**: MIT

## Example

To run the bridge fetching entries from multiple feeds every 10 minutes and sending them to an Azure Event Hub:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...' \
    -e FEED_URLS='https://example.com/feed1.xml,https://example.com/feed2.xml' \
    -e STATE_FILE='/mnt/state/rssbridge_state.json' \
    -v /path/to/state:/mnt/state \
    ghcr.io/clemensv/real-time-sources-rss:latest
```

This setup allows you to integrate RSS and Atom feed data into your data processing pipelines, enabling real-time data analysis and monitoring.

## Notes

- Ensure that you have network connectivity to the RSS and Atom feed URLs.
- The bridge efficiently handles data fetching and forwarding, but monitor resource usage if you are fetching data from many feeds at a high frequency.

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/clemensv/real-time-sources/issues).
