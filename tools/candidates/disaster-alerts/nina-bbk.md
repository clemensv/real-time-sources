# NINA / BBK Warn-App (Germany)
**Country/Region**: Germany
**Publisher**: Bundesamt für Bevölkerungsschutz und Katastrophenhilfe (BBK)
**API Endpoint**: `https://warnung.bund.de/api31/{provider}/mapData.json`
**Documentation**: https://nina.api.proxy.bund.de/ (informal)
**Protocol**: REST/JSON (CAP-based structure)
**Auth**: None
**Data Format**: JSON (CAP-aligned)
**Update Frequency**: Real-time (event-driven)
**License**: German government open data

## What It Provides
NINA is Germany's official multi-source emergency warning system, aggregating alerts from six providers into a single API:
- **MoWaS** (Modulares Warnsystem) — civil protection, CBRN, critical infrastructure
- **DWD** (Deutscher Wetterdienst) — severe weather warnings
- **KATWARN** — regional disaster warnings
- **BIWAPP** — municipal warning app
- **LHP** (Länderübergreifendes Hochwasserportal) — flood warnings
- **Police** — police alerts

Each warning follows CAP (Common Alerting Protocol) structure with severity, urgency, category, multilingual titles (de/en/ar/es/fr/pl/ru/tr), and geographic areas.

## API Details
- **Map data per provider**: `GET https://warnung.bund.de/api31/{provider}/mapData.json`
  - Providers: `mowas`, `katwarn`, `biwapp`, `dwd`, `lhp`, `police`
  - Returns array of warning summaries with id, version, startDate, severity, urgency, type, i18nTitle
- **Warning detail**: `GET https://warnung.bund.de/api31/warnings/{warningId}.json`
  - Returns full CAP message: identifier, sender, sent, status, msgType, scope, info[]
  - Info block includes: category, event, severity, urgency, headline, description, area polygons
- **Dashboard** (regional): `GET https://warnung.bund.de/api31/dashboard/{ags}.json`
  - AGS = Amtlicher Gemeindeschlüssel (German municipality code)
- **Severity levels**: Extreme, Severe, Moderate, Minor, Unknown
- **i18n**: Titles available in 8 languages for DWD warnings

## Probe Results
```
mowas: 6 active warnings
katwarn: 0 warnings
biwapp: 0 warnings
dwd: 6 active warnings (storm gusts, weather)
lhp: 0 warnings
police: 0 warnings

Sample warning:
{
  "id": "dwdmap.2.49.0.0.276.0.DWD...",
  "severity": "Moderate",
  "urgency": "Immediate",
  "i18nTitle": {
    "de": "Amtliche WARNUNG vor STURMBÖEN",
    "en": "Official WARNING of GALE-FORCE GUSTS"
  }
}

Detail endpoint returns full CAP:
  identifier, sender, sent, status: "Actual", msgType: "Alert",
  scope: "Public", info[]: category, event, severity, urgency,
  headline, description, area polygons
```

## Freshness Assessment
Excellent. Warnings are published in real-time as events occur. The DWD weather warnings update multiple times daily. MoWaS civil protection alerts are event-driven. The API serves Germany's entire 83-million population through the official NINA app.

## Entity Model
- **Warning** (id, version, startDate, expiresDate, severity, urgency, type, i18nTitle, transKeys)
- **WarningDetail** (CAP structure: identifier, sender, sent, status, msgType, scope, info[])
- **Info** (category, event, severity, urgency, headline, description, area, parameter[])
- **Area** (polygon coordinates, geocode with AGS)
- **Provider** (mowas, dwd, katwarn, biwapp, lhp, police)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time, event-driven |
| Openness | 3 | No auth, public API |
| Stability | 3 | Federal government system, serves 83M people |
| Structure | 3 | Clean JSON, CAP-aligned, multilingual |
| Identifiers | 2 | Warning IDs are unique but complex strings |
| Additive Value | 3 | Germany's only official multi-source warning aggregator |
| **Total** | **17/18** | |

## Notes
- Six warning providers aggregated into one API — a true federation model
- DWD weather warnings include 8-language translations
- CAP-compatible structure enables standards-based integration
- AGS (municipality codes) enable precise geographic targeting
- The NINA app is Germany's most-downloaded emergency app
- KATWARN and BIWAPP data may appear sparse — they fire only during active regional emergencies
