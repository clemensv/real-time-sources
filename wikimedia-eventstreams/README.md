# Wikimedia EventStreams RecentChange Bridge

## Overview

**Wikimedia EventStreams RecentChange Bridge** connects to Wikimedia
Foundation's public `recentchange` feed and forwards edit activity from
Wikipedia, Wikidata, Wikimedia Commons, and the rest of the Wikimedia
universe to Kafka as [CloudEvents](https://cloudevents.io/).

This first implementation deliberately focuses on the public
`recentchange` stream. Wikimedia exposes more stream families, but they are
not just filter variants of the same payload. Some are aliases, some are
more specialized page or revision feeds, and some are internal mutation
topics. Those deserve separate contract work instead of being collapsed
into one generic schema.

## Data Source

- **Endpoint**: `https://stream.wikimedia.org/v2/stream/recentchange`
- **Protocol**: EventStreams over HTTP, consumed here as newline-delimited
  JSON with `Accept: application/json`
- **Authentication**: None
- **Freshness**: Near-real-time, typically within seconds of the edit
- **Coverage**: All Wikimedia projects, including Wikipedia, Wikidata, and
  Wikimedia Commons
- **Upstream docs**:
  - <https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams>
  - <https://www.mediawiki.org/wiki/Manual:RCFeed>

## Key Features

- **Continuous HTTP stream**: Holds an open EventStreams connection and
  forwards events as they arrive
- **Resume support**: Reconnects with `?since=` using the last seen event
  timestamp
- **Bounded dedupe**: Keeps a rolling cache of recent Wikimedia event UUIDs
  to avoid replay duplicates after reconnects
- **Kafka integration**: Works with direct Kafka settings or
  Event Hubs / Fabric connection strings
- **Typed contract**: Emits one `Wikimedia.EventStreams.RecentChange`
  CloudEvent family documented in [EVENTS.md](EVENTS.md)

## Installation

Requires Python 3.10 or later.

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/wikimedia-eventstreams
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md)
instructions.

## How to Use

After installation, the tool can be run with `wikimedia-eventstreams`.

### Probe the Live Stream

Print a few live events without Kafka:

```bash
wikimedia-eventstreams probe
```

Limit the probe:

```bash
wikimedia-eventstreams probe --max-events 2 --duration 10
```

### Stream to Kafka

#### Using a Connection String

```bash
wikimedia-eventstreams feed \
    --connection-string "<your_connection_string>"
```

#### Using Kafka Parameters Directly

```bash
wikimedia-eventstreams feed \
    --kafka-bootstrap-servers "<bootstrap_servers>" \
    --kafka-topic "<topic_name>" \
    --sasl-username "<username>" \
    --sasl-password "<password>"
```

### Command-Line Arguments

| Argument | Env Var | Description |
|----------|---------|-------------|
| `-c`, `--connection-string` | `CONNECTION_STRING` | Event Hubs / Fabric connection string |
| `--kafka-bootstrap-servers` | `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers |
| `--kafka-topic` | `KAFKA_TOPIC` | Kafka topic name |
| `--sasl-username` | `SASL_USERNAME` | SASL PLAIN username |
| `--sasl-password` | `SASL_PASSWORD` | SASL PLAIN password |
| `--state-file` | `WIKIMEDIA_EVENTSTREAMS_STATE_FILE` | Resume and dedupe state file |
| `--flush-interval` | `WIKIMEDIA_EVENTSTREAMS_FLUSH_INTERVAL` | Flush Kafka every N events |
| `--dedupe-size` | `WIKIMEDIA_EVENTSTREAMS_DEDUPE_SIZE` | Number of recent event IDs to retain |
| `--max-retry-delay` | `WIKIMEDIA_EVENTSTREAMS_MAX_RETRY_DELAY` | Maximum reconnect delay in seconds |
| `--user-agent` | `WIKIMEDIA_EVENTSTREAMS_USER_AGENT` | HTTP `User-Agent` header sent to Wikimedia |

## Event Model Notes

The payload closely follows Wikimedia's `mediawiki/recentchange` schema.
Three small normalizations keep the generated Python types sane and make the
CloudEvents contract self-describing from the data payload:

1. `event_id` is copied from `meta.id`.
2. `event_time` is copied from `meta.dt`.
3. Upstream `$schema` becomes `schema_uri`.
4. Upstream `log_params`, which may be an object, array, or string, is
   serialized into `log_params_json`.

The CloudEvents Kafka key and subject are both the globally unique
Wikimedia event UUID from `meta.id`. That is the most stable identity in
this public multi-wiki stream.
