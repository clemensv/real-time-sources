# RSS Bridge Usage Guide

## Overview

**RSS Bridge** is a tool designed to fetch and process RSS/Atom feeds or OPML
feed lists, with the ability to publish feed data to Microsoft Fabric Event
Streams via Kafka. It can also handle the periodic polling of feeds, maintain a
cache of processed feed states, and handle backoff and rate-limiting.

## Installation

The tool is written in Python and requires Python 3.10 or later. You can
download Python from [here](https://www.python.org/downloads/) or get it from
the Microsoft Store if you are on Windows. You may also need to install the
`git` command line tool. You can download `git` from
[here](https://git-scm.com/downloads).

### Installation Steps

Having Python, you can install the tool in one shot from the command line as follows:

```bash
pip install git+https://github.com/clemensv/real-time-sources#subdirectory=gtfs
```

if you clone the repository, you can install the tool from the command line as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/rss
pip install .
```

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## Key Features:
- **Feed Processing**: Retrieve and parse RSS/Atom feeds and OPML files, and
  send the data to a Kafka topic.
- **State Management**: Track feed states to handle ETag caching, backoff, and
  skip rules.
- **Feed Store**: Add, remove, and show stored feeds from an OPML-style feed
  store.
- **Kafka Integration**: Send processed feed data to a Kafka topic with
  Microsoft Fabric Event Streams support.
  
## How to Use

The tool supports multiple subcommands:
- **Process Feeds (`process`)**: Fetches and processes feed items from URLs or OPML files.
- **Add Feeds (`add`)**: Adds new feed URLs or OPML files to the feed store.
- **Remove Feeds (`remove`)**: Removes specific feed URLs from the feed store.
- **Show Feeds (`show`)**: Displays all stored feed URLs.

The argument `--state-dir` is optional and common for all subcommands. It
specifies the directory for storing state files and the feed store. If not
provided, the default directory is the user's home directory.

### **Process Feeds (`process`)**

Fetches and processes feed items from URLs or OPML files and publishes them to a
Kafka topic as CloudEvents. The event format is described in
[EVENTS.md](EVENTS.md).

   
  - `--kafka-bootstrap-servers`: Kafka bootstrap servers (comma-separated list).
  - `--kafka-topic`: Kafka topic for publishing.
  - `--sasl-username`: SASL username for Kafka authentication.
  - `--sasl-password`: SASL password for Kafka authentication.
  - `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Streams [connection string](#connection-string-for-microsoft-event-hubs-or-fabric-event-streams) (obviates the need for and overrides other Kafka parameters).
  - `--state-dir`: Directory for storing state files.
  - `feed_urls`: List of RSS/Atom feed URLs or OPML URLs. These are optional if there are feeds registered in the feed store.
  


#### Example Usage for Kafka
   ```bash
   rssbridge process --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>" <feed_url1> <feed_url2>
   ```

#### Example Usage for Microsoft Event Hubs or Fabric Event Streams
    ```bash
    rssbridge process --connection-string "<your_connection_string>" <feed_url1> <feed_url2>
    ```

### Add Feeds (`add`)

Adds new feed URLs or OPML files to the feed store.

#### Example Usage

   ```bash
   rssbridge add <feed_url_or_opml>
   ```

### Remove Feeds (`remove`)

Removes specific feed URLs from the feed store.

#### Example Usage

```bash
rssbridge remove <feed_url>
```

### Show Feeds (`show`)

Displays all stored feed URLs.

#### Example Usage

```bash
rssbridge show
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

Instead of manually passing the Kafka connection parameters (`bootstrap-servers`, `topic`, `username`, and `password`), you can use a **connection string** for **Microsoft Event Hubs** or **Microsoft Fabric Event Streams**. This connection string simplifies the configuration by consolidating these parameters.

#### Format
The connection string should be provided in the following format:
```bash
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

#### Usage in the Command Line
You can provide the connection string using the `--connection-string` flag:

```bash
rssbridge process --connection-string "<your_connection_string>" <feed_url1> <feed_url2>
```

The tool automatically parses the connection string to extract the following
details:
- **Bootstrap Servers**: Derived from the `Endpoint` value.
- **Kafka Topic**: Derived from the `EntityPath` value.
- **SASL Username and Password**: The username is set to `'$ConnectionString'`
  and the password is set to the entire connection string.

This simplifies the Kafka configuration for Microsoft Event Hubs and Fabric
Event Streams.

### Environment Variables
The tool supports the following environment variables to avoid passing them via
the command line:
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers (comma-separated list).
- `KAFKA_TOPIC`: Kafka topic for publishing.
- `SASL_USERNAME`: SASL username for Kafka authentication.
- `SASL_PASSWORD`: SASL password for Kafka authentication.
- `FEED_URLS`: Comma-separated list of RSS/Atom feed URLs.
- `STATE_DIR`: Directory for storing state files.
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream
  connection string.

### State Management

The tool maintains a state file (`~/.rss-grabber.json`) that stores the ETag and
the time of the next polling operation for each feed URL. The feed store is
stored in OPML format (`~/.rss-grabber-feedstore.xml`).


