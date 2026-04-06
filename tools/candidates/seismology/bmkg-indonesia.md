# BMKG Indonesia — Earthquake Data API

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Badan Meteorologi, Klimatologi, dan Geofisika (BMKG) |
| **Operator**     | Indonesian Agency for Meteorology, Climatology, and Geophysics |
| **URL**          | https://www.bmkg.go.id/ |
| **API Base**     | `https://data.bmkg.go.id/DataMKG/TEWS/` |
| **Coverage**     | Indonesia and surrounding region |
| **Update Freq.** | Near-real-time; latest felt earthquake updated within minutes |

## What It Does

Indonesia is arguably the most seismically active country on Earth — sitting atop the Pacific Ring of Fire where the Indo-Australian, Eurasian, and Philippine Sea plates collide. BMKG operates Indonesia's earthquake and tsunami early warning system. Their open data API provides JSON feeds for the latest earthquake, recent significant quakes, and felt reports.

This is the authoritative source for Indonesian seismicity. The 2004 Boxing Day tsunami, 2018 Palu earthquake-tsunami, and countless other major events originate in this region. Having BMKG data is not optional for a comprehensive global seismic picture.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/autogempa.json` | ✅ 200 | Latest earthquake (auto-detected) |
| `/gempaterkini.json` | ✅ 200 | Recent significant earthquakes (M5+) |
| `/gempadirasakan.json` | ✅ Documented | Felt earthquakes |

### Sample Response — `/autogempa.json`

```json
{
  "Infogempa": {
    "gempa": {
      "Tanggal": "06 Apr 2026",
      "Jam": "08:56:46 WIB",
      "DateTime": "2026-04-06T01:56:46+00:00",
      "Coordinates": "1.42,126.40",
      "Lintang": "1.42 LU",
      "Bujur": "126.40 BT",
      "Magnitude": "4.0",
      "Kedalaman": "21 km",
      "Wilayah": "Pusat gempa berada di laut 126 km barat Jailolo",
      "Potensi": "Gempa ini dirasakan untuk diteruskan pada masyarakat",
      "Dirasakan": "II - III Batang Dua",
      "Shakemap": "20260406085646.mmi.jpg"
    }
  }
}
```

### Sample Response — `/gempaterkini.json` (array, trimmed)

```json
{
  "Infogempa": {
    "gempa": [
      {
        "DateTime": "2026-04-04T11:21:11+00:00",
        "Coordinates": "-2.05,100.05",
        "Magnitude": "5.7",
        "Kedalaman": "11 km",
        "Wilayah": "51 km Tenggara TUAPEJAT-SUMBAR",
        "Potensi": "Tidak berpotensi tsunami"
      }
    ]
  }
}
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not documented; public data service.
- **License**: Indonesian government open data. Attribution to BMKG expected.

## Integration Notes

The JSON is clean but uses Indonesian-language field names: `Tanggal` (date), `Jam` (time), `Kedalaman` (depth), `Wilayah` (region), `Potensi` (potential — tsunami risk), `Dirasakan` (felt). The `DateTime` field is ISO 8601 with timezone offset — reliable for parsing. `Coordinates` is a comma-separated lat,lon string that needs splitting.

The `autogempa.json` endpoint returns a single object (latest quake), while `gempaterkini.json` returns an array of recent significant events. The `Potensi` field gives tsunami potential assessment — unique and operationally valuable data not available from global aggregators.

ShakeMap images are available at `https://data.bmkg.go.id/DataMKG/TEWS/{Shakemap}`.

Deduplication: BMKG events appear in EMSC (contributor "BMKG") and USGS, but the local detail — felt reports, tsunami potential, Indonesian locality descriptions — is unique.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | Working JSON; minimal documentation |
| **Data Freshness**           | 3     | Near-real-time; auto-detected events within minutes |
| **Format / Schema Quality**  | 2     | Clean JSON but Indonesian field names; string parsing needed |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 3     | One of the most seismically active regions on Earth |
| **Operational Reliability**  | 3     | National agency; critical infrastructure |
| **Total**                    | **16 / 18** | |

## Verdict

✅ **Build** — Indonesia generates more earthquakes than almost any other country. BMKG's JSON API works, returns real-time data, and includes unique fields (tsunami potential, felt intensity descriptions) not available through global aggregators. The Indonesian field names need a mapping layer, but the data quality justifies it. Essential for Ring of Fire coverage.
