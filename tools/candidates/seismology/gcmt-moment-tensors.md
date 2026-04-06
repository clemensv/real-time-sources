# Global CMT — Centroid Moment Tensor Catalog

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Global Centroid-Moment-Tensor (CMT) Project |
| **Operator**     | Lamont-Doherty Earth Observatory, Columbia University |
| **URL**          | https://www.globalcmt.org/ |
| **Catalog URL**  | `https://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/` |
| **Coverage**     | Global, M5+ (roughly) |
| **Update Freq.** | Monthly catalog updates; several months delay |

## What It Does

The Global CMT catalog is the definitive source for earthquake moment tensor solutions — the mathematical description of the forces that caused an earthquake. Since 1976, the project has determined source parameters for over 60,000 earthquakes. Every significant earthquake on Earth gets a CMT solution eventually.

Moment tensors tell you *how* a fault ruptured — not just where and when, but the orientation of the fault plane, the slip direction, and the seismic moment (a more physically meaningful measure than magnitude). This is reference-grade scientific data, not real-time monitoring.

## Data Access

| Method | Status | Notes |
|--------|--------|-------|
| NDK catalog file | ✅ 200 | 22 MB bulk download; 1976–2020 |
| Web search form | ✅ 200 | CGI-based search; HTML output |
| Monthly NDK files | ✅ Documented | `catalog/NEW_MONTHLY/` directory |
| Quick CMT (near-real-time) | ✅ Documented | Preliminary solutions within hours |

### NDK Format (sample record)

```
 PDE  2020  1  1  3 34 22.70 -15.77 -175.11  10.0 5.4 5.1 TONGA ISLANDS                  
C202001010334A   B: 38   40  40 S: 31   50  50 M: 25   55  50 CMT: 1 TRIHD:  0.7
CENTROID:      3.9 0.1 -15.63 0.01 -175.46 0.01  45.8  0.7 FREE S-20200416123122
24  0.264 0.041  0.006 0.043 -0.270 0.028  0.222 0.043 -0.043 0.027 -0.096 0.038
V10   0.339 59 302  -0.003 15  61  -0.336 27 159   0.338  3  132 56  243 35
```

## Authentication & Licensing

- **Auth**: None. Public access.
- **Rate Limits**: None stated; bulk files preferred.
- **License**: Academic use with citation. DOI: published in Physics of the Earth and Planetary Interiors.

## Integration Notes

This is *not* a real-time source. The reviewed catalog has months to years of delay. The "Quick CMT" solutions are preliminary and appear faster (days to weeks), but there's no REST API — just files in a directory structure.

The NDK (New Data Kernel) format is a fixed-width text format that's been stable since the 1980s. Parsing is straightforward but very 1980s — column-position-based fields, no delimiters. Every seismology toolkit in existence can parse NDK.

The real value of GCMT data is as an enrichment layer. When an earthquake appears in USGS or EMSC data, the GCMT solution (when available) adds the moment tensor, fault plane solution, and centroid location. This transforms a "where/when/how big" event into a "what kind of fault, how it moved" event.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | No API; file-based access; CGI search form |
| **Data Freshness**           | 1     | Months delay for reviewed catalog; days for Quick CMT |
| **Format / Schema Quality**  | 2     | NDK is well-defined but archaic fixed-width |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 3     | Every significant earthquake globally |
| **Operational Reliability**  | 3     | Running continuously since 1976; gold-standard |
| **Total**                    | **13 / 18** | |

## Verdict

⏭️ **Skip for real-time** — The catalog is scientifically invaluable but not real-time. No API exists. However, as an enrichment data source it's unmatched. If the project ever adds a "scientific context" layer to earthquake events, GCMT moment tensors would be the first enrichment to integrate. File it under "future enrichment" rather than "real-time source."
