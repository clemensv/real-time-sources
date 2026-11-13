# CelesTrak Orbital Data Events

<sub>satellite catalog (SATCAT) and GP orbital element sets, keyed by NORAD catalog number · Kafka · MQTT · AMQP · <a href="https://celestrak.org/">upstream</a> · <a href="https://celestrak.org/NORAD/documentation/gp-data-formats.php">API docs</a></sub>

## At a glance

- **Event types:** 3 documented event types (36 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{NORAD_CAT_ID}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `celestrak`. The record key is `{NORAD_CAT_ID}`. In plain language, `{NORAD_CAT_ID}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['celestrak'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `space/celestrak/satcat/+`, `space/celestrak/gp/+`, `space/celestrak/supgp/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('space/celestrak/satcat/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `celestrak`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/celestrak')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Satellite Catalog Entry

CloudEvents type: `org.celestrak.SatelliteCatalogEntry`

#### What it tells you

A CelesTrak SATCAT reference record for one catalogued space object. Emitted at start-up and on periodic refresh so consumers can resolve every `NORAD_CAT_ID` to a named, described object. Reference record for one object in the US Space Force satellite catalog (SATCAT), as published by CelesTrak at `satcat/records.php`.

#### Identity

Each event identifies the real-world resource with `{NORAD_CAT_ID}`. `{NORAD_CAT_ID}` is NORAD Catalog Number: the globally-recognised unique identifier for a tracked resident space object, assigned by the US Space Force 18th Space Defense Squadron. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `celestrak`, key `{NORAD_CAT_ID}` |
| `MQTT/5.0` | topic `space/celestrak/satcat/{NORAD_CAT_ID}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/celestrak`, message subject `{NORAD_CAT_ID}` |

#### Payload

`Satellite Catalog Entry` payloads are JSON object. Required fields: `NORAD_CAT_ID`.

- **`OBJECT_NAME`** (null or string, optional): Satellite / object name(s). May include alternate names in parentheses, an object-descriptor in brackets (e.g. `BREEZE-M DEB [TANK]`), and `&` to denote two or more attached objects. Mutable; never use as a key. From the SATCAT `OBJECT_NAME` field.
- **`OBJECT_ID`** (null or string, optional): International Designator (COSPAR ID), format `YYYY-NNNAAA`: launch year, launch number of the year, and one-to-three-letter piece designator (excluding I and O). Null for analyst objects with no associated launch. From the SATCAT `OBJECT_ID` field. Constraints: pattern `^[0-9]{4}-[0-9]{3}[A-Z]{0,3}$`.
- **`NORAD_CAT_ID`** (int32, required): NORAD Catalog Number: the globally-recognised unique identifier for a tracked resident space object, assigned by the US Space Force 18th Space Defense Squadron. One to nine digits (the five-digit range was exhausted at 100000+ on 2026-07-11; analyst objects use the 7995xxxxx range). Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic leaf and the AMQP subject. References the same object as the OrbitMeanElements event with the identical `NORAD_CAT_ID`. From the SATCAT `NORAD_CAT_ID` field. Constraints: minimum `1`, maximum `999999999`.
- **`OBJECT_TYPE`** (enum, optional): Object type: `PAY` payload, `R/B` rocket body, `DEB` other debris, `UNK` unknown. From the SATCAT `OBJECT_TYPE` field.
- **`OPS_STATUS_CODE`** (null or string, optional): Operational status code: `+` operational, `-` nonoperational, `P` partially operational, `B` backup/standby, `S` spare, `X` extended mission, `D` decayed, `?` unknown. An object is considered 'active' if its status is one of `+`,`P`,`B`,`S`,`X`. Modelled as a plain string because the code symbols (`+`,`-`,`?`) are not valid enumeration identifiers. From the SATCAT `OPS_STATUS_CODE` field; see https://celestrak.org/satcat/status.php.
- **`OWNER`** (null or string, optional): Owner / source: the country or organisation that owns the object, as a CelesTrak source code (e.g. `US`, `CIS`, `PRC`, `ESA`, `ISS`, `TBD`). From the SATCAT `OWNER` field; see https://celestrak.org/satcat/sources.php.
- **`LAUNCH_DATE`** (null or string, optional): Launch date as a UTC calendar date, an ISO 8601 `YYYY-MM-DD` string. Null if unknown. From the SATCAT `LAUNCH_DATE` field. Constraints: pattern `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`.
- **`LAUNCH_SITE`** (null or string, optional): Launch site code (e.g. `TYMSC` Baikonur/Tyuratam, `AFETR` Cape Canaveral, `FRGUI` Kourou). Null if unknown. From the SATCAT `LAUNCH_SITE` field; see https://celestrak.org/satcat/launchsites.php.
- **`DECAY_DATE`** (null or string, optional): Decay (re-entry) date as a UTC calendar date, an ISO 8601 `YYYY-MM-DD` string. Null while the object is still on orbit. From the SATCAT `DECAY_DATE` field (upstream empty string is mapped to null). Constraints: pattern `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`.
- **`PERIOD`** (null or double, optional): Orbital period, in minutes. Null when no current elements are available. From the SATCAT `PERIOD` field. Constraints: minimum `0`.
- **`INCLINATION`** (null or double, optional, °): Orbital inclination to the equator, in degrees (0-180). Null when no current elements are available. From the SATCAT `INCLINATION` field. Constraints: minimum `0`, maximum `180`.
- **`APOGEE`** (null or int32, optional): Apogee altitude above the Earth's surface, in kilometres (the farthest orbital point). Null when no current elements are available. From the SATCAT `APOGEE` field. Constraints: minimum `0`.
- **`PERIGEE`** (null or int32, optional): Perigee altitude above the Earth's surface, in kilometres (the closest orbital point). Null when no current elements are available. From the SATCAT `PERIGEE` field. Constraints: minimum `0`.
- **`RCS`** (null or double, optional): Radar Cross Section, in square metres -- a proxy for the object's size as seen by tracking radar. Null when not available. From the SATCAT `RCS` field. Constraints: minimum `0`.
- **`DATA_STATUS_CODE`** (enum, optional): Data status: `NCE` no current elements, `NIE` no initial elements, `NEA` no elements available. Null when elements are available. From the SATCAT `DATA_STATUS_CODE` field (upstream empty string is mapped to null).
- **`ORBIT_CENTER`** (null or string, optional): Orbit center: `EA` Earth, `EM` Earth-Moon barycenter, `EL1`/`EL2` Earth-Sun Lagrange points, `MO` Moon, `SU` Sun, `SS` solar-system escape, planetary bodies (`MA` Mars, `JU` Jupiter, `VE` Venus, ...), or a NORAD Catalog Number for an object docked to another catalogued object. Modelled as a plain string because the value space includes numeric catalog numbers. From the SATCAT `ORBIT_CENTER` field.
- **`ORBIT_TYPE`** (enum, optional): Orbit type: `ORB` orbiting, `LAN` landing, `IMP` impact, `DOC` docked to another catalogued object, `R/T` roundtrip. From the SATCAT `ORBIT_TYPE` field.
##### `OBJECT_TYPE` values

- `PAY`
- `R/B`
- `DEB`
- `UNK`
##### `DATA_STATUS_CODE` values

- `NCE`
- `NIE`
- `NEA`
##### `ORBIT_TYPE` values

- `ORB`
- `LAN`
- `IMP`
- `DOC`
- `R/T`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "OBJECT_NAME": "string",
  "OBJECT_ID": "string",
  "NORAD_CAT_ID": 0,
  "OBJECT_TYPE": "PAY",
  "OPS_STATUS_CODE": "string",
  "OWNER": "string",
  "LAUNCH_DATE": "string",
  "LAUNCH_SITE": "string",
  "DECAY_DATE": "string",
  "PERIOD": 0,
  "INCLINATION": 0,
  "APOGEE": 0,
  "PERIGEE": 0,
  "RCS": 0,
  "DATA_STATUS_CODE": "NCE",
  "ORBIT_CENTER": "string",
  "ORBIT_TYPE": "ORB"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Orbit Mean Elements

CloudEvents type: `org.celestrak.OrbitMeanElements`

#### What it tells you

A CelesTrak GP (General Perturbations) OMM orbital element set for one object. Emitted when a new or refreshed element set is observed. A General Perturbations (GP) orbital element set for one catalogued object, as published by CelesTrak at `NORAD/elements/gp.php`.

#### Identity

Each event identifies the real-world resource with `{NORAD_CAT_ID}`. `{NORAD_CAT_ID}` is NORAD Catalog Number: the globally-recognised unique identifier for a tracked resident space object, assigned by the US Space Force 18th Space Defense Squadron. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `celestrak`, key `{NORAD_CAT_ID}` |
| `MQTT/5.0` | topic `space/celestrak/gp/{NORAD_CAT_ID}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/celestrak`, message subject `{NORAD_CAT_ID}` |

#### Payload

`Orbit Mean Elements` payloads are JSON object. Required fields: `EPOCH`, `MEAN_MOTION`, `ECCENTRICITY`, `INCLINATION`, `RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY`, `EPHEMERIS_TYPE`, `CLASSIFICATION_TYPE`, `NORAD_CAT_ID`, `ELEMENT_SET_NO`, `REV_AT_EPOCH`, `BSTAR`, `MEAN_MOTION_DOT`, `MEAN_MOTION_DDOT`.

- **`OBJECT_NAME`** (null or string, optional): Satellite / object name (TLE Line 0). Up to 24 characters in the legacy TLE format; Unicode-capable in OMM. Mutable and not globally unique -- never use as a key. Null for uncatalogued / analyst objects that have no assigned name. From the CCSDS OMM `OBJECT_NAME` keyword.
- **`OBJECT_ID`** (null or string, optional): International Designator (COSPAR ID) of the object, format `YYYY-NNNAAA`: four-digit launch year, three-digit launch number of that year, and one-to-three-letter piece designator (letters I and O are excluded). Null for analyst objects with no associated launch. From the CCSDS OMM `OBJECT_ID` keyword. Constraints: pattern `^[0-9]{4}-[0-9]{3}[A-Z]{0,3}$`.
- **`EPOCH`** (datetime, required): UTC epoch of the element set: the reference instant to which every mean element below applies and from which an SGP4 propagator integrates. The upstream CCSDS OMM `EPOCH` keyword is an offset-less ISO 8601 value (UTC is implied by `TIME_SYSTEM=UTC`); the feeder normalizes it to a UTC-aware RFC 3339 timestamp with an explicit `+00:00` offset, e.g. `2026-07-15T18:23:37.536288+00:00`. From the CCSDS OMM `EPOCH` keyword.
- **`MEAN_MOTION`** (double, required, rev/day): Mean motion: the number of orbital revolutions the object completes per solar day, a Brouwer mean element consumed directly by the SGP4 propagator. Larger values correspond to lower orbits (~15.5 for the ISS in LEO, ~1.0 for geostationary objects). From the CCSDS OMM `MEAN_MOTION` keyword. Constraints: minimum `0`.
- **`ECCENTRICITY`** (double, required): Orbital eccentricity, dimensionless: 0 is a circular orbit and values approaching 1 are highly elliptical. In the legacy TLE this is stored as a leading-decimal integer; the OMM JSON gives the true fractional value. From the CCSDS OMM `ECCENTRICITY` keyword. Constraints: minimum `0`, maximum `1`.
- **`INCLINATION`** (double, required, deg (°)): Inclination of the orbital plane to Earth's equatorial plane, in degrees (0-180; > 90 indicates a retrograde orbit). From the CCSDS OMM `INCLINATION` keyword. Constraints: minimum `0`, maximum `180`.
- **`RA_OF_ASC_NODE`** (double, required, deg (°)): Right Ascension of the Ascending Node (RAAN), in degrees (0-360): the angle from the vernal equinox to the point where the orbit crosses the equatorial plane going north. From the CCSDS OMM `RA_OF_ASC_NODE` keyword. Constraints: minimum `0`, maximum `360`.
- **`ARG_OF_PERICENTER`** (double, required, deg (°)): Argument of pericenter (perigee), in degrees (0-360): the angle from the ascending node to the point of closest approach, measured in the orbital plane. From the CCSDS OMM `ARG_OF_PERICENTER` keyword. Constraints: minimum `0`, maximum `360`.
- **`MEAN_ANOMALY`** (double, required, deg (°)): Mean anomaly at epoch, in degrees (0-360): the fraction of the orbital period elapsed since pericenter passage expressed as an angle, used with the other elements to locate the object at `EPOCH`. From the CCSDS OMM `MEAN_ANOMALY` keyword. Constraints: minimum `0`, maximum `360`.
- **`EPHEMERIS_TYPE`** (int32, required): Ephemeris / orbital-model type. `0` denotes the SGP4 (SGP4/SDP4) mean-element theory, the only value distributed in public GP data. From the CCSDS OMM `EPHEMERIS_TYPE` keyword. Constraints: minimum `0`.
- **`CLASSIFICATION_TYPE`** (enum, required): Security classification of the element set (always `U` for public CelesTrak data). From the CCSDS OMM `CLASSIFICATION_TYPE` keyword.
- **`NORAD_CAT_ID`** (int32, required): NORAD Catalog Number: the globally-recognised unique identifier for a tracked resident space object, assigned by the US Space Force 18th Space Defense Squadron. One to nine digits -- regular objects exhausted the five-digit range (reaching 100000+) on 2026-07-11, and analyst objects use the 7995xxxxx range -- so this MUST be treated as an up-to-9-digit integer, never a fixed-width field. Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic leaf and the AMQP message subject for every event this source emits. From the CCSDS OMM `NORAD_CAT_ID` keyword. Constraints: minimum `1`, maximum `999999999`.
- **`ELEMENT_SET_NO`** (int32, required): Element set number: a counter incremented (modulo 1000) each time a new element set is generated for the object; 18 SDS frequently emits the placeholder `999`. From the CCSDS OMM `ELEMENT_SET_NO` keyword. Constraints: minimum `0`.
- **`REV_AT_EPOCH`** (int32, required): Revolution number at epoch: the integer count of orbital revolutions the object has completed since launch, as of `EPOCH`. From the CCSDS OMM `REV_AT_EPOCH` keyword. Constraints: minimum `0`.
- **`BSTAR`** (double, required, 1/ER): B* (BSTAR) drag term, in inverse Earth radii, used by SGP4 to model the effect of atmospheric drag. Physically meaningful only for low-Earth-orbit objects; may be zero (deep space) or negative. From the CCSDS OMM `BSTAR` keyword.
- **`MEAN_MOTION_DOT`** (double, required, rev/day^2): First time-derivative of the mean motion (one half of dn/dt), in revolutions per day squared -- the classical TLE 'ballistic coefficient' term. From the CCSDS OMM `MEAN_MOTION_DOT` keyword.
- **`MEAN_MOTION_DDOT`** (double, required, rev/day^3): Second time-derivative of the mean motion (one sixth of d2n/dt2), in revolutions per day cubed; almost always 0 under the SGP4 theory. From the CCSDS OMM `MEAN_MOTION_DDOT` keyword.
##### `CLASSIFICATION_TYPE` values

- `U`
- `C`
- `S`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "OBJECT_NAME": "string",
  "OBJECT_ID": "string",
  "EPOCH": "2024-01-01T00:00:00Z",
  "MEAN_MOTION": 0,
  "ECCENTRICITY": 0,
  "INCLINATION": 0,
  "RA_OF_ASC_NODE": 0,
  "ARG_OF_PERICENTER": 0,
  "MEAN_ANOMALY": 0,
  "EPHEMERIS_TYPE": 0,
  "CLASSIFICATION_TYPE": "U",
  "NORAD_CAT_ID": 0,
  "ELEMENT_SET_NO": 0,
  "REV_AT_EPOCH": 0,
  "BSTAR": 0,
  "MEAN_MOTION_DOT": 0,
  "MEAN_MOTION_DDOT": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Supplemental Orbit Mean Elements

CloudEvents type: `org.celestrak.SupplementalOrbitMeanElements`

#### What it tells you

A CelesTrak SupGP (Supplemental GP) OMM element set for one object, from an operator or analysis-centre source. Emitted when supplemental sources are configured. A Supplemental GP (SupGP) orbital element set for one catalogued object, as published by CelesTrak at `NORAD/elements/supplemental/sup-gp.php`.

#### Identity

Each event identifies the real-world resource with `{NORAD_CAT_ID}`. `{NORAD_CAT_ID}` is NORAD Catalog Number: the globally-recognised unique identifier for a tracked resident space object, assigned by the US Space Force 18th Space Defense Squadron. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `celestrak`, key `{NORAD_CAT_ID}` |
| `MQTT/5.0` | topic `space/celestrak/supgp/{NORAD_CAT_ID}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/celestrak`, message subject `{NORAD_CAT_ID}` |

#### Payload

`Supplemental Orbit Mean Elements` payloads are JSON object. Required fields: `EPOCH`, `MEAN_MOTION`, `ECCENTRICITY`, `INCLINATION`, `RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY`, `EPHEMERIS_TYPE`, `CLASSIFICATION_TYPE`, `NORAD_CAT_ID`, `ELEMENT_SET_NO`, `REV_AT_EPOCH`, `BSTAR`, `MEAN_MOTION_DOT`, `MEAN_MOTION_DDOT`.

- **`OBJECT_NAME`** (null or string, optional): Satellite / object name as published by the supplemental data provider. May carry provider annotations absent from standard GP data, e.g. an ISS ephemeris segment tag `ISS [Segment 01]` or a CPF prediction-centre tag in brackets. Mutable; never use as a key. From the CCSDS OMM `OBJECT_NAME` keyword.
- **`OBJECT_ID`** (null or string, optional): International Designator (COSPAR ID) of the object, format `YYYY-NNNAAA`: four-digit launch year, three-digit launch number of that year, and one-to-three-letter piece designator (letters I and O are excluded). Null for analyst objects with no associated launch. From the CCSDS OMM `OBJECT_ID` keyword. Constraints: pattern `^[0-9]{4}-[0-9]{3}[A-Z]{0,3}$`.
- **`EPOCH`** (datetime, required): UTC epoch of the element set: the reference instant to which every mean element below applies and from which an SGP4 propagator integrates. The upstream CCSDS OMM `EPOCH` keyword is an offset-less ISO 8601 value (UTC is implied by `TIME_SYSTEM=UTC`); the feeder normalizes it to a UTC-aware RFC 3339 timestamp with an explicit `+00:00` offset, e.g. `2026-07-15T18:23:37.536288+00:00`. From the CCSDS OMM `EPOCH` keyword.
- **`MEAN_MOTION`** (double, required, rev/day): Mean motion: the number of orbital revolutions the object completes per solar day, a Brouwer mean element consumed directly by the SGP4 propagator. Larger values correspond to lower orbits (~15.5 for the ISS in LEO, ~1.0 for geostationary objects). From the CCSDS OMM `MEAN_MOTION` keyword. Constraints: minimum `0`.
- **`ECCENTRICITY`** (double, required): Orbital eccentricity, dimensionless: 0 is a circular orbit and values approaching 1 are highly elliptical. In the legacy TLE this is stored as a leading-decimal integer; the OMM JSON gives the true fractional value. From the CCSDS OMM `ECCENTRICITY` keyword. Constraints: minimum `0`, maximum `1`.
- **`INCLINATION`** (double, required, deg (°)): Inclination of the orbital plane to Earth's equatorial plane, in degrees (0-180; > 90 indicates a retrograde orbit). From the CCSDS OMM `INCLINATION` keyword. Constraints: minimum `0`, maximum `180`.
- **`RA_OF_ASC_NODE`** (double, required, deg (°)): Right Ascension of the Ascending Node (RAAN), in degrees (0-360): the angle from the vernal equinox to the point where the orbit crosses the equatorial plane going north. From the CCSDS OMM `RA_OF_ASC_NODE` keyword. Constraints: minimum `0`, maximum `360`.
- **`ARG_OF_PERICENTER`** (double, required, deg (°)): Argument of pericenter (perigee), in degrees (0-360): the angle from the ascending node to the point of closest approach, measured in the orbital plane. From the CCSDS OMM `ARG_OF_PERICENTER` keyword. Constraints: minimum `0`, maximum `360`.
- **`MEAN_ANOMALY`** (double, required, deg (°)): Mean anomaly at epoch, in degrees (0-360): the fraction of the orbital period elapsed since pericenter passage expressed as an angle, used with the other elements to locate the object at `EPOCH`. From the CCSDS OMM `MEAN_ANOMALY` keyword. Constraints: minimum `0`, maximum `360`.
- **`EPHEMERIS_TYPE`** (int32, required): Ephemeris / orbital-model type. `0` denotes the SGP4 (SGP4/SDP4) mean-element theory, the only value distributed in public GP data. From the CCSDS OMM `EPHEMERIS_TYPE` keyword. Constraints: minimum `0`.
- **`CLASSIFICATION_TYPE`** (enum, required): Security classification of the element set (always `U` for public CelesTrak data). From the CCSDS OMM `CLASSIFICATION_TYPE` keyword.
- **`NORAD_CAT_ID`** (int32, required): NORAD Catalog Number: the globally-recognised unique identifier for a tracked resident space object, assigned by the US Space Force 18th Space Defense Squadron. One to nine digits -- regular objects exhausted the five-digit range (reaching 100000+) on 2026-07-11, and analyst objects use the 7995xxxxx range -- so this MUST be treated as an up-to-9-digit integer, never a fixed-width field. Used as the CloudEvents `subject`, the Kafka partition key, the MQTT topic leaf and the AMQP message subject for every event this source emits. From the CCSDS OMM `NORAD_CAT_ID` keyword. Constraints: minimum `1`, maximum `999999999`.
- **`ELEMENT_SET_NO`** (int32, required): Element set number: a counter incremented (modulo 1000) each time a new element set is generated for the object; 18 SDS frequently emits the placeholder `999`. From the CCSDS OMM `ELEMENT_SET_NO` keyword. Constraints: minimum `0`.
- **`REV_AT_EPOCH`** (int32, required): Revolution number at epoch: the integer count of orbital revolutions the object has completed since launch, as of `EPOCH`. From the CCSDS OMM `REV_AT_EPOCH` keyword. Constraints: minimum `0`.
- **`BSTAR`** (double, required, 1/ER): B* (BSTAR) drag term, in inverse Earth radii, used by SGP4 to model the effect of atmospheric drag. Physically meaningful only for low-Earth-orbit objects; may be zero (deep space) or negative. From the CCSDS OMM `BSTAR` keyword.
- **`MEAN_MOTION_DOT`** (double, required, rev/day^2): First time-derivative of the mean motion (one half of dn/dt), in revolutions per day squared -- the classical TLE 'ballistic coefficient' term. From the CCSDS OMM `MEAN_MOTION_DOT` keyword.
- **`MEAN_MOTION_DDOT`** (double, required, rev/day^3): Second time-derivative of the mean motion (one sixth of d2n/dt2), in revolutions per day cubed; almost always 0 under the SGP4 theory. From the CCSDS OMM `MEAN_MOTION_DDOT` keyword.
- **`RMS`** (null or double, optional): Root-mean-square of the orbit-determination fit residuals reported by the supplemental data provider -- a quality indicator for this element set. Present only in SupGP data (absent from standard 18 SDS GP data). From the CelesTrak SupGP `RMS` field.
- **`DATA_SOURCE`** (null or string, optional): Supplemental data source / provider code identifying who produced this element set and by which technique, e.g. `ISS-E` (ISS ephemeris), `SpaceX-E` (SpaceX ephemeris), `CPF` (consolidated laser-ranging predictions), `GPS-A` (GPS almanac), `Intelsat-E`. Unlike standard GP, a single object may have several SupGP element sets distinguished by `DATA_SOURCE` and `EPOCH`. From the CelesTrak SupGP `DATA_SOURCE` field.
##### `CLASSIFICATION_TYPE` values

- `U`
- `C`
- `S`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "OBJECT_NAME": "string",
  "OBJECT_ID": "string",
  "EPOCH": "2024-01-01T00:00:00Z",
  "MEAN_MOTION": 0,
  "ECCENTRICITY": 0,
  "INCLINATION": 0,
  "RA_OF_ASC_NODE": 0,
  "ARG_OF_PERICENTER": 0,
  "MEAN_ANOMALY": 0,
  "EPHEMERIS_TYPE": 0,
  "CLASSIFICATION_TYPE": "U",
  "NORAD_CAT_ID": 0,
  "ELEMENT_SET_NO": 0,
  "REV_AT_EPOCH": 0,
  "BSTAR": 0,
  "MEAN_MOTION_DOT": 0,
  "MEAN_MOTION_DDOT": 0,
  "RMS": 0,
  "DATA_SOURCE": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

The default payload remains JSON with a JSON Structure schema. The manifest also declares inherited `.avro` groups with Avro schemas and unchanged `application/json` payloads, and `.avro.binary` groups with `application/vnd.apache.org.avro+avro` payloads. These encoding variants retain the same event identities and transport routing. Binary Avro bytes inside structured JSON CloudEvents belong in `data_base64`; payload encoding is independent of the CloudEvents envelope mode.

Binary Avro is declared by the contract but is not yet a supported feeder output. [xregistry/codegen#670](https://github.com/xregistry/codegen/issues/670) tracks the producer-generation defect. The checked-in feeders continue to use their existing JSON producers. Avro schemas preserve RFC3339 strings as strings where no native timestamp mapping was already declared; optional JSON properties without a declared default use null defaults in Avro records.

MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/celestrak.xreg.json`](xreg/celestrak.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
