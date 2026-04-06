# GIRO — Global Ionospheric Radio Observatory

**Country/Region**: Global (ionosonde stations worldwide)
**Publisher**: University of Massachusetts Lowell / GIRO consortium
**API Endpoint**: `https://lgdc.uml.edu/common/DIDBGetValues`
**Documentation**: https://giro.uml.edu/didbase/
**Protocol**: REST (text/CSV), SAO Explorer (Java app)
**Auth**: None
**Data Format**: Text/CSV (GIRO header + tabular data), SAO format (ionograms)
**Update Frequency**: 5-15 minutes (ionosonde sounding cadence)
**License**: Open for scientific use; citation requested

## What It Provides

GIRO is a global network of ionosondes — ground-based radar instruments that send radio pulses straight up and measure the reflection from ionospheric layers. Each sounding produces a profile of electron density vs. altitude, yielding critical parameters: foF2 (critical frequency of the F2 layer), hmF2 (height of the F2 peak), MUF(3000)F2 (maximum usable frequency for a 3000km path), and others.

These parameters directly determine HF radio propagation conditions. foF2 tells you the highest frequency that will be reflected by the ionosphere overhead — anything above it punches through into space. This is the ground truth for ionospheric modeling.

## API Details

- **Get values**: `GET /common/DIDBGetValues?ursiCode={station}&charName={param}&fromDate={YYYY.MM.DD}&toDate={YYYY.MM.DD}`
- **Parameters**: `foF2`, `hmF2`, `foF1`, `foE`, `MUF(3000)F2`, `TEC` (Total Electron Content)
- **Station codes**: URSI codes (e.g., `JR055` for Juliusruh, `BC840` for Boulder)
- **Station list**: Available via GIRO DIDBase station map
- **SAO Explorer**: Java application for detailed ionogram analysis
- **No auth required**: Public data access
- **Response format**: Text with GIRO header, comment lines (starting `#`), then CSV data

## Freshness Assessment

Ionosondes typically sound every 5-15 minutes. Data appears in DIDBase shortly after processing (minutes to hours depending on station and processing pipeline). Some stations have near-real-time pipelines; others batch-process with longer delay.

API confirmed responsive: returns proper GIRO headers and error messages for empty date ranges. Historical data retrieval works; real-time availability varies by station.

## Entity Model

- **Station**: URSI code, geographic coordinates, instrument type
- **Ionospheric parameter**: `charName` (e.g., foF2), value (MHz for frequencies, km for heights), confidence score
- **Sounding**: Timestamp (UTC), station, set of derived parameters
- **Ionogram**: Full frequency-height profile (available via SAO Explorer)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 5-15 min sounding cadence; processing adds variable delay |
| Openness | 3 | No auth, public API |
| Stability | 2 | Academic infrastructure; station availability varies |
| Structure | 2 | Text/CSV format with headers; not JSON |
| Identifiers | 3 | URSI station codes, parameter names, timestamps |
| Additive Value | 3 | Direct ionospheric measurements — ground truth for propagation models |
| **Total** | **15/18** | |

## Notes

- Confirmed: API returns proper GIRO formatted responses with station metadata.
- The text/CSV format requires custom parsing but is well-documented and consistent.
- Station coverage is global but uneven — denser in Europe, North America, and East Asia.
- foF2 is the single most important parameter for HF propagation prediction.
- Real-time data availability depends on individual station pipelines — some are near-real-time, others have hours of delay.
- GIRO data is the empirical basis for ionospheric models like IRI (International Reference Ionosphere).
- Pairs with DSCOVR (solar wind drives ionospheric changes), PSKReporter/RBN (observed propagation vs. predicted from foF2), and SWPC data.
