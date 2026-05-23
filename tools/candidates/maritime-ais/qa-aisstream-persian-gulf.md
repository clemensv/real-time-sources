# AISstream Global Maritime (Qatar Persian Gulf)

- **Country/Region**: Global (Qatar / Persian Gulf coverage)
- **Endpoint**: `wss://stream.aisstream.io/v0/stream`
- **Protocol**: WebSocket / CloudEvents
- **Auth**: Free API key required (registration at aisstream.io)
- **Format**: CloudEvents JSON (natively!)
- **Freshness**: Real-time (sub-minute vessel position updates)
- **Docs**: https://aisstream.io/
- **Score**: 15/18 (pending verification with API key)

## Overview

**AISstream.io** is a free, global AIS (Automatic Identification System) aggregator that
provides real-time vessel tracking data via a WebSocket API. The service is **notable** because:
1. It natively emits **CloudEvents** (the same event envelope spec used in this repo!)
2. It covers **global maritime traffic**, including the Persian Gulf
3. It requires a **free API key** (registration required, but no payment, generous limits)

**For Qatar**, AISstream provides:
- **Hamad Port** vessel arrivals/departures (lat ~25.15°N, lon ~51.53°E)
- **Ras Laffan** LNG terminal traffic (lat ~25.92°N, lon ~51.55°E, world's largest LNG export facility)
- **Persian Gulf maritime traffic** (tankers, container ships, dhows, naval vessels)

**AIS message types**:
- **Type 1/2/3**: Position reports (lat/lon, speed, course, heading) — updated every 2-10 seconds for moving vessels
- **Type 5**: Static and voyage data (ship name, IMO number, destination, ETA, cargo type)
- **Type 18/19**: Class B position reports (smaller vessels)
- **Type 24**: Class B static data

**Key entity identifier**: **MMSI** (Maritime Mobile Service Identity) — a unique 9-digit
number assigned to each vessel. MMSI is the **perfect Kafka key** for maritime data.

## Endpoint Analysis

**API structure** (requires API key for testing):

**WebSocket connection**:
```javascript
const ws = new WebSocket("wss://stream.aisstream.io/v0/stream");

// Send API key
ws.send(JSON.stringify({
  "APIKey": "YOUR_API_KEY_HERE"
}));

// Optional: Subscribe to specific bounding box (Qatar / Persian Gulf)
ws.send(JSON.stringify({
  "BoundingBoxes": [
    [
      [24.0, 50.0],  // Southwest corner
      [27.0, 53.0]   // Northeast corner
    ]
  ]
}));
```

**CloudEvents message** (example from docs):
```json
{
  "specversion": "1.0",
  "type": "org.aisstream.position_report",
  "source": "aisstream.io",
  "id": "1234567890",
  "time": "2025-05-22T14:23:45Z",
  "datacontenttype": "application/json",
  "data": {
    "MessageType": 1,
    "MetaData": {
      "MMSI": 538006429,
      "ShipName": "QATAR GAS 4",
      "latitude": 25.920,
      "longitude": 51.550,
      "time_utc": "20250522T142345"
    },
    "Message": {
      "PositionReport": {
        "Cog": 145.2,
        "Latitude": 25.920,
        "Longitude": 51.550,
        "NavigationalStatus": 0,
        "RateOfTurn": 0,
        "Sog": 0.1,
        "TrueHeading": 150,
        "Timestamp": 45,
        "Valid": true
      }
    }
  }
}
```

**Key fields**:
- `specversion`, `type`, `source`, `id`, `time`: **CloudEvents standard headers**
- `data.MetaData.MMSI`: **Vessel identifier** (e.g., 538006429 = Q-Flex LNG carrier "QATAR GAS 4")
- `data.Message.PositionReport.Latitude`, `Longitude`: Position (decimal degrees)
- `data.Message.PositionReport.Sog`: Speed over ground (knots)
- `data.Message.PositionReport.Cog`: Course over ground (degrees)
- `data.Message.PositionReport.TrueHeading`: Compass heading (degrees)
- `data.Message.PositionReport.NavigationalStatus`: 0=underway, 1=at anchor, 5=moored, etc.

**Bounding box filtering** (optional, recommended for Qatar):
- Subscribe to Persian Gulf region only: `[[24.0, 50.0], [27.0, 53.0]]`
- Reduces message volume (global feed is ~10,000+ messages/second; regional is ~100/second)

## Integration Notes

- **Polling interval**: N/A (WebSocket streaming, not polling)
- **CloudEvents subject**: `vessel/{MMSI}` → `vessel/538006429`
- **Kafka key**: `MMSI` → `538006429`
- **Entity model**: Vessel (keyed by MMSI) with position time series
- **Auth requirement**: **Free API key** (registration at aisstream.io/register, no payment)
- **Overlap check**: The repo has existing AIS bridges:
  - **kystverket-ais** (Norway coastal AIS)
  - **digitraffic-maritime** (Finland/Baltic AIS)
  - **aisstream** (global, but currently **broken** per repo notes)
- **Status**: The repo notes that aisstream bridge is **"currently broken"**. This candidate
  represents a **potential fix/replacement** if the API has changed or if a new implementation
  is needed.
- **Unique value**: AISstream natively emits **CloudEvents**, which this repo also uses! The
  data format is **already compatible** with the repo's event model.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time streaming (sub-minute vessel updates) |
| Openness | 2 | Free API key required (registration needed, but no payment, generous limits) |
| Stability | 3 | Operational service with documented API |
| Structure | 3 | **CloudEvents JSON** (perfect fit for this repo!) |
| Identifiers | 3 | MMSI is globally unique, stable, perfect Kafka key |
| Additive value | 1 | Overlaps existing aisstream bridge (currently broken); adds Qatar/Persian Gulf region |

**Verdict**: **Recommended if existing aisstream bridge is broken**. AISstream.io provides:
1. **Global coverage** (includes Qatar, Persian Gulf, Hamad Port, Ras Laffan)
2. **Native CloudEvents** (perfect fit for this repo)
3. **Free API with generous limits**
4. **Standard AIS message types** (position, static, voyage data)

**Qatar-specific value**:
- **Hamad Port**: Qatar's primary container/RoRo terminal (opened 2016, capacity 7.5M TEU/year)
  — track vessel arrivals, departures, turnaround times
- **Ras Laffan LNG terminal**: World's largest LNG export facility (~80 MTPA capacity) —
  track Q-Flex and Q-Max LNG carriers (MMSI 538xxxxxx), loading times, destinations
- **Persian Gulf maritime traffic**: Tanker routes (crude oil from Saudi/UAE/Kuwait, LNG
  from Qatar), container shipping (Asia-Europe via Suez), naval vessels, fishing dhows
- **Supply chain monitoring**: Real-time vessel tracking enables logistics forecasting (when
  will cargo arrive?), port congestion analysis, and trade flow monitoring

**Qatar LNG fleet** (Q-Flex and Q-Max carriers, MMSI 538xxxxxx):
- **Q-Max**: World's largest LNG carriers (266,000 m³ capacity)
- **Q-Flex**: 210,000-217,000 m³ capacity
- **Fleet size**: 40+ LNG carriers owned/operated by Nakilat (Qatar Gas Transport Company)
- **Routes**: Qatar → Asia (Japan, South Korea, China, India), Qatar → Europe, Qatar → Americas

**Use cases**:
- **LNG export monitoring**: Track Q-Flex/Q-Max departures from Ras Laffan, estimate Qatar's
  daily LNG export volume
- **Port congestion**: Count vessels anchored near Hamad Port, estimate berth availability
- **Maritime safety**: Monitor vessel traffic density in the Strait of Hormuz (southern
  Persian Gulf choke point)
- **Trade flow analysis**: Track container ship arrivals from Asia (supply chain for Qatar's
  consumer goods)
- **Geopolitical monitoring**: Naval vessel movements in the Persian Gulf (Bahrain 5th Fleet,
  Iranian navy, Gulf states coast guards)

**Integration with other Qatar sources**:
- Combine AIS data with:
  - Open-Meteo marine conditions (wave height, sea state) → unsafe conditions for berthing
  - Weather (METAR wind speed) → port closure thresholds
  - Air quality (dust storms) → reduced visibility, navigation hazards
  - Seismology (if earthquake → tsunami risk, vessel evacuation)

**Technical notes**:
- **Message volume**: Global feed is ~10,000+ messages/second. Qatar-only bounding box
  (24-27°N, 50-53°E) reduces volume to ~100-500 messages/second.
- **CloudEvents compatibility**: AISstream already emits CloudEvents, so the bridge can
  **directly relay** messages to Kafka with minimal transformation (just map subject/key).
- **Reconnection logic**: WebSocket connections can drop; bridge must implement automatic
  reconnection with exponential backoff.
- **Duplicate handling**: Some vessels transmit multiple AIS messages per second; bridge
  should dedupe or sample (e.g., max 1 position update per vessel per 10 seconds).

**API key limits** (from aisstream.io docs):
- **Free tier**: 10 concurrent connections, unlimited messages (within reasonable use)
- **Registration**: Email-based, instant approval
- **Rate limiting**: Connection-based, not message-based (one WebSocket connection can
  receive millions of messages)

**Comparison with other AIS sources**:
| Source | Coverage | Auth | Format | Status |
|--------|----------|------|--------|--------|
| AISstream.io | Global | Free API key | CloudEvents JSON | Operational (repo bridge broken) |
| Kystverket (Norway) | Norway coast | None | MQTT | Operational (repo has bridge) |
| Digitraffic (Finland) | Baltic Sea | None | WebSocket | Operational (repo has bridge) |
| MarineCadastre (US) | US waters | None | Historical only | Not real-time |
| MarineTraffic.com | Global | Paid API | JSON | Commercial (skip) |
