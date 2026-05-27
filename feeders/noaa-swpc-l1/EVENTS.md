# NOAA SWPC L1 Propagated Solar Wind Events

This document describes the events emitted by the NOAA SWPC L1 propagated
solar wind bridge.

- [gov.noaa.swpc.l1](#message-group-govnoaaswpcl1)
  - [gov.noaa.swpc.l1.PropagatedSolarWind](#message-govnoaaswpcl1propagatedsolarwind)

---

## Message Group: gov.noaa.swpc.l1

The group contains one event type sourced from
`GET https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json`.
The upstream document is a 7-day rolling window in array-of-arrays form,
with the column header at index 0 and one observation per minute
thereafter.

---

### Message: gov.noaa.swpc.l1.PropagatedSolarWind

One minute-resolution solar-wind observation at L1 with forward-
propagated Earth-arrival timestamp. Fuses plasma
(speed/density/temperature), magnetic field (Bx/By/Bz/Bt in GSM), and
bulk velocity vector (Vx/Vy/Vz in GSM) into a single row per `time_tag`.
The `propagated_time_tag` field is the upstream's predicted Earth arrival
time for the solar-wind parcel observed at L1 at `time_tag`. The
CloudEvent `time` attribute mirrors `time_tag`; consumers that need the
Earth-arrival time must read `data.propagated_time_tag` instead.

#### CloudEvents Attributes

| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `gov.noaa.swpc.l1.PropagatedSolarWind` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Stable spacecraft channel identifier | `uritemplate` | `False` | `{spacecraft}` |
| `time` | L1 observation time | `uritemplate` | `False` | `{time_tag}` |

Transport identity is aligned across protocols:

| Transport | Identity value |
|---|---|
| Kafka key | `{spacecraft}` |
| MQTT topic | `space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind` |
| AMQP subject | `{spacecraft}` |
| AMQP `x-opt-partition-key` | `{spacecraft}` |

#### Schema

##### Record: PropagatedSolarWind

One minute-resolution solar-wind observation at the Sun-Earth Lagrange-1
(L1) point with forward-propagated Earth-arrival timestamp. Fuses plasma
(speed/density/temperature), magnetic-field (Bx/By/Bz/Bt in GSM
coordinates), and bulk velocity (Vx/Vy/Vz in GSM coordinates) into one
row per `time_tag`. Sourced from `GET
https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json`
— a 7-day rolling window in array-of-arrays form, with the column header
at index 0 and one observation per minute thereafter. The operational
primary spacecraft is NOAA's DSCOVR; NASA's ACE serves as the backup.
Many sub-fields are nullable: DSCOVR's magnetometer experiences routine
gaps, and DSCOVR does not measure the Vx/Vy/Vz velocity components
reliably (the upstream nearly always emits null for those). Consumers
must treat plasma and magnetic-field measurements as independently
optional and not skip rows that have only partial values.

| **Field Name** | **Type** | **Unit** | **Nullable** | **Description** |
|---|---|---|---|---|
| `spacecraft` | `string` enum (`dscovr`, `ace`) |  | No | Stable channel identifier for the source spacecraft at L1. **Synthesized by the bridge — not present in the upstream payload.** Set to `dscovr` for the operational primary, `ace` for the backup. Used as the CloudEvent `subject`, the Kafka partition key, the MQTT topic `{spacecraft}` segment, the AMQP message subject, and the AMQP `x-opt-partition-key` message annotation. SWPC does not currently disclose source spacecraft per row in the propagated-solar-wind feed; the bridge sets `dscovr` by default and exposes a configuration override for operators who know the active spacecraft has switched. |
| `time_tag` | `datetime` |  | No | Wall-clock time the upstream observation was taken at L1, in ISO 8601 / RFC 3339 with explicit UTC offset. Upstream emits this in `YYYY-MM-DD HH:MM:SS.fff` form with implicit UTC; the bridge normalises to RFC 3339 with explicit `Z`. Minute-aligned. Strictly monotonic across the 7-day rolling window. |
| `propagated_time_tag` | `datetime` |  | No | Predicted wall-clock time at which the solar-wind parcel observed at L1 at `time_tag` is expected to reach Earth's magnetopause, computed by SWPC from the observed bulk speed and the L1-to-Earth distance. Typically 30-60 minutes after `time_tag` — always `propagated_time_tag > time_tag`. This lead time is the operational value of the propagated product: downstream geomagnetic-storm forecasts trigger from `propagated_time_tag`, not `time_tag`. RFC 3339 with explicit `Z`. |
| `speed` | `double` / `null` | km/s | Yes | Bulk solar-wind speed measured at L1 by the spacecraft's Faraday cup / plasma instrument. Quiet solar wind is 300-500 km/s; high-speed streams from coronal holes can reach 800 km/s; coronal-mass-ejection (CME) shock fronts have been observed above 2000 km/s. Null when the upstream plasma instrument has no valid measurement for that minute. Unit: kilometres per second. |
| `density` | `double` / `null` | cm⁻³ | Yes | Proton number density measured at L1. Quiet solar wind is 1-10 p/cm³; CME sheath / heliospheric current sheet crossings can reach 50-100 p/cm³ briefly. Null when the upstream plasma instrument has no valid measurement. Unit: particles (protons) per cubic centimetre. |
| `temperature` | `double` / `null` | K | Yes | Proton temperature at L1 in kelvin. Quiet solar wind is ~10^5 K; high-speed streams are hotter (~5×10^5 K); CME interiors are usually cooler than the ambient solar wind, while shocked sheath plasma can exceed 10^6 K. Null when the upstream plasma instrument has no valid measurement. Unit: kelvin. |
| `bx` | `double` / `null` | nT | Yes | Bx component of the interplanetary magnetic field at L1 in Geocentric Solar Magnetospheric (GSM) coordinates — the component pointing from Earth toward the Sun. Quiet solar wind: \|Bx\| typically 1-5 nT; CME magnetic clouds: up to 50 nT. Wire values are nanotesla (nT); the JsonStructure `unit` is `nT` (not the SI base unit T). Null when the upstream magnetometer has no valid measurement (DSCOVR magnetometer experiences routine gaps). |
| `by` | `double` / `null` | nT | Yes | By component of the interplanetary magnetic field at L1 in GSM coordinates — the component pointing in the direction of Earth's orbital motion projected onto the magnetic equator. Quiet solar wind: \|By\| 1-5 nT. Wire values are nanotesla (nT); JsonStructure `unit` is `nT`. Null on magnetometer gaps. |
| `bz` | `double` / `null` | nT | Yes | Bz component of the interplanetary magnetic field at L1 in GSM coordinates — the component perpendicular to Earth's orbital plane, positive northward. **The single most operationally important field in this schema**: sustained southward Bz (negative values, especially Bz < -10 nT for ≥ 30 minutes) couples solar-wind energy into Earth's magnetosphere via dayside magnetic reconnection and drives geomagnetic storms. Bz is the principal input to the Dst, Kp, and Ap forecast models downstream of this feed. Wire values are nanotesla (nT); JsonStructure `unit` is `nT`. Null on magnetometer gaps — null Bz means no forecasting signal for that minute, not a quiet condition. |
| `bt` | `double` / `null` | nT | Yes | Total magnetic-field magnitude at L1: Bt = sqrt(Bx² + By² + Bz²). Always non-negative. Quiet solar wind: 3-8 nT; CME magnetic clouds: 20-50 nT. Wire values are nanotesla (nT); JsonStructure `unit` is `nT`. Null when any of Bx/By/Bz is null. |
| `vx` | `double` / `null` | km/s | Yes | Vx component of the solar-wind bulk velocity at L1 in GSM coordinates — the radial (Sun-Earth) component. The dominant component of solar-wind flow; almost equal to -`speed` because the flow is nearly radially outward from the Sun (negative in GSM because GSM Vx points sunward while the wind flows anti-sunward). **DSCOVR typically does not measure this component reliably**; the upstream emits null for Vx/Vy/Vz on the majority of rows. Unit: kilometres per second. |
| `vy` | `double` / `null` | km/s | Yes | Vy component of the solar-wind bulk velocity at L1 in GSM coordinates — the dawn-dusk component. Typically small (\|Vy\| ≲ 100 km/s). DSCOVR usually emits null; treat as optional. Unit: kilometres per second. |
| `vz` | `double` / `null` | km/s | Yes | Vz component of the solar-wind bulk velocity at L1 in GSM coordinates — the north-south component. Typically small (\|Vz\| ≲ 100 km/s). DSCOVR usually emits null; treat as optional. Unit: kilometres per second. |

---

## On-the-wire example

Kafka, MQTT and AMQP use binary-mode CloudEvents by default, so the data
body and CloudEvent attributes are carried in transport-specific headers,
user properties or AMQP properties. The equivalent structured JSON
envelope is:

```json
{
  "specversion": "1.0",
  "type": "gov.noaa.swpc.l1.PropagatedSolarWind",
  "source": "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json",
  "id": "example-2025-01-15T12:34:00Z-dscovr",
  "time": "2025-01-15T12:34:00Z",
  "subject": "dscovr",
  "datacontenttype": "application/json",
  "data": {
    "spacecraft": "dscovr",
    "time_tag": "2025-01-15T12:34:00Z",
    "propagated_time_tag": "2025-01-15T13:12:00Z",
    "speed": 486.2,
    "density": 7.8,
    "temperature": 145000.0,
    "bx": -1.8,
    "by": 3.2,
    "bz": -11.4,
    "bt": 12.1,
    "vx": null,
    "vy": null,
    "vz": null
  }
}
```

Sample retained MQTT topic for the same event:

```text
space-weather/us/noaa-swpc/l1/dscovr/propagated-solar-wind
```

## Schema location

The authoritative contract is
[`xreg/noaa_swpc_l1.xreg.json`](xreg/noaa_swpc_l1.xreg.json):

```text
#/messagegroups/gov.noaa.swpc.l1/messages/gov.noaa.swpc.l1.PropagatedSolarWind
#/schemagroups/gov.noaa.swpc.l1.jstruct/schemas/gov.noaa.swpc.l1.PropagatedSolarWind
```

The generated KQL ingestion schema is
[`kql/noaa_swpc_l1.kql`](kql/noaa_swpc_l1.kql).
