# Hamburg Elektro Ladestandorte

**Country/Region**: Germany — Hamburg
**Publisher**: Behörde für Wirtschaft, Arbeit und Innovation (BWAI) / Freie und Hansestadt Hamburg
**NAP / Catalog**: https://mobilithek.info/offers/-5494354146735462252
**Public Endpoints**:
- https://api.hamburg.de/datasets/v1/emobility
- https://api.hamburg.de/datasets/v1/emobility/collections
- https://iot.hamburg.de/v1.1/Datastreams?$filter=properties/layerName%20eq%20'Status_E-Ladepunkt'&$count=true
- https://iot.hamburg.de/v1.1/Things?$filter=Datastreams/properties/serviceName%20eq%20'HH_STA_E-Ladestationen'&$count=true
**Documentation**:
- https://api.hamburg.de/datasets/v1/emobility/api?f=html
- https://metaver.de/trefferanzeige?docuuid=07302A1A-3250-4F0F-9F6E-96C508288D03
**Protocol**: HTTPS pull
**Auth**: None observed during probe
**Data Format**: OGC API Features JSON, SensorThings v1.1 JSON, GeoJSON/WFS/WMS distributions on the Mobilithek offer
**Real-Time Status**: Yes — observed datastream results include `AVAILABLE`, `CHARGING`, `FINISHING`, `PREPARING`, `SUSPENDEDEV`, `SUSPENDEDEVSE`, and `UNAVAILABLE`
**Update Frequency**: Near-real-time; public SensorThings observations updated on 2026-04-07 and 2026-04-08 during the probe
**License**: Public Hamburg open-data publication; exact reuse terms should be confirmed from dataset metadata

## What It Provides

Hamburg publishes `Elektro Ladestandorte Hamburg` through Mobilithek and its own
OGC API / SensorThings stack. The OGC API landing page explicitly says the
dataset contains the publicly accessible EV charging locations in Hamburg and
that the charge-point operating status is published in real time as `frei`,
`belegt`, `außer Betrieb`, and `keine Daten`.

Unlike many NAP catalog entries that only point at metadata, Hamburg's public API
is directly usable and exposes both static station information and live
charge-point status without authentication.

## API Details

The public landing page is:

```text
GET https://api.hamburg.de/datasets/v1/emobility
```

During the probe, it returned:
- an OGC API landing document for `Elektro Ladestandorte Hamburg`
- links to `collections`, OpenAPI docs, and the metaver metadata page
- a German description explicitly stating that real-time charge-point status is included

The strongest live-status evidence is the SensorThings service:

```text
GET https://iot.hamburg.de/v1.1/Datastreams?$filter=properties/layerName eq 'Status_E-Ladepunkt'&$count=true
```

During the probe, it exposed:
- `@iot.count = 2,152` charge-point datastreams
- `@iot.count = 1,066` station `Things` for `HH_STA_E-Ladestationen`
- stable asset IDs such as `DE*HHM*E1011`
- connector/datastream identifiers such as `Ladepunkt DE*HHM*E8099*01`
- OCPP-grounded observed property text: `Charge Point availability of a public Charge Station according to OCPP 2.0`
- live observation values including `AVAILABLE`, `CHARGING`, `FINISHING`, `PREPARING`, `SUSPENDEDEV`, `SUSPENDEDEVSE`, and `UNAVAILABLE`

Each datastream also carries useful static attributes such as `chargingProtocol`,
`connectorType`, `current`, and geographic coordinates.

## Freshness Assessment

This is a genuine live-status source. The public SensorThings observations
changed on current-day timestamps during the probe, and the datastream histories
showed actual state transitions rather than static registry records.

The main limitation is geographic scope. This is a Hamburg city feed, not a
nationwide German aggregation.

## Entity Model

- **Station / Thing**: Hamburg charging station keyed by stable `assetID`
- **Charge Point / Datastream**: per-connector or per-EVSE status stream
- **Observation**: timestamped status event
- **Connector metadata**: connector type, current, charging protocol
- **Location**: coordinates and street address

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Same-day SensorThings observations and state transitions were observed directly |
| Openness | 2 | Public unauthenticated APIs are available, but licence terms still need explicit confirmation from metadata |
| Stability | 3 | Government-published open-data service and Mobilithek catalog entry |
| Structure | 3 | OGC API Features plus SensorThings v1.1 with OpenAPI docs |
| Identifiers | 3 | Stable station and charge-point identifiers are present |
| Additive Value | 2 | Strong German city-level live feed, but narrower than a state or national aggregation |
| **Total** | **16/18** | |

## Notes

- This is the second clearly confirmed German public live-status source found on Mobilithek after MobiData BW.
- Hamburg is particularly valuable because it shows an alternate technical pattern from Baden-Württemberg: OGC API plus SensorThings rather than DATEX-first delivery.
- The dataset landing page and the SensorThings API independently confirm that the status feed is public and real-time.