# PTWC/NTWC Tsunami Bulletins Events

## Topics and Keys

| Topic | Key template | Message group | Event types |
|---|---|---|---|
| `ptwc-tsunami` | `{bulletin_id}` | `PTWC.Bulletins` | `TsunamiBulletin` |

## Event Metadata

- `source`: `https://www.tsunami.gov`
- `time`: Atom entry `updated` timestamp

## Event Types

### PTWC.TsunamiBulletin

Tsunami bulletin from NOAA's National Tsunami Warning Center (NTWC, Palmer AK)
or the Pacific Tsunami Warning Center (PTWC, Honolulu HI).

- `bulletin_id` — URN UUID from the Atom entry (key)
- `feed` — feed origin: PAAQ (Alaska/Pacific) or PHEB (Pacific/Atlantic)
- `center` — issuing center name
- `title` — location of the seismic event
- `updated` — bulletin timestamp
- `latitude`, `longitude` — earthquake epicenter
- `category` — threat level: Warning, Advisory, Watch, Information
- `magnitude` — preliminary earthquake magnitude (e.g., "5.2(mb)")
- `affected_region` — affected region description
- `note` — additional advisory text
- `bulletin_url` — URL to full text bulletin
- `cap_url` — URL to the CAP XML document

## Data Sources

- Pacific/Alaska: `https://www.tsunami.gov/events/xml/PAAQAtom.xml`
- Pacific/Atlantic: `https://www.tsunami.gov/events/xml/PHEBAtom.xml`

---

## Message Group: PTWC.Bulletins.mqtt

MQTT/5.0 transport variant for tsunami.gov PTWC/NTWC tsunami bulletins. Non-retained QoS-1 bulletin events route by basin, tsunami bulletin level, and bulletin id under alerts/intl/ptwc/ptwc-tsunami/... Basin is derived from the NOAA feed (PHEB=pacific, PAAQ=alaska); ptwc_level is the native bulletin category normalized to lowercase.

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin` | `PTWC.TsunamiBulletin` | `false` | `1` | `` |
