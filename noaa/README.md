# NOAA Data Poller

The NOAA Data Poller is a tool designed to periodically fetch data from NOAA (National Oceanic and Atmospheric Administration) and send it to a specified Apache Kafka topic using SASL PLAIN authentication.

## Features

- Polls various NOAA data products including water level, air temperature, wind, air pressure, water temperature, and more.
- Sends the data to a Kafka topic in the form of CloudEvents.
- Uses SASL PLAIN authentication for Kafka communication.
- Stores the last polled times for each station and product to avoid duplicate data fetching.

## Requirements

- Python 3.8+

## Installation

Install the required Python packages using pip:

```sh
pip install requests confluent_kafka cloudevents
```

## Usage

The NOAA Data Poller can be run from the command line. Below are the available command-line arguments:

```sh
python noaa_data_poller.py --last-polled-file LAST_POLLED_FILE --kafka-bootstrap-servers KAFKA_BOOTSTRAP_SERVERS --kafka-topic KAFKA_TOPIC --sasl-username SASL_USERNAME --sasl-password SASL_PASSWORD --connection-string CONNECTION_STRING
```

### Arguments

- `--last-polled-file`: File to store the last polled times for each station and product. Default is `~/.noaa_last_polled.json`.
- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Azure Event Hubs or Microsoft Fabric Event Streams connection string.

### Example

```sh
python noaa_data_poller.py --last-polled-file ~/.noaa_last_polled.json --kafka-bootstrap-servers your.kafka.server:9093 --kafka-topic noaa-data --sasl-username your_username --sasl-password your_password
```

## Environment Variables

The tool can also be configured using environment variables as an alternative to command-line arguments.

- `NOAA_LAST_POLLED_FILE`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_TOPIC`
- `SASL_USERNAME`
- `SASL_PASSWORD`
- `CONNECTION_STRING`

## Logging and Error Handling

The tool logs progress and errors to the console. Ensure proper monitoring of logs for troubleshooting and maintenance.


##  Deploying as a Container to Azure Container Instances

The NOAA Data Poller can be deployed as a container to Azure Container Instances. 

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2real-time-sources%2Fmain%2Fnoaa%2Fazure-template.json)

## Contributing

Contributions are welcome. Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or issues, please open an issue in the repository or contact the maintainer.

