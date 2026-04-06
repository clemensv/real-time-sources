# ECMWF Open Data

**Country/Region**: International (European Centre, global coverage)
**Publisher**: ECMWF (European Centre for Medium-Range Weather Forecasts)
**API Endpoint**: `https://data.ecmwf.int/forecasts/` (direct), also mirrored on AWS, Azure, Google Cloud
**Documentation**: https://github.com/ecmwf/ecmwf-opendata and https://confluence.ecmwf.int/display/DAC/
**Protocol**: HTTPS file download (with Python client library), also available via cloud object storage
**Auth**: None (open access, no registration required)
**Data Format**: GRIB2
**Update Frequency**: 4× daily (00Z, 06Z, 12Z, 18Z model runs), available 7–9 hours after run time
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

ECMWF provides a subset of its operational forecast data as open data:

- **IFS (Integrated Forecasting System)**: The world's leading global weather model at 0.25° (~28 km) resolution. Available parameters include:
  - Single-level: 2m temperature, 10m wind, mean sea level pressure, total precipitation, total cloud cover, significant wave height, and more
  - Pressure-level: Geopotential, temperature, wind, humidity at standard pressure levels

- **AIFS (Artificial Intelligence Forecasting System)**: Machine-learning-based forecasts (single deterministic and ensemble variants).

- **Ensemble forecasts**: Probabilistic forecasts from IFS ensemble (51 members).

- **Extended range**: Up to 10 days for deterministic, 15 days for ensemble.

The `ecmwf-opendata` Python package provides a MARS-like request interface for subsetting and downloading specific parameters and levels.

## API Details

Direct access via HTTPS:
```
https://data.ecmwf.int/forecasts/{date}/{time}/{model}/{resolution}/{step}/
```

Python client usage:
```python
from ecmwf.opendata import Client
client = Client(source="ecmwf")  # or "aws", "azure", "google"
client.retrieve(
    step=24,
    type="fc",
    param=["2t", "msl"],
    target="data.grib2",
)
```

The `Client.latest()` method returns the most recent available forecast run datetime.

Cloud mirrors provide redundancy:
- AWS: `source="aws"`
- Azure: `source="azure"` (generates SAS token)
- Google Cloud: `source="google"`

500 simultaneous connection limit on the ECMWF direct server.

## Freshness Assessment

- Data available 7–9 hours after model run start (so 00Z run available ~07–09Z).
- 4 model runs per day provides regular updates.
- The Python client can automatically find the latest available run.
- Cloud mirrors may have slight additional latency but better bandwidth.

## Entity Model

- **Model run**: Identified by date + time (00/06/12/18)
- **Forecast step**: Hours from run time (0, 3, 6, ..., 240)
- **Parameter**: ECMWF parameter shortnames (2t, msl, tp, etc.)
- **Level**: Single-level or pressure level (1000, 850, 500 hPa, etc.)
- **Stream**: Operational forecast (oper), ensemble forecast (enfo)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 7–9h latency after model run; 4× daily. Good for medium-range, not nowcasting |
| Openness | 3 | No auth required, CC BY 4.0, multi-cloud mirrors |
| Stability | 3 | Intergovernmental organization, long-term commitment |
| Structure | 2 | GRIB2 requires specialized libraries (eccodes); not JSON-friendly |
| Identifiers | 3 | Well-defined MARS vocabulary (param, level, step, type) |
| Additive Value | 3 | The world's most accurate global NWP model — enormous additive value |
| **Total** | **16/18** | |

## Notes

- ECMWF's IFS is widely regarded as the best global weather model. Having free access to a subset is remarkable.
- GRIB2 format requires `cfgrib`, `eccodes`, or similar libraries to decode — not trivial for a simple integration.
- The Python client is well-maintained and simplifies access significantly.
- A full day's data is ~726 GiB, so subsetting is essential.
- The AIFS model represents cutting-edge ML-based weather prediction.
- Cloud mirrors (AWS, Azure, GCP) mean you can access from anywhere without hitting the ECMWF server directly.
- This is model output, not station observations — complementary to station-based services.
