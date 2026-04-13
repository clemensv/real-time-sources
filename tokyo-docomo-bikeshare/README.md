# Tokyo Docomo Bikeshare

Real-time bikeshare data for **Tokyo Docomo Bikeshare** (ドコモ・バイクシェア),
Japan's largest bikeshare network with 1,794 dock-based stations across the central
wards of Tokyo (Chiyoda, Minato, Shibuya, Shinjuku, and others).

Data is sourced from the [Open Data Platform for Transportation (ODPT)](https://developer-dc.odpt.org/)
which publishes the system as a standard GBFS 2.3 feed.

## Data model

### Event families

| Family | Description |
|---|---|
| `BikeshareSystem` | System-level metadata (name, operator, timezone, URLs). Emitted at startup and refreshed hourly. |
| `BikeshareStation` | Static station information: location, name (bilingual Japanese/English), capacity. Emitted at startup and refreshed hourly. |
| `BikeshareStationStatus` | Real-time availability per station: bikes available, docks available, operational flags. Updated every 60 seconds. |

### Kafka key model

| Event | Kafka key |
|---|---|
| `BikeshareSystem` | `{system_id}` |
| `BikeshareStation` | `{system_id}/{station_id}` |
| `BikeshareStationStatus` | `{system_id}/{station_id}` |

Station and status events share the same key so consumers can join reference and
telemetry by Kafka partition assignment or a simple dict lookup.

## Upstream API

| Feed | URL |
|---|---|
| Autodiscovery | `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json` |
| System information | `…/system_information.json` |
| Station information | `…/station_information.json` |
| Station status | `…/station_status.json` |

**Auth**: none required  
**License**: ODPT open data license  
**Protocol**: GBFS 2.3

## Running the bridge

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Event schemas

See [EVENTS.md](EVENTS.md) for full CloudEvents field descriptions.
