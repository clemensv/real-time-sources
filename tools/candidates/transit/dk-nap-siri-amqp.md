# Danish NAP — SIRI over AMQP (Movia + Lokaltog)

> **NOT A CONFIG-ADD** · Danish NAP delivers SIRI 2.x over an AMQP 1.0 push subscription, not the poll-based SIRI-Lite the `siri` feeder configures. Needs an AMQP-consumer build.

**Country/Region**: Denmark (national NAP, Sjælland operational coverage)
**Publisher**: Rejsekort & Rejseplan A/S (on behalf of Movia for buses, Movia for Lokaltog regional rail)
**Access Point Operator**: Vejdirektoratet (Danish Road Directorate) — operates the NAP per EU ITS Directive 2010/40/EU + Delegated Regulation 2017/1926 (MMTIS, Retsakt-A)
**Portal Endpoint**: <https://du-portal-ui.dataudveksler.app.vd.dk/> ("Dataudveksleren" — *The Data Exchanger*; the portal `nap.vd.dk` is a permanent redirect)
**Documentation**:
- Catalog page: https://du-portal-ui.dataudveksler.app.vd.dk/data/788/overview (bus) and `/data/799/overview` (Lokaltog)
- AMQP subscription guide: https://vejdirektoratet.atlassian.net/wiki/spaces/DP/pages/3232563240/V+rkt+jer+til+at+udstille+og+modtage+data#Besked-værktøj-(AmqpTool)
- Reference client (AmqpTool, supplied by Vejdirektoratet): same Confluence space
**Protocol**: **SIRI 2.x XML over AMQP** (`GenericAmqpEvent` adapter in the NAP's own dataflow taxonomy)
**Auth**: **MitID Erhverv** (Danish business digital identity) OR **eIDAS-bridged foreign eID** (Bundesdruckerei AusweisApp / BundID for 🇩🇪, ItsMe for 🇧🇪, DigiD for 🇳🇱, etc.). After portal login the user creates a "Servicekonto" (service account, SASL credentials); the password is shown exactly once and cannot be recovered.
**Data Format**: SIRI XML (event-per-message; "A message can contain updates to one or several journeys"). Detailed types in the NAP record:
- `REAL_TIME_ESTIMATED_DEPARTURE_AND_ARRIVAL_TIMES` (ET)
- `DISRUPTIONS_DELAYS_CANCELLATIONS` (SX-style situations)
**Update Frequency**: `ON_OCCURENCE` — pushed live, available from approximately 1 hour before departure through the journey's lifetime
**License**: **CC BY 4.0** — commercial use permitted with attribution. `rightsStatement: Licence-provided`. (CC BY URL: https://creativecommons.org/licenses/by/4.0/)
**Score**: **17/18 if the eID barrier is removable; 11/18 with the barrier**

## What It Provides

The Danish NAP is — as of this survey — **the only publicly accessible SIRI-over-AMQP endpoint in Europe.** Every other European NAP and major operator publishes SIRI over HTTP (REST/SIRI-Lite, SOAP, or callback POST). The CEN/TS 15531 spec defines an AMQP binding; nobody else has actually deployed it as a subscription channel.

Two datasets relevant here:

| Dataset ID | Title | Subscribers as of 2026-05 | Last validated | Coverage |
|---|---|---|---|---|
| **788** | *Realtime data for Movia* | 20 | 2026-05-13 | Movia bus network across Sjælland — entire Greater Copenhagen + regional |
| **799** | *Realtime data for Lokaltog on Zealand* | 9 | 2026-05-17 | Lokaltog A/S regional rail (Hornbæk, Frederiksværk, Gribskov, Hovedstaden, Lille Nord, Nærum, Tølløse-Slagelse lines) |

Both have `dataFlowStatus.status: Online, validationStatus: Validated`. Both are CC BY 4.0. Both share the same publisher (Rejsekort & Rejseplan A/S) and the same dataset owner (Lene Marianne Bergsler, `lbe@rejseplanen.dk`). Both are matched against Plandata in Rejseplanen *before* being submitted to the NAP — meaning the SIRI `LineRef`, `StopPointRef`, `OperatorRef` values are guaranteed to align with the GTFS feed at `rejseplanen.info/labs/GTFS.zip` (which this repo already consumes via the `gtfs` source).

The NAP record explicitly excludes vehicle monitoring (VM); only ET + SX-style situations are exposed.

## API Details

### AMQP subscription model

The portal-provisioned credential is a **service account** (username + one-shot password). The user binds the service account to each dataset they want to subscribe to, and the portal then exposes the AMQP broker URL, queue/topic name, and SASL credentials. Exact broker shape (host, port, AMQP version 0.9.1 vs 1.0, TLS) is not visible in the public catalog — it only becomes visible *after* login and subscription. Strong indications (from the supplied AmqpTool client name and NAPCORE alignment) that this is **AMQP 1.0** over TLS with SASL PLAIN.

The reference client (`AmqpTool`) is provided by Vejdirektoratet and lives in their Confluence wiki under "Værktøjer til at udstille og modtage data". It demonstrates subscribe/receive against the NAP's AMQP broker.

### SIRI message shape (expected, from CEN/TS 15531-2.0 / NAPCORE profile)

```xml
<Siri xmlns="http://www.siri.org.uk/siri" version="2.0">
  <ServiceDelivery>
    <ResponseTimestamp>2026-05-26T12:00:00Z</ResponseTimestamp>
    <ProducerRef>RKRP</ProducerRef>
    <EstimatedTimetableDelivery>
      <EstimatedJourneyVersionFrame>
        <EstimatedVehicleJourney>
          <LineRef>1A</LineRef>
          <OperatorRef>MOVIA</OperatorRef>
          <DatedVehicleJourneyRef>...</DatedVehicleJourneyRef>
          <Cancellation>false</Cancellation>
          <EstimatedCalls>
            <EstimatedCall>...</EstimatedCall>
          </EstimatedCalls>
        </EstimatedVehicleJourney>
      </EstimatedJourneyVersionFrame>
    </EstimatedTimetableDelivery>
  </ServiceDelivery>
</Siri>
```

For SX situations, the body would wrap a `SituationExchangeDelivery` containing `PtSituationElement` records.

### Anonymous catalog discovery (no account required)

The portal's Angular SPA hits two anonymous JSON endpoints — useful for surveying without a Danish identity:

- `POST https://businessservice.dataudveksler.app.vd.dk/api/Search/search-advanced` — anonymous keyword search returning publication metadata
- `GET https://businessservice.dataudveksler.app.vd.dk/api/Dataset/{id}` — full anonymous read of a publication record (publisher, owner email, transport, format, license, validation status)

Per-subscriber distribution URLs (queue names, broker host, credentials) require login.

## Freshness Assessment

Excellent. NAP records show both feeds validated within the past 14 days as of this survey. 20 active subscribers on the bus feed indicates a working production stream consumed by real downstream systems. *"Update to journeys may be found from 1 hour before departure"* — meaning the bus feed will carry updates roughly continuously from ~04:30 UTC through ~01:00 UTC each operating day.

## Entity Model

Two CloudEvent families would be modeled from these feeds:

### Estimated journey (ET)
- **Identity**: `(operator_ref, line_ref, dated_vehicle_journey_ref)` — stable across all updates for the same journey
- **Subject + key template**: `journeys/{operator_ref}/{line_ref}/{dated_vehicle_journey_ref}`
- Contains EstimatedCalls list (one per scheduled stop) with `AimedDepartureTime`, `ExpectedDepartureTime`, `DepartureStatus`

### Situation (SX)
- **Identity**: `(situation_number, version)` — `Version` is incremented when the situation is amended
- **Subject + key template**: `situations/{situation_number}/{version}`
- Contains `Summary`, `Description`, `AffectedLines`, `AffectedStopPoints`, `ValidityPeriod`, `Severity`

## Authentication barrier — the one blocker

The portal supports three IDP options:

| Option | Audience | Practical for non-Danish users |
|---|---|---|
| MitID Erhverv | Danish CVR-registered organizations | **No** — requires Danish business identity |
| Brugerkatalog | Pre-registered Vejdirektoratet user-catalog accounts | **No** — out-of-band provisioning |
| MitID / eID | Danish citizens (MitID) **and** EU/EEA via eIDAS | **Maybe** — depends on cross-border eIDAS interoperability with the user's national scheme. 🇩🇪 Personalausweis-online-ID via AusweisApp/BundID, 🇧🇪 ItsMe, 🇳🇱 DigiD, 🇪🇸 Cl@ve all *should* work in theory; cross-border eIDAS is famously hit-or-miss in practice. |

The Vejdirektoratet IDP is built on Safewhere (a Danish identity broker product) and is configured for eIDAS federation. So the legal/technical path exists. Whether your specific national eID actually completes the federation handshake is a five-minute test, not a multi-month negotiation.

## Repo signal — discovery method (preserved for replay)

This source was discovered via the Trafiklab European pointer page (https://www.trafiklab.se/api/other-apis/public-transport-europe/) which lists `nap.vd.dk` as Denmark's official NAP under the ITS Directive. Direct probing of the portal's Angular SPA captured the anonymous Search and Dataset endpoints documented above. The same workflow applies to any EU NAP built on the "Dataudveksler" / Vejdirektoratet stack — useful prior art for future Nordic surveys.

Catalog records archived at `files/nap-movia-datasets.json` in the session workspace.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Live event push; validated weekly; 20 production subscribers |
| Openness | 1 | CC BY 4.0 license is excellent; **but** the eID barrier costs two points |
| Stability | 3 | EU ITS-Directive mandated; Vejdirektoratet-operated; named publisher contact |
| Structure | 3 | SIRI 2.x XML over AMQP — formal CEN/TS 15531 spec |
| Identifiers | 3 | `OperatorRef`, `LineRef`, `DatedVehicleJourneyRef` — all aligned to Rejseplanen GTFS Plandata before publication |
| Additive Value | 3 | **The only publicly accessible SIRI-over-AMQP endpoint in Europe.** Proves the AMQP binding works at production scale. |
| **Total** | **16/18** | **with eID barrier removable.** Drops to 11/18 if your national eID does not federate via eIDAS to the Danish IDP. |

## Notes

- The portal lists a third related dataset — *"Banedanmark Journeys"* — covering national rail. Worth investigating as a companion if eID access is secured.
- Sister Nordic SIRI source already in the repo: `entur-norway/` consumes Entur's HTTP-SIRI; could reuse the entire XML parser and CloudEvents data model for this source.
- Repo skill match: `amqp-feeder` (transport), `bootstrap-real-time-source` (process). No new tooling required.
- The Danish NAP is built on the same software stack ("Dataudveksleren") that may be reused by other Nordic NAPs in the future — discovery patterns here are portable.

## Verdict

**⚠️ MAYBE — gated on eID interoperability.**

Concrete action: spend five minutes testing the eIDAS handshake from your national eID provider against the Vejdirektoratet IDP. If it works, this becomes a ✅ Build with a 16/18 score. If it fails, fall back to one of the HTTP-SIRI alternatives in the survey deep-dive at `_research-rounds/2026-05-eu-siri-amqp-survey.md` and re-emit AMQP downstream ourselves.

If built: source folder name `dk-nap-siri`. Two messagegroups (ET journeys, SX situations). Three transport variants (Kafka + MQTT + AMQP) per repo convention. Reuse the SIRI parser and data classes from `entur-norway/`.
