# NOAA VIIRS Nightfire - Iraq Gas Flaring

- **Country/Region**: Global (Iraq is #2 worldwide for gas flaring after Russia)
- **Endpoint**: `https://eogdata.mines.edu/wwwdata/viirs_products/vnf/` (requires auth)
- **Protocol**: HTTP file server (CSV downloads)
- **Auth**: Required (OpenID Connect, free registration)
- **Format**: CSV
- **Freshness**: Daily (one global file per day)
- **Docs**: https://eogdata.mines.edu/products/vnf/
- **Score**: 11/18

## Overview

Iraq is the **world's second-largest gas flarer** after Russia. The country burns an estimated 18 billion cubic meters of natural gas per year — gas that is produced alongside oil extraction but not captured due to lack of gas processing infrastructure.

Gas flaring in Iraq:
- Concentrated in southern oil fields (Basra, Rumaila, West Qurna, Majnoon)
- Also present in northern Kurdistan oil fields (Kirkuk region)
- Visible from space as persistent thermal hotspots
- Major contributor to Iraq's greenhouse gas emissions
- Represents massive economic waste (billions of dollars of gas burned)
- Local air quality impact around oil fields

The NOAA Visible Infrared Imaging Radiometer Suite (VIIRS) Nightfire product detects combustion sources globally using satellite thermal infrared bands. It distinguishes gas flares from wildfires by persistence (flares burn continuously, fires are transient).

This is the **only near-real-time data source** for Iraq's gas flaring activity.

## Endpoint Analysis

**VIIRS Nightfire data verified but requires authentication** — the Colorado School of Mines Earth Observation Group recently added OpenID Connect authentication to downloads.

Data structure:
- **Daily global CSV files** at `https://eogdata.mines.edu/wwwdata/viirs_products/vnf/v30_all_countries/`
- File naming: `VNF_npp_dYYYYMMDD_noaa_v30-ez.csv.gz`
- Each file contains all global detections for that day (typically 5,000-10,000 detections worldwide)
- Iraq detections can be filtered by lat/lon bounding box (approx 29-38°N, 38-49°E)

File format (CSV columns):
```
ID_KEY,Lat_GMTCO,Lon_GMTCO,Temp_BB,RH,DateTime,QF_Sat,DN_Sat,...
```

Key fields:
- `ID_KEY` — unique detection ID (string)
- `Lat_GMTCO`, `Lon_GMTCO` — coordinates of detection
- `Temp_BB` — blackbody temperature (K)
- `RH` — radiant heat (MW)
- `DateTime` — ISO 8601 timestamp
- Flare vs fire classification (persistent detections at known oil field locations = flares)

## Integration Notes

- **Registration required**: Free account at https://eogauth.mines.edu/ (OpenID provider)
- **Daily cadence**: New file appears each day for previous day's detections
- **Polling pattern**: Download daily file, filter for Iraq bounding box, emit detections
- **Flare identification**: Iraq oil fields have ~100-200 persistent flare locations. Build a reference list of known flare coordinates and flag detections within 1km as flares vs transient fires.
- **Kafka key challenge**: Detections are point events with coordinates but no stable facility ID. Options:
  - Use `ID_KEY` (unique per detection, but changes daily for same flare)
  - Use grid cell ID (snap coordinates to 0.01° grid)
  - Use nearest known oil field + flare index
- **Volume**: Iraq typically has 50-150 detections per day (mix of persistent flares and occasional agricultural fires or waste burning)
- **Alternative sources**: 
  - **CAMS Global Fire Assimilation System (GFAS)** — similar satellite fire data, but VIIRS is more specialized for flares
  - **World Bank GGFR** — Global Gas Flaring Reduction partnership publishes annual statistics, but not real-time

## Significance for Iraq

Gas flaring data is **politically and economically significant**:
- Iraq's government has committed to reducing flaring under international agreements
- Oil companies (IOCs and state-owned) are under pressure to capture gas
- Local communities near Basra oil fields have protested air quality impacts
- Real-time flaring data could track compliance and detect changes in flaring intensity

This is a **frontier data source** — very few organizations track oil field flaring in near-real-time at the individual flare level.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily (one file per day, previous day's data) |
| Openness | 1 | Free registration but auth required |
| Stability | 3 | NOAA operational product, versioned (v30) |
| Structure | 2 | CSV, documented columns |
| Identifiers | 1 | Detection IDs change daily; no stable flare facility IDs |
| Richness | 2 | Coordinates, temperature, radiant heat, timestamp |

**Verdict**: ✅ **Promising candidate** — Iraq is the world's #2 gas flarer. VIIRS Nightfire is the only near-real-time satellite-based flare monitoring. Daily cadence is acceptable for tracking flaring trends. **Registration required is a friction point** (not ideal for open data bridge) but the data is free and the use case is compelling. The **lack of stable facility identifiers** makes Kafka keying awkward (would need to assign grid cells or build a flare location registry). Worth deeper investigation — if stable flare locations can be established, this would be a **unique high-value source** for Iraq environmental and energy monitoring.
