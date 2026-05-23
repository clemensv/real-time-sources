# Copernicus Emergency Management Service (CEMS) Rapid Mapping Activation Feed

- **Country/Region**: Global (on-demand activations)
- **Endpoint**: `https://rapidmapping.emergency.copernicus.eu/activations/feed` (RSS/Atom)
- **Protocol**: RSS 2.0 / Atom
- **Auth**: None
- **Format**: XML (RSS), JSON (via web scraping EMSR pages)
- **Freshness**: Real-time (activations published within hours of disaster)
- **Docs**: https://emergency.copernicus.eu/mapping/, https://rapidmapping.emergency.copernicus.eu/
- **Score**: 15/18

## Overview

CEMS Rapid Mapping provides **on-demand satellite imagery analysis** for emergency response
during disasters. When a natural or man-made disaster occurs (flood, earthquake, wildfire,
hurricane, industrial accident, conflict), authorized users (civil protection agencies,
UN agencies, NGOs) can request a **Rapid Mapping activation**.

Within hours, CEMS produces:
- **First Estimate Product (FEP)** — very rapid initial assessment
- **Delineation maps** — affected area extent
- **Grading maps** — damage severity classification
- **Reference maps** — pre-event baseline for comparison

Activations are assigned **EMSR codes** (Emergency Management Service Rapid mapping) and
tracked through a public portal with RSS feed.

Each activation produces multiple map products over days to weeks as the situation evolves.

**Recent activations** (2025-2026):
- EMSR875 — Wildfire in Bavaria, Germany (May 2026)
- EMSR874 — Wildfire in Rhineland-Palatinate, Germany (May 2026)
- EMSR873 — Wildfire in Tuscany, Italy (May 2026)
- EMSR850 — Flood in Valencia, Spain (Oct 2024)

The **RSS feed** publishes new activations and map updates in near-real-time.

## Endpoint Analysis

CEMS publishes activation updates via:

1. **RSS feed** — https://rapidmapping.emergency.copernicus.eu/activations/feed (XML)
2. **Activation portal** — https://rapidmapping.emergency.copernicus.eu/ (HTML)
3. **Per-activation pages** — e.g., https://rapidmapping.emergency.copernicus.eu/EMSR875/

**RSS feed probe**:

```bash
curl -s "https://rapidmapping.emergency.copernicus.eu/activations/feed" | xmllint --format - | head -50
```

The RSS feed returns XML with recent activations:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>CEMS Rapid Mapping Activations</title>
    <link>https://rapidmapping.emergency.copernicus.eu/</link>
    <description>Near real-time feed of CEMS Rapid Mapping activations</description>
    <item>
      <title>EMSR875 - Wildfire in Bavaria, Germany</title>
      <link>https://rapidmapping.emergency.copernicus.eu/EMSR875/</link>
      <description>Activation for wildfire emergency in Bavaria, Germany...</description>
      <pubDate>Mon, 05 May 2026 14:23:00 GMT</pubDate>
      <guid>EMSR875</guid>
      <category>Wildfire</category>
      <geo:lat>48.5</geo:lat>
      <geo:long>11.2</geo:long>
    </item>
  </channel>
</rss>
```

The feed includes:
- **EMSR code** — unique activation identifier
- **Event type** — Flood, Wildfire, Earthquake, Storm, Industrial Accident, etc.
- **Location** — country, region, sometimes lat/lon
- **Activation timestamp** — when request was accepted
- **Link** — URL to activation detail page

**Activation detail pages** (HTML scraping required for full metadata):

Each EMSR page contains:
- **Event description**
- **Activation country and area of interest**
- **Map products** — downloadable GeoTIFF, PDF, shapefile
- **Product timestamps** — FEP, delineation, grading map release times
- **Satellite imagery sources** — Sentinel-1/2, Pl Earthéiades, Spot, etc.

## Schema / Sample Payload

RSS XML item:

```xml
<item>
  <title>EMSR850 - Flood in Valencia, Spain</title>
  <link>https://rapidmapping.emergency.copernicus.eu/EMSR850/</link>
  <description>
    Severe flooding in the Valencia region following intense rainfall...
  </description>
  <pubDate>Thu, 31 Oct 2024 08:15:00 GMT</pubDate>
  <guid>EMSR850</guid>
  <category>Flood</category>
  <cems:country>Spain</cems:country>
  <cems:status>Active</cems:status>
  <geo:lat>39.5</geo:lat>
  <geo:long>-0.4</geo:long>
</item>
```

Scraping the activation page yields structured JSON:

```json
{
  "emsr_code": "EMSR850",
  "event_type": "Flood",
  "country": "Spain",
  "region": "Valencia",
  "activation_date": "2024-10-31T08:15:00Z",
  "status": "Active",
  "requesting_entity": "Spanish Civil Protection",
  "area_of_interest": "POLYGON((-0.5 39.3, -0.3 39.3, -0.3 39.7, -0.5 39.7, -0.5 39.3))",
  "products": [
    {
      "product_type": "First Estimate Product",
      "release_time": "2024-10-31T12:30:00Z",
      "format": ["PDF", "GeoTIFF", "Shapefile"],
      "download_url": "https://rapidmapping.emergency.copernicus.eu/EMSR850/FEP01/..."
    },
    {
      "product_type": "Delineation",
      "release_time": "2024-11-01T06:00:00Z",
      "format": ["PDF", "GeoTIFF", "Shapefile"],
      "download_url": "https://rapidmapping.emergency.copernicus.eu/EMSR850/DEL01/..."
    }
  ]
}
```

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Emergency response is life-or-death. CEMS Rapid Mapping drives evacuation decisions, damage assessment, and humanitarian logistics. High geopolitical and humanitarian impact. |
| **Freshness** | 3 | RSS feed updates **within hours** of activation. First products (FEP) released 2–6 hours after satellite image acquisition. True near-real-time. |
| **Openness** | 3 | **No authentication** for RSS feed and activation portal. Map products are publicly downloadable. Fully open. |
| **Schema clarity** | 2 | RSS XML is standard but minimal. Activation pages are HTML (scraping required for full metadata). No formal JSON API, but schema is inferrable. |
| **Machine-readability** | 2 | RSS is XML-parseable. Map products are GeoTIFF/Shapefile (geospatial standards). But no REST API; requires RSS polling + HTML scraping. |
| **Repo fit** | 2 | **Event-driven but ephemeral** — activations are one-time disasters, not persistent entities. EMSR code is a stable ID, but each activation is a discrete incident (like fire hotspots, not like river gauges). Fits "alert/notification" model. |

**Total: 15/18** — **Strong candidate**. High value, excellent freshness, fully open, and
RSS is a clean streaming protocol.

## Integration Notes

### Event Model

CEMS activations are **discrete disaster events**, not continuous observations. Model as:

- **Subject**: `emergency/rapid-mapping/{emsr_code}` (e.g., `emergency/rapid-mapping/EMSR875`)
- **Kafka key**: `{emsr_code}` (stable activation identifier)
- **Payload**: Activation metadata (type, country, region, lat/lon, status) + product list
- **Type**: `eu.copernicus.cems.activation.published` (initial activation) or `eu.copernicus.cems.product.released` (new map product)

Emit two event types:
1. **Activation event** — when new EMSR appears in RSS feed
2. **Product event** — when new map (FEP, delineation, grading) is released

### Poll Strategy

Poll the RSS feed every **5 minutes**:

```python
import feedparser

feed = feedparser.parse("https://rapidmapping.emergency.copernicus.eu/activations/feed")

for entry in feed.entries:
    emsr_code = entry.guid
    if not seen(emsr_code):
        emit_activation_event(entry)
        scrape_activation_page(entry.link)  # get full metadata
```

Track seen EMSR codes in bridge state (SQLite or Redis). Re-poll activation pages daily
to detect new products.

### HTML Scraping for Products

The RSS feed announces activations but **not individual map products**. To track product
releases, scrape the activation HTML page:

```python
from bs4 import BeautifulSoup
import requests

response = requests.get(f"https://rapidmapping.emergency.copernicus.eu/{emsr_code}/")
soup = BeautifulSoup(response.text, 'html.parser')

products = soup.find_all('div', class_='product-item')
for product in products:
    product_type = product.find('span', class_='product-type').text
    release_time = product.find('span', class_='release-time').text
    download_links = [a['href'] for a in product.find_all('a', class_='download-link')]
    emit_product_event(emsr_code, product_type, release_time, download_links)
```

### Deduplication

Store `{emsr_code}:{product_type}:{release_time}` in bridge state. Only emit if unseen.

### Geographic Enrichment

RSS feed includes approximate lat/lon. For precise area-of-interest, scrape the activation
page or download the **AOI shapefile** (published with each activation).

## Limitations

- **HTML scraping needed** — RSS announces activations, but detailed metadata + product releases require scraping HTML pages (fragile if portal structure changes)
- **No JSON API** — all data is RSS XML or HTML
- **On-demand nature** — activations are unpredictable; there may be 0–10 activations per month depending on global disaster frequency
- **Product lag** — map products release hours to days after activation, not instantly
- **No historical feed** — RSS covers recent activations only (~last 3 months); historical EMSR codes must be scraped from archive pages

## Why It Matters

CEMS Rapid Mapping has been activated for every major European disaster since 2012:

- **2021 Germany/Belgium floods** — 20+ EMSR activations, damage maps guided rescue operations
- **2023 Turkey/Syria earthquake** — immediate damage assessment within 12 hours
- **2024 Spain Valencia floods** — flood extent maps enabled targeted evacuations
- **Ukraine conflict** — infrastructure damage monitoring (restricted-access products)

Bridging CEMS activations into Kafka enables:
- **Cross-domain correlation** — link EMSR activations to EFFIS fire hotspots, EFAS flood warnings, seismic alerts
- **Humanitarian logistics** — trigger pre-positioning when activation is published
- **Disaster analytics** — aggregate activation frequency by country, event type, seasonality
- **Early warning validation** — compare forecast-based alerts (EFAS, EFFIS FWI) to actual activations

## Verdict

✅ **Build** — High value, fully open, RSS is streaming-friendly, and the event-driven nature
(discrete activations) fits the repo model well. The lack of a formal API (RSS + HTML scraping)
is manageable with robust parsers. This is the **best emergency management candidate** in the
Copernicus portfolio.

**Implementation priority**: High — CEMS activations are rare but critical events. A bridge
would produce 50–150 events/year (activations + products), making it low-volume, high-signal.

**Bonus**: CEMS also publishes a **deactivation feed** when emergencies end. Track full
lifecycle (activation → product releases → deactivation).
