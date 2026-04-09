# GraceDB Gravitational Wave Candidate Alerts

GraceDB (Gravitational-Wave Candidate Event Database) is a public database
maintained by the LIGO/Virgo/KAGRA collaboration that tracks gravitational wave
candidate events (superevents) detected by the worldwide network of
gravitational wave observatories.

This bridge polls the GraceDB public REST API for new superevents and forwards
them to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

## Source

- **API**: https://gracedb.ligo.org/api/superevents/?format=json
- **Auth**: None (public read access)
- **Update frequency**: Events posted within seconds of detection; bridge polls
  every 2 minutes
- **Coverage**: Global — LIGO Hanford (H1), LIGO Livingston (L1), Virgo (V1),
  KAGRA (K1)

## Events

The bridge emits a single event type, documented in [EVENTS.md](EVENTS.md):

- `org.ligo.gracedb.Superevent` — Gravitational wave candidate superevent with
  ID, category, false alarm rate, labels, preferred pipeline event metadata.

## Related

- [GraceDB Web Interface](https://gracedb.ligo.org/)
- [GraceDB API Docs](https://gracedb.ligo.org/documentation/rest.html)
- [LIGO Scientific Collaboration](https://www.ligo.org/)
