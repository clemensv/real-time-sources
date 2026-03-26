# RWS Waterwebservices (Netherlands) Water Level Bridge

This project bridges water level data from the Dutch
[Rijkswaterstaat Waterwebservices](https://waterwebservices.rijkswaterstaat.nl/)
API to Apache Kafka, emitting CloudEvents.

**Rijkswaterstaat** (RWS) is the executive agency of the Dutch Ministry of
Infrastructure and Water Management. It manages the main waterways, roads, and
water systems in the Netherlands and publishes real-time water data through the
Waterwebservices API.

## Data

- **Stations**: ~785 monitoring locations measuring water level across the Netherlands
- **Water Level**: Water height (WATHTE) for surface water (OW) in cm, 10-minute intervals
- **Polling interval**: 10 minutes

The API is a POST-based JSON REST service. No authentication required. Data is
published under CC0 (public domain).

## Usage

### List stations

```bash
python -m rws_waterwebservices list
```

### Get latest water level for a station

```bash
python -m rws_waterwebservices level HOlv
```

### Feed to Kafka

Using a connection string (Azure Event Hubs):

```bash
python -m rws_waterwebservices feed -c "Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..."
```

Using explicit Kafka configuration:

```bash
python -m rws_waterwebservices feed \
    --kafka-bootstrap-servers your-server:9093 \
    --kafka-topic rws-waterwebservices \
    --sasl-username '$ConnectionString' \
    --sasl-password 'your-connection-string'
```

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents message definitions.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker container deployment info.

## API Reference

- **Base URL**: `https://ddapi20-waterwebservices.rijkswaterstaat.nl`
- **Protocol**: POST-based JSON REST
- **Key endpoints**:
  - `METADATASERVICES/OphalenCatalogus` — catalog of available parameters
  - `ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen` — latest observations
  - `ONLINEWAARNEMINGENSERVICES/OphalenWaarnemingen` — historical observations
- **Swagger**: `https://ddapi20-waterwebservices.rijkswaterstaat.nl/swagger-ui/index.html`
- **No authentication required**
- **License**: CC0 (public domain)

## Daily Volume Estimate

- ~785 water level stations × 144 readings/day (10 min) = ~113,000 readings/day
- Each CloudEvent ≈ 500 bytes → ~57 MB/day
- Plus ~785 station reference events at startup
