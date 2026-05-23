# GDACS Global Disasters (Qatar Region)

- **Country/Region**: Global (Qatar-relevant subset)
- **Endpoint**: `https://gdacs.org/xml/rss.xml`
- **Protocol**: RSS / XML
- **Auth**: None
- **Format**: RSS 2.0 XML with GeoRSS extensions
- **Freshness**: Multiple updates per day (sub-hourly for major events)
- **Docs**: https://gdacs.org/About/dataproviders.aspx
- **Score**: 13/18

## Overview

The **Global Disaster Alert and Coordination System (GDACS)** is a cooperation framework
between the United Nations and the European Commission to provide real-time alerts about
natural disasters worldwide. GDACS aggregates data from multiple authoritative sources:
- **Earthquakes**: USGS, EMSC, GEOFON
- **Tropical cyclones**: JTWC, NHC, JMA
- **Floods**: Dartmouth Flood Observatory, Copernicus EMS
- **Volcanic eruptions**: Smithsonian GVP, VAAC advisories
- **Tsunamis**: PTWC, JMA, NOAA
- **Droughts**: Global Drought Observatory

For **Qatar**, the most relevant disaster types are:
1. **Tropical cyclones** from the Arabian Sea (rare but impactful — Cyclone Gonu 2007, Shaheen 2021)
2. **Dust storms** (not directly covered by GDACS, but adjacent weather hazards)
3. **Earthquakes** from the Zagros (M6+ felt in Qatar)
4. **Floods** (flash floods from rare heavy rain events — Doha lacks drainage infrastructure)

**GDACS alert levels**:
- **Green**: Minor event (informational)
- **Orange**: Moderate impact expected
- **Red**: Severe humanitarian impact expected

Each alert includes:
- Event type and magnitude/intensity
- Geographic extent (bounding box, affected countries)
- Population exposure estimate
- Humanitarian impact score
- Links to detailed reports and maps

## Endpoint Analysis

**Live test confirmed** — RSS feed is operational:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:gdacs="http://www.gdacs.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:georss="http://www.georss.org/georss">
  <channel>
    <title>GDACS - Global Disaster Alert and Coordination System</title>
    <link>https://gdacs.org</link>
    <description>GDACS provides real-time alerts about natural disasters around the world</description>
    <item>
      <title>Green cyclone alert MAHINA-25 in Seychelles, Mauritius, Reunion, Madagascar</title>
      <link>https://gdacs.org/report.aspx?eventtype=TC&amp;eventid=1048582</link>
      <description>Green tropical cyclone alert. Tropical cyclone wind speeds of 111 km/h are expected. Population affected by category 1 (120-153 km/h) wind speeds or higher is 0.</description>
      <pubDate>Thu, 22 May 2025 14:23:00 GMT</pubDate>
      <guid>https://gdacs.org/report.aspx?eventtype=TC&amp;eventid=1048582</guid>
      <gdacs:eventtype>TC</gdacs:eventtype>
      <gdacs:alertlevel>Green</gdacs:alertlevel>
      <gdacs:eventid>1048582</gdacs:eventid>
      <gdacs:episodeid>1048582</gdacs:episodeid>
      <gdacs:calculatedexpiry>2025-05-29T00:00:00Z</gdacs:calculatedexpiry>
      <gdacs:severity unit="kph">111</gdacs:severity>
      <gdacs:population unit="number">0</gdacs:population>
      <gdacs:country>MDG</gdacs:country>
      <gdacs:country>MUS</gdacs:country>
      <gdacs:country>REU</gdacs:country>
      <gdacs:country>SYC</gdacs:country>
      <geo:Point>
        <geo:lat>-14.2</geo:lat>
        <geo:long>55.8</geo:long>
      </geo:Point>
      <georss:polygon>-12.0 53.0 -12.0 58.0 -16.0 58.0 -16.0 53.0 -12.0 53.0</georss:polygon>
    </item>
  </channel>
</rss>
```

**Key RSS extensions**:
- `gdacs:eventtype`: TC (tropical cyclone), EQ (earthquake), FL (flood), VO (volcano), TS (tsunami), DR (drought)
- `gdacs:alertlevel`: Green, Orange, Red
- `gdacs:eventid`: Unique event identifier
- `gdacs:severity`: Magnitude or wind speed (units vary by event type)
- `gdacs:population`: Estimated population affected
- `gdacs:country`: ISO 3166-1 alpha-3 country codes (e.g., QAT for Qatar)
- `georss:polygon`: Bounding box of affected area (lat/lon pairs)
- `geo:Point`: Event epicenter or cyclone position

**Filtering by country**: The feed is global. To extract Qatar-specific events, filter on:
```xml
<gdacs:country>QAT</gdacs:country>
```

Or filter by bounding box (22-27°N, 50-52°E for Qatar).

**Event types relevant to Qatar**:
- **TC** (Tropical Cyclone): Arabian Sea cyclones occasionally bring high winds and heavy rain to Qatar (Cyclone Gonu 2007 caused widespread flooding in Oman and impacts in Qatar; Cyclone Shaheen 2021 passed south of Qatar but affected Oman/UAE)
- **EQ** (Earthquake): Zagros M6+ events may trigger alerts if population exposure in Qatar is significant
- **FL** (Flood): Rare but possible — Doha's poor drainage means even 20-30mm rainfall can cause flash floods
- **DR** (Drought): Qatar is arid by default, but extreme heat waves could trigger alerts

**Alternative format**: GDACS also provides JSON/GeoJSON at `https://www.gdacs.org/gdacsapi/api/events/geteventlist/MAP` but RSS is the documented primary feed.

## Integration Notes

- **Polling interval**: 30 minutes (events are added as disasters develop)
- **CloudEvents subject**: `disaster/{eventtype}/{eventid}` → `disaster/TC/1048582`
- **Kafka key**: `eventid` (unique per disaster)
- **Entity model**: Disaster event (point or polygon + severity + affected countries)
- **Overlap check**: The repo does not currently have a multi-hazard disaster alert bridge.
  Individual hazard bridges exist (usgs-earthquake for EQ, potentially others), but GDACS
  provides **cross-hazard aggregation** plus humanitarian impact assessment (population
  exposure, severity levels).
- **Additive value**: GDACS adds value by:
  1. Aggregating multiple disaster types in one feed
  2. Providing humanitarian impact scores (population affected, alert level)
  3. Country-level filtering (easier to extract Qatar-relevant events)
  4. Historical context (links to detailed reports and maps)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Multiple updates per day (not real-time like USGS, but sub-daily) |
| Openness | 3 | No auth, RSS feed, public |
| Stability | 3 | UN/EC operational system, RSS 2.0 standard |
| Structure | 2 | XML/RSS with GeoRSS extensions (one level below JSON/GeoJSON) |
| Identifiers | 2 | Event IDs are unique but not as stable as USGS (multi-source aggregation) |
| Additive value | 1 | Overlaps existing earthquake bridge; cyclone/flood data is new |

**Verdict**: **Marginal candidate** due to overlap with existing seismicity bridges and
relatively low disaster frequency for Qatar. However, GDACS fills a gap for **tropical
cyclones** (Arabian Sea) and **multi-hazard situational awareness**. Recommend as a
**low-priority** candidate or defer until the repo adds cyclone/flood domain coverage.

**Qatar-specific use cases**:
- **Arabian Sea cyclone early warning**: When a cyclone forms in the Arabian Sea and tracks
  toward the Persian Gulf, GDACS issues alerts days in advance. This is valuable for:
  - Offshore oil/gas platform evacuations
  - LNG tanker route planning (Ras Laffan port)
  - Event cancellations (outdoor sports, concerts at FIFA-legacy stadiums)
  - Public preparedness (rare events, population not accustomed to cyclone impacts)
- **Flash flood alerts**: When rare heavy rain is forecast for Doha, GDACS may issue flood
  alerts if population exposure is high. This complements weather forecasts with impact
  assessment.
- **Regional awareness**: Even if Qatar is not directly affected, GDACS alerts for neighboring
  countries (Oman cyclone, Iran earthquake, Saudi flood) are relevant for supply chain
  disruptions and regional coordination.

**Historical context**:
- **Cyclone Gonu (2007)**: Category 5 cyclone in Arabian Sea, made landfall in Oman,
  caused 50+ deaths and $4B damage. Qatar experienced high winds and heavy rain (unusual for June).
- **Cyclone Shaheen (2021)**: Category 1 cyclone, made landfall in Oman, passed south of Qatar.
  No significant impact in Qatar but affected regional shipping.
- **Doha flash floods (2015)**: 80mm rainfall in 24 hours (Qatar's annual avg is <80mm),
  caused widespread flooding in Doha due to inadequate drainage. No GDACS alert (flood was
  short-duration, low population exposure), but highlights vulnerability.

**Integration with other Qatar sources**:
- Combine GDACS cyclone alerts with:
  - Open-Meteo wind speed forecasts (km/h)
  - Open-Meteo precipitation forecasts (mm)
  - Open-Meteo wave height (Persian Gulf marine conditions)
  - Aviation SIGMETs (tropical cyclone SIGMETs for Qatar FIR)
- Combine GDACS earthquake alerts with:
  - USGS/EMSC real-time seismic data (detailed magnitude, depth, location)
  - Social media felt reports
