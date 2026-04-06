# EAWS/ALBINA Avalanche Bulletins
**Country/Region**: European Alps (Tirol, South Tyrol, Trentino, Vorarlberg, Salzburg + more)
**Publisher**: EAWS member services via avalanche.report (ALBINA system)
**API Endpoint**: `https://avalanche.report/albina_files/{date}/{date}_{region}_{lang}_CAAMLv6.json`
**Documentation**: https://avalanche.report/ (bulletins), https://www.avalanches.org/ (EAWS standards)
**Protocol**: HTTP file access (static JSON/XML files)
**Auth**: None
**Data Format**: CAAMLv6 JSON and XML (IACS/EAWS standard)
**Update Frequency**: Daily during winter season (typically 2x: evening + morning update)
**License**: CC BY (Creative Commons Attribution)

## What It Provides
The ALBINA system publishes avalanche bulletins in the international CAAMLv6 standard for multiple Alpine regions:
- **Danger ratings** (1-5 European scale) with temporal validity
- **Avalanche problems** (wet snow, wind slab, persistent slab, gliding snow, new snow)
- **Snowpack structure** analysis
- **Avalanche activity** commentary and highlights
- **Tendency** (increasing/decreasing/steady) for next period
- **Danger patterns** (DP1-DP10 Tyrolian classification)
- **Regional breakdown** by named mountain groups with region IDs (AT-07-xx, IT-32-xx)
- **Multilingual**: de, en, it, es, fr, ca, oc (7 languages)
- **Audio bulletins**: MP3 + SSML voice synthesis files

## API Details
- **File listing**: `GET https://avalanche.report/albina_files/` — browsable directory, dates from 2018-12-04 to present
- **Date directory**: `GET https://avalanche.report/albina_files/{date}/` — lists all files for that date
- **CAAMLv6 JSON**: `GET https://avalanche.report/albina_files/{date}/{date}_{region}_{lang}_CAAMLv6.json`
  - Region codes: AT-02 (Salzburg), AT-07 (Tirol), IT-32-BZ (South Tyrol), IT-32-TN (Trentino)
  - Language codes: de, en, it, es, fr, ca, oc
- **CAAMLv6 XML**: Same pattern with `.xml` extension
- **Legacy XML**: `{date}_{region}_{lang}.xml` (non-CAAML)
- **Audio**: `{uuid}_{lang}.mp3` and `.ssml` files
- **Timestamped subdirectories**: `{date}_{HH-MM-SS}/` for intraday updates

## Probe Results
```json
{
  "bulletins": [{
    "publicationTime": "2026-04-06T06:46:10Z",
    "validTime": {
      "startTime": "2026-04-05T15:00:00Z",
      "endTime": "2026-04-06T15:00:00Z"
    },
    "dangerRatings": [{"mainValue": "considerable", "validTimePeriod": "all_day"}],
    "avalancheProblems": [{
      "problemType": "wet_snow",
      "snowpackStability": "very_poor",
      "frequency": "some",
      "avalancheSize": 2,
      "aspects": ["NW","N","SE","E","W","S","NE","SW"]
    }],
    "regions": [
      {"name": "Brandenberg Alps", "regionID": "AT-07-05"},
      {"name": "Kaiser Mountains - Waidring Alps", "regionID": "AT-07-06"}
    ],
    "tendency": [{"tendencyType": "decreasing"}],
    "customData": {"ALBINA": {"mainDate": "2026-04-06"}, "LWD_Tyrol": {"dangerPatterns": ["DP10","DP4"]}}
  }]
}
```

## Freshness Assessment
Excellent (seasonal). During winter season (roughly November through May), bulletins publish daily — typically an evening forecast and a morning update. The file system shows daily entries back to December 2018. Intraday updates appear as timestamped subdirectories. Outside winter season, publication stops.

## Entity Model
- **Bulletin** (bulletinID UUID, publicationTime, validTime, lang, unscheduled flag)
- **DangerRating** (mainValue: low/moderate/considerable/high/very_high, validTimePeriod, elevation)
- **AvalancheProblem** (problemType, elevation, aspects[], snowpackStability, frequency, avalancheSize)
- **Region** (regionID in ISO-like format: AT-07-05, name)
- **Tendency** (tendencyType: increasing/decreasing/steady, highlights, validTime)
- **DangerPattern** (DP1-DP10 codes, Tyrol-specific classification)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily during winter, with intraday updates |
| Openness | 3 | No auth, CC BY license, browsable directory |
| Stability | 3 | Multi-national cooperation (AT/IT), operational since 2018 |
| Structure | 3 | CAAMLv6 international standard, clean JSON |
| Identifiers | 3 | Stable region IDs, UUID bulletin IDs, EAWS standard |
| Additive Value | 3 | Multi-region Alpine avalanche data in standardized format |
| **Total** | **17/18** | |

## Notes
- CAAMLv6 is the official IACS/EAWS international standard for avalanche bulletin exchange
- The ALBINA system is a model of cross-border cooperation (Austria/Italy/Liechtenstein)
- File-based access is simple and reliable — no API rate limits or auth complexity
- Audio bulletins (MP3/SSML) are a unique feature for accessibility
- Region ID format follows ISO 3166-2 pattern — AT-07 is Tirol, IT-32-BZ is South Tyrol
- Historical archive goes back to December 2018
- Pairs with SLF (Switzerland) and NVE (Norway) for broader European coverage
