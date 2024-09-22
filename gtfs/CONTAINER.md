# GTFS and GTFS-RT API bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between GTFS and GTFS-RT APIs and Apache
Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge reads data from
GTFS and GTFS-RT APIs and writes data to a Kafka topic.

GTFS stands for General Transit Feed Specification. GTFS is a set of open data
standards for public transportation schedules and associated geographic
information. GTFS-RT is a real-time extension to GTFS that allows public
transportation agencies to provide real-time updates about their fleet. Over 2000
transit agencies worldwide provide GTFS and GTFS-RT data.

The [Mobility Database](https://mobilitydatabase.org) provides a comprehensive list of GTFS
and GTFS-RT feeds from around the world. 

The bridge fetches GTFS and GTFS-RT data from the supplied URLs and writes the
data to a Kafka topic as [CloudEvents](https://cloudevents.io/) in a JSON format that
is documented in [EVENTS.md](EVENTS.md). One bridge instance can handle multiple
GTFS and GTFS-RT feeds, but they are managed under a single agency identifier that
must be supplied in the configuration.

## Installing the container image

Install from the command line as
```shell
$ docker pull ghcr.io/clemensv/real-time-sources-gtfs:latest
```

Use as base image in Dockerfile:

```Dockerfile
FROM ghcr.io/clemensv/real-time-sources-gtfs:latest
```

## Database Schemas and handling

If you want to build a full data pipeline with all events ingested into
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Using the container image

The container image defines a single command that starts the bridge. The bridge
reads data from GTFS and GTFS-RT APIs and writes data to a Kafka topic or
Azure Event Hubs or Fabric Event Streams.

### With a Kafka broker

The image assumes that you have a Kafka broker that is configured with TLS and
SASL PLAIN authentication. You can start the container locally on docker with
the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e GTFS_RT_URLS='<gtfs-rt-urls>' \
    -e GTFS_URLS='<gtfs-urls>' \
    -e AGENCY='<agency-id>' \
    ghcr.io/clemensv/real-time-sources-gtfs:latest
```

### With Azure Event Hubs or Fabric Event Streams

With Azure Event Hubs or Fabric Event Streams, you can use the connection string
to establish a connection to the service. You get the connection string from the
Azure portal, from the Azure CLI, or from the "custom endpoint" of a Fabric
Event Stream.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e GTFS_RT_URLS='<gtfs-rt-urls>' \
    -e GTFS_URLS='<gtfs-urls>' \
    -e AGENCY='<agency-id>' \
    ghcr.io/clemensv/real-time-sources-gtfs:latest
```


### Preserve the cache directory

If you want to preserve state between restarts to avoid sending that you have
already sent, you can mount a volume to the container and refer to it in the
`SCHEDULE_CACHE_DIR` environment variable:

```shell
$ docker run --rm \
    -v /path/to/state:/var/lib/real-time-sources-gtfs \
    ... other args... \
    -e SCHEDULE_CACHE_DIR='/var/lib/real-time-sources-gtfs' \
    ghcr.io/clemensv/real-time-sources-gtfs:latest
```

## Environment Variables

### `CONNECTION_STRING`

Azure Event Hubs-style connection string is used to establish a connection to
Azure Event Hubs or Fabric Event Streams. This connection string contains the
necessary credentials and configuration settings required for secure and
efficient data transmission. The connection string is used in place of
`KAFKA_BOOTSTRAP_SERVERS` and `SASL_USERNAME` and `SASL_PASSWORD`.

### `KAFKA_BOOTSTRAP_SERVERS`

Address of the Kafka broker. This is a comma-separated list of host and port
pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster
that a Kafka client connects to initially to bootstrap itself. For example,
`broker1:9092,broker2:9092`. The client assumes communication with TLS enabled
Kafka brokers.

### `KAFKA_TOPIC`

Kafka topic to produce messages to.

### `SASL_USERNAME`

Username for SASL PLAIN authentication. The client assumes that the Kafka
brokers have been configured to support SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication. The client assumes that the Kafka
brokers have been configured to support SASL PLAIN authentication.

### `GTFS_RT_URLS`

Comma-separated list of GTFS-RT URLs for real-time vehicle positions and/or trip
updates and/or alerts. The supplied endpoints may support any combination of the
GTFS-RT feeds. The client fetches GTFS-RT data from all of these URLs.

### `GTFS_RT_HEADERS`

HTTP headers to pass to the GTFS-RT endpoint. The headers are passed as
key=value pairs separated by spaces. For example, `key1=value1 key2=value2`.
Values may be quoted to preserve spaces inside values. For example,
`key1="value with spaces"`. The client passes these headers to the GTFS-RT
endpoint when fetching GTFS-RT data.

### `GTFS_URLS`

Comma-separated list of GTFS URLs for schedule and other reference data. The
client fetches GTFS data from all of these URLs.

### `GTFS_HEADERS`

HTTP headers to pass to the schedule endpoint. The headers are passed as
key=value pairs separated by spaces. For example, `key1=value1 key2=value2`.
Values may be quoted to preserve spaces inside values. For example,
`key1="value with spaces"`. The client passes these headers to the schedule
endpoint when fetching GTFS data.

### `AGENCY`

Agency identifier. The client uses this identifier to group GTFS and GTFS-RT
data under a single agency. The client includes this identifier in the CloudEvent
`source` field.

### `ROUTE`

Route filter. Reserved.

### `SCHEDULE_CACHE_DIR`

Schedule file cache directory. The client caches GTFS schedule files in this
directory and keeps track of the last modification time of the files. This
assures that data is not acquired and sent to the Kafka broker if the schedule
files have not changed since the last fetch.


## Deploying into Azure Container Instances

You can deploy the RSS/Atom bridge as a container directly to Azure Container
Instances providing the information explained above. Just click the button below and go.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgtfs%2Fazure-template.json)


### Example

The following example shows how to start the bridge with a set of feeds for the
Seattle metropolitan area, sending to an Event Hub.

The corresponding entries in the mobility database are:
*  [Puget Sound Consolidated GTFS](https://mobilitydatabase.org/feeds/mdb-1080)
*  [King County Metro GTFS-RT Trip Updates](https://mobilitydatabase.org/feeds/mdb-1540)
*  [King County Metro GTFS-RT Vehicle Positions](https://mobilitydatabase.org/feeds/mdb-1542)
*  [King County Metro GTFS-RT Alerts](https://mobilitydatabase.org/feeds/mdb-1541)

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e GTFS_RT_URLS='https://api-endpoint.com/gtfs-rt' \
    -e GTFS_URLS='https://gtfs.sound.obaweb.org/prod/1_gtfs.zip' \
    -e GTFS_RT_URLS='https://s3.amazonaws.com/kcm-alerts-realtime-prod/tripupdates.pb,https://s3.amazonaws.com/kcm-alerts-realtime-prod/alerts.pb,https://s3.amazonaws.com/kcm-alerts-realtime-prod/vehiclepositions.pb' \
    -e AGENCY='KingCountyMetro' \
    ghcr.io/clemensv/real-time-sources-gtfs:latest
```
