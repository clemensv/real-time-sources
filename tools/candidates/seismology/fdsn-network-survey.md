# FDSN Event Service Network — Node Survey

## Overview

The International Federation of Digital Seismograph Networks (FDSN) defines a standard web service specification for earthquake event data. Multiple institutions worldwide implement this spec, creating a federated network of interoperable seismic data sources. This document surveys all known FDSN event service nodes beyond those already documented individually (EMSC, GFZ, INGV).

The beauty of FDSN is the uniform interface: change the base URL, and the same query works everywhere. A generic FDSN bridge adapter is the highest-leverage investment in this domain.

## Nodes Probed — April 2026

| Node | Base URL | Status | Catalog | Notes |
|------|----------|--------|---------|-------|
| **ETHZ (Switzerland)** | `eida.ethz.ch/fdsnws/event/1/` | ✅ Working | SED | Swiss + Alpine; see [ethz-switzerland.md](ethz-switzerland.md) |
| **RESIF (France)** | `ws.resif.fr/fdsnws/event/1/` | ✅ Working | Namazu | France + global M5+; see [resif-france.md](resif-france.md) |
| **IPGP (France)** | `ws.ipgp.fr/fdsnws/event/1/` | ✅ Working | REVOSIMA | Mayotte volcanic swarm monitoring |
| **NIEP (Romania)** | `eida-sc3.infp.ro/fdsnws/event/1/` | ✅ Working | NIEP | Romanian + Vrancea deep seismicity |
| **LMU Munich** | `erde.geophysik.uni-muenchen.de/fdsnws/event/1/` | ✅ Working | LMU | Bavarian seismicity |
| **EMSC** | `seismicportal.eu/fdsnws/event/1/` | ✅ Working | EMSC-RTS | Already documented; global aggregator |
| **GFZ** | `geofon.gfz-potsdam.de/fdsnws/event/1/` | ✅ Working | Already documented |
| **INGV** | `webservices.ingv.it/fdsnws/event/1/` | ✅ Working | Already documented |
| **NOA (Greece)** | `eida.gein.noa.gr/fdsnws/event/1/` | ❌ Timeout | — | Server unresponsive |
| **BGR (Germany)** | `eida.bgr.de/fdsnws/event/1/` | ❌ 404 | — | Event service not available |
| **ORFEUS/ODC** | `orfeus-eu.org/fdsnws/event/1/` | ❌ 404 | — | Waveform-only node |
| **KOERI (Turkey)** | `eida.koeri.boun.edu.tr/fdsnws/event/1/` | ❌ 404 | — | Waveform service only |
| **CSN (Chile)** | `evtdb.csn.uchile.cl/fdsnws/event/1/` | ❌ 404 | — | Endpoint defunct |
| **ISC** | `isc-mirror.iris.washington.edu/fdsnws/event/1/` | ❌ SSL error | — | IRIS retirement issues |

## Key Findings

### Working Nodes (new, not previously documented)

**IPGP/REVOSIMA** deserves special mention. The endpoint at `ws.ipgp.fr` exclusively serves data from the REVOSIMA observatory monitoring the Mayotte volcanic seismic swarm — a submarine volcanic eruption discovered in 2018 that created a new seamount. This is a highly specialized source: every event in the catalog is located near Mayotte (lat -12.8, lon 45.4). It's scientifically fascinating but narrow.

**NIEP Romania** returned data, but the most recent event was from September 2025 — suggesting either very low activity or a stale catalog. Romania's Vrancea seismic zone produces deep (70–200 km) intermediate-depth earthquakes that are geophysically unusual. The data may update in bursts.

**LMU Munich** responded but returned a binary/empty body that couldn't be parsed as text. The endpoint exists but may have encoding or configuration issues.

### Not All EIDA Nodes Serve Events

A critical insight: many EIDA/FDSN nodes only implement the *waveform* service (`fdsnws/dataselect/1/`) and *station* service (`fdsnws/station/1/`), not the *event* service. BGR, ORFEUS, and KOERI all fall into this category. The event service is optional in the FDSN spec, and many nodes leave event catalogs to the major aggregators (EMSC, USGS, ISC).

### The FDSN Adapter Strategy

Given the survey results, the generic FDSN adapter should target these nodes in priority order:

1. **EMSC** — Global aggregator, WebSocket + FDSN (already documented)
2. **GFZ** — Global M4+, reliable FDSN (already documented)
3. **INGV** — Italy, reliable FDSN (already documented)
4. **ETHZ** — Switzerland/Alps, reliable FDSN (new)
5. **RESIF** — France + global teleseismic, reliable FDSN (new)
6. **NIEP** — Romania/Vrancea, intermittent (new)
7. **IPGP** — Mayotte volcanic swarm, specialized (new)

The adapter is configurable: `base_url` + optional `minmagnitude` filter + optional geographic bounding box. That's it.

## Feasibility Rating (for the generic FDSN adapter targeting new nodes)

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | FDSN spec is rock-solid |
| **Data Freshness**           | 2     | Poll-based; minutes latency |
| **Format / Schema Quality**  | 3     | Identical format across all nodes |
| **Auth / Access Simplicity** | 3     | All nodes are anonymous |
| **Coverage Relevance**       | 2     | Adds European depth; most events in aggregators |
| **Operational Reliability**  | 2     | Variable — some nodes are flaky |
| **Total**                    | **15 / 18** | |

## Verdict

The FDSN network is a *configuration exercise*, not a development exercise. Once the generic adapter exists for EMSC/GFZ/INGV, adding ETHZ, RESIF, and NIEP is literally a config change — new base URL, done. The incremental engineering cost is near zero. The incremental data value is moderate (more European detail, lower-magnitude events). Recommend adding ETHZ and RESIF as default FDSN targets alongside the existing three.
