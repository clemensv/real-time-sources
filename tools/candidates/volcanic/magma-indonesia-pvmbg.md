# MAGMA Indonesia — PVMBG Volcanic Monitoring

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | MAGMA Indonesia — Pusat Vulkanologi dan Mitigasi Bencana Geologi (PVMBG) |
| **Operator**     | Geological Agency, Indonesian Ministry of Energy and Mineral Resources |
| **URL**          | https://magma.esdm.go.id/ |
| **VONA Page**    | `https://magma.esdm.go.id/v1/vona` |
| **Coverage**     | Indonesia — 127 active volcanoes, the most of any country |
| **Update Freq.** | VONAs during eruptions; daily status reports for monitored volcanoes |

## What It Does

Indonesia has more active volcanoes than any other country on Earth. Merapi, Semeru, Sinabung, Agung, Krakatau (Anak Krakatau), Bromo — the list of dangerous, populated volcanoes is staggering. MAGMA Indonesia is the national volcanic monitoring platform operated by PVMBG (formerly BPPTKG for specific volcanoes like Merapi).

The platform issues Volcano Observatory Notices for Aviation (VONAs) — the international standard for volcanic ash advisories — and maintains volcanic activity status levels for all 127 monitored volcanoes. The system integrates seismic monitoring, visual observations, gas measurements, and deformation data.

## Endpoints Probed

| Endpoint | Status | Notes |
|----------|--------|-------|
| VONA page (HTML) | ✅ 200 | HTML page listing recent VONAs |
| `/api/v1/vona/json` | ❌ 401 | API exists but requires authentication |
| `/api/v1` | ❌ 404 | Base API not publicly accessible |
| `/rss/vona` | ❌ 404 | RSS feed not found |
| `/v1/gunung-api/informasi-letusan` | ✅ 200 | Eruption information (HTML) |

### VONA Page Content

The VONA page lists recent volcanic advisories with:
- Volcano name and VNUM (Smithsonian Volcano Number)
- Date/time of notice
- Aviation color code (GREEN/YELLOW/ORANGE/RED)
- Current activity level (Normal/Waspada/Siaga/Awas)
- Eruption description and ash cloud information

Indonesian activity levels: Normal (I), Waspada/Advisory (II), Siaga/Watch (III), Awas/Warning (IV).

## Authentication & Licensing

- **Auth**: API requires authentication (401 Unauthorized returned). Public website accessible.
- **Rate Limits**: Unknown.
- **License**: Indonesian government data. Attribution to PVMBG/MAGMA expected.

## Integration Notes

The API exists — the 401 response proves there's a JSON endpoint. Registration may be available for researchers or agencies. The HTML VONA page is publicly accessible and follows a structured format that could be parsed.

MAGMA Indonesia's VONAs also feed into the Darwin VAAC (which covers Indonesia's airspace for volcanic ash). However, the local MAGMA data includes Indonesian-specific activity levels and more detailed eruption descriptions than the VAAC advisories.

The website uses CSRF tokens (`meta name="csrf-token"`) suggesting a Laravel-based backend — the API is likely a standard REST/JSON service behind authentication.

For the 2018 Anak Krakatau tsunami and the 2021 Semeru eruption, MAGMA was the primary data source. Indonesia's volcanic monitoring is a national security function — the data infrastructure is well-maintained.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | API exists (401); HTML pages structured |
| **Data Freshness**           | 3     | Real-time VONAs during eruptions |
| **Format / Schema Quality**  | 2     | API likely JSON; HTML fallback |
| **Auth / Access Simplicity** | 1     | API requires registration/auth |
| **Coverage Relevance**       | 3     | 127 active volcanoes; most volcanic country |
| **Operational Reliability**  | 3     | National government platform; critical infrastructure |
| **Total**                    | **14 / 18** | |

## Verdict

⚠️ **Maybe — pending API access** — Indonesia's 127 active volcanoes make MAGMA one of the most important volcanic monitoring sources globally. The API exists but is gated behind authentication. If registration is available (even for research/non-commercial use), this becomes a strong Build candidate. The HTML VONA pages are a viable fallback. Darwin VAAC provides the aviation-grade ash advisories for the region, but MAGMA has deeper volcanological detail. Worth pursuing API access.
