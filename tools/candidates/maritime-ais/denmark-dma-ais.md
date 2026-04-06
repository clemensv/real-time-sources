# Denmark DMA AIS (Investigation Report)

**Country/Region**: Denmark
**Publisher**: Danish Maritime Authority (DMA) / Danish Emergency Management Agency (DEMA)
**API Endpoint**: Not found — no public API endpoint discovered
**Documentation**: https://dma.dk/safety-at-sea/navigational-information/ais-data
**Protocol**: Unknown (VTExchange.dk referenced but unreachable)
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time shore-based AIS system exists
**License**: Unknown

## What It Provides

Denmark operates a comprehensive shore-based AIS system covering Danish waters. The Danish
Maritime Authority (DMA) has historically provided AIS data and maintains shore-based AIS
stations along the Danish coastline.

According to DMA's public documentation, the system provides:
- Real-time vessel traffic picture in Danish waters
- Position, course, speed, identity of AIS-equipped vessels
- Historical AIS data for accident reconstruction and traffic analysis

**Important change**: The DMA website states that "The Danish Land Based AIS-system is now under
the jurisdiction of the Danish Emergency Management Agency." This institutional transfer may
explain why the traditional access points are no longer reachable.

## API Details

### What was investigated:

| URL | Status |
|---|---|
| `https://dma.dk/safety-at-sea/navigational-information/ais-data` | ✅ Page exists (info only) |
| `https://dma.dk/.../access-to-ais-data` | ❌ 404 |
| `https://dma.dk/.../access-to-the-danish-ais-data` | ❌ 404 |
| `https://dma.dk/.../distribution-of-data-from-the-danish-ais` | ❌ 404 |
| `https://ais.dma.dk/` | ❌ Connection failed |
| `https://data.dma.dk/` | ❌ Connection failed |
| `https://havfruen.dma.dk/` | ❌ Connection failed |
| `https://api.vtexchange.dk/` | ❌ Connection failed |
| `https://www.vtexchange.dk/` | ❌ Connection failed |

VTExchange.dk was historically a Danish AIS data exchange service, but appears to be offline
or restricted. The `havfruen.dma.dk` domain (named after a famous Danish mermaid statue) was
a known AIS visualization portal but is not responding.

### Historical context:

Denmark has been known to provide AIS data through various programs, including academic research
data from ITU Copenhagen (aisdk) and through HELCOM for Baltic Sea monitoring. However, no
currently accessible public API endpoint was found during this investigation.

## Freshness Assessment

Cannot be assessed — no working endpoint found. The shore-based AIS infrastructure exists and
provides real-time data operationally, but public programmatic access was not discoverable.

## Entity Model

Unknown — no response data obtained.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | ? | System is real-time, but no access to verify |
| Openness | 0 | No discoverable public API |
| Stability | ? | Government infrastructure exists |
| Structure | ? | Unknown |
| Identifiers | ? | Standard AIS identifiers expected |
| Additive Value | 2 | Danish waters coverage would complement Nordic set |

**Total: 2/18 (incomplete — further investigation needed)**

## Notes

- This is an **investigation report**, not a confirmed candidate. The Danish AIS system exists
  but no public API was found.
- The transfer from DMA to the Danish Emergency Management Agency (Beredskabsstyrelsen) may
  have disrupted public access. DEMA may have different data sharing policies.
- Recommended next steps:
  1. Contact DMA directly (dma@dma.dk) to ask about current AIS data access
  2. Check DEMA (brs.dk) for any data portals
  3. Investigate HELCOM AIS data sharing for Baltic regional access
  4. Check if Denmark participates in SafeSeaNet or other EU maritime data sharing
- Denmark's AIS data, if accessible, would fill a gap between Norway (kystverket/barentswatch)
  and Finland (digitraffic) for complete Nordic AIS coverage.
- The Finnish Digitraffic Maritime REST API already covers Danish-flagged vessels transiting
  the Baltic, providing partial coverage of Danish waters.
