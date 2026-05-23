# Bayanat.ae - UAE Federal Open Data Portal (CKAN)

- **Country/Region**: United Arab Emirates (Federal)
- **Endpoint**: `https://bayanat.ae/api/3/action/...` (CKAN API v3)
- **Protocol**: CKAN REST API
- **Auth**: None (public API)
- **Format**: JSON
- **Freshness**: **Varies by dataset** (portal aggregates static and real-time sources)
- **Docs**: https://bayanat.ae/ (when accessible)
- **Score**: **Portal/Aggregator** (not a direct source)

## Overview

**Bayanat** is the UAE federal open data portal using CKAN. During discovery, the portal was unreachable (timeouts). If accessible, it could catalog real-time datasets from NCM, RTA, DEWA, EAD, and other agencies.

**Verdict**: **Not a source** (portal only). Value as a discovery tool if accessible in future.

**Recommendation**: Re-probe during UAE business hours (UTC+4); query CKAN API for real-time datasets if/when accessible.
