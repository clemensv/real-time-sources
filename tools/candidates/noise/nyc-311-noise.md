# NYC 311 Noise Complaints (Socrata/Open Data)
**Country/Region**: New York City, USA
**Publisher**: NYC Department of Environmental Protection / NYC Open Data
**API Endpoint**: `https://data.cityofnewyork.us/resource/fhrw-4uyv.json`
**Documentation**: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
**Protocol**: REST (Socrata SODA 2.0)
**Auth**: None required (app token recommended for higher rate limits)
**Data Format**: JSON (also CSV, GeoJSON)
**Update Frequency**: Near real-time (complaints appear within minutes)
**License**: NYC Open Data Terms of Use (public domain equivalent)

## What It Provides
NYC's 311 system receives and tracks noise complaints from all five boroughs. The Socrata API exposes:
- **Complaint types**: Noise - Residential, Noise - Street/Sidewalk, Noise - Commercial, Noise - Vehicle, Noise - Park, Noise - Helicopter, Collection Truck Noise
- **Descriptors**: Loud Music/Party, Loud Talking, Banging/Pounding, Barking Dog, Car/Truck Horn, Ice Cream Truck, Jack Hammering, Air Condition/Ventilation Equipment, Construction Before/After Hours
- **Geographic data**: Incident address, borough, zip code, latitude/longitude, community board
- **Status tracking**: Open, In Progress, Closed, with resolution timestamps
- **Temporal data**: Created date, closed date, due date, resolution action
- **Agency routing**: DEP, NYPD, DOB, DOT depending on complaint type

## API Details
- **Base endpoint**: `GET https://data.cityofnewyork.us/resource/fhrw-4uyv.json`
- **Noise filter**: `$where=complaint_type like '%25Noise%25'`
- **Latest complaints**: `$order=created_date DESC`
- **Field selection**: `$select=unique_key,created_date,complaint_type,descriptor,incident_address,city,borough,latitude,longitude,status`
- **Pagination**: `$limit=N&$offset=N`
- **SoQL query language**: Full SQL-like filtering, aggregation, grouping
- **Formats**: `.json`, `.csv`, `.geojson`
- **Rate limits**: 1000 requests/hour without app token, higher with free token

## Probe Results
```json
[
  {
    "unique_key": "68560134",
    "created_date": "2026-04-05T02:05:52",
    "complaint_type": "Noise - Residential",
    "descriptor": "Loud Music/Party",
    "incident_address": "117-31 202 STREET",
    "city": "SAINT ALBANS",
    "borough": "QUEENS",
    "latitude": "40.694704251612855",
    "longitude": "-73.74981471209315",
    "status": "In Progress"
  }
]
```

## Freshness Assessment
Excellent. Complaints appear in the API within minutes of being filed. The dataset contains records from 2010 to present. During peak hours (weekend nights), hundreds of noise complaints flow in per hour. The Last-Modified header confirmed data current to the probe date.

## Entity Model
- **ServiceRequest** (unique_key, created_date, closed_date, agency, agency_name)
- **Complaint** (complaint_type, descriptor, resolution_description, resolution_action_updated_date)
- **Location** (incident_address, street_name, cross_street_1/2, city, borough, zip, latitude, longitude)
- **Geographic** (community_board, borough_boundaries, city_council_district, police_precinct)
- **Status** (status: Open/In Progress/Closed, due_date)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Near real-time, minutes-fresh |
| Openness | 3 | No auth required, public domain |
| Stability | 3 | NYC Open Data, running since 2010 |
| Structure | 3 | Clean JSON, SoQL queries, multiple formats |
| Identifiers | 3 | Stable unique_key per complaint |
| Additive Value | 3 | Only real-time urban noise complaint stream at this scale |
| **Total** | **18/18** | |

## Notes
- Perfect score — this is an exemplary open data API
- Socrata SODA 2.0 platform provides excellent developer experience
- SoQL enables complex queries: time windows, geographic bounds, aggregations
- GeoJSON output format enables direct map visualization
- 15+ years of historical data enables trend analysis
- Noise complaints serve as a proxy for urban noise levels — crowdsourced ambient monitoring
- Consider pairing with actual sensor data (Dublin Sonitus, Schiphol NOMOS) for calibration
- App tokens are free and increase rate limits significantly
