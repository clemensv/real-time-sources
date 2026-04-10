# Luxembourg CITA DATEX II Traffic Feeds

**Country/Region**: Luxembourg
**Publisher**: CITA Luxembourg
**API Endpoint**: `https://www.cita.lu/info_trafic/datex/`
**Documentation**: `https://www.cita.lu/`
**Protocol**: DATEX II XML
**Auth**: None
**Data Format**: XML
**Update Frequency**: Minute-scale publication of current measured traffic values
**License**: Public feed; exact license text not verified in this pass

## What It Provides

CITA publishes open DATEX II traffic feeds for several Luxembourg motorway corridors.
The feeds contain measured traffic data rather than static road metadata, which makes
them immediately relevant for the repo's traffic category and for DATEX parser reuse.

This is the kind of European source that pays off twice. First, it gives direct
Luxembourg coverage. Second, it exercises the same DATEX family already relevant for
NDW Netherlands, French road traffic, and other national traffic publishers.

## API Details

### Confirmed traffic feeds

- `https://www.cita.lu/info_trafic/datex/trafficstatus_a1`
- `https://www.cita.lu/info_trafic/datex/trafficstatus_a3`
- `https://www.cita.lu/info_trafic/datex/trafficstatus_a4`
- `https://www.cita.lu/info_trafic/datex/trafficstatus_a6`
- `https://www.cita.lu/info_trafic/datex/trafficstatus_a7`
- `https://www.cita.lu/info_trafic/datex/trafficstatus_a13`
- `https://www.cita.lu/info_trafic/datex/trafficstatus_b40`

### Sample payload shape

The `trafficstatus_a6` feed returned a DATEX II `MeasuredDataPublication` with:

- `publicationTime`: `2026-04-08T13:05:09...+02:00`
- `measurementTimeDefault`: `2026-04-08T13:04:00+02:00`
- `measurementSiteReference`: `A6.WG.2178`
- `measurementEquipmentTypeUsed`: `induction loop`
- `basicData xsi:type="TrafficSpeed"`
- `locationForDisplay`: latitude / longitude
- Alert-C linear location references

The sampled A6 feed contained **36** `siteMeasurements`.

## Freshness Assessment

Confirmed live on 2026-04-08. The publication timestamp and default measurement time
were within a minute of one another, and the payload clearly carried current measured
traffic values. This is a genuine real-time traffic feed, not a static catalog entry.

## Entity Model

- **Feed** - per-road DATEX stream (`a1`, `a3`, `a4`, `a6`, `a7`, `a13`, `b40`)
- **Measurement Site** - site reference such as `A6.WG.2178`
- **Measured Value** - traffic speed and related measured traffic data
- **Location Reference** - coordinates plus Alert-C linear references

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Current measured data with minute-scale timestamps |
| Openness | 3 | No auth |
| Stability | 3 | National traffic operator feed |
| Structure | 3 | Standard DATEX II measured-data publication |
| Identifiers | 2 | Stable site references present; fuller site-table mapping still to inspect |
| Additive Value | 3 | Luxembourg coverage plus strong DATEX reuse value |
| **Total** | **17/18** | |

## Notes

- `data.europa.eu` was useful here because SPARQL expanded a single catalog record into
  the full set of per-road feed URLs.
- There is also a Luxembourg parking DATEX feed, but the traffic feeds are the clearer
  first bridge target.
- This is a good parser-validation source because it is smaller and easier to reason
  about than some of the larger national DATEX estates.
