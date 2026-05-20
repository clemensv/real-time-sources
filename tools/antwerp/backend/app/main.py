"""Antwerp City Reports — FastAPI backend.

Provides domain-specific REST endpoints that query Fabric Eventhouse (KQL)
via managed identity. No raw KQL access is exposed to clients.

Endpoints:
- /api/waterbus/positions  — latest position per vessel
- /api/waterbus/names      — latest static data (name, destination) per vessel
- /api/waterbus/trails     — 2-hour position trail per vessel
- /api/maps/{path}         — Azure Maps proxy (hides subscription key)
- /api/irail/{path}        — iRail Belgian Railways proxy
- /api/health              — health check
- /api/auth/config         — MSAL SPA configuration
"""
import logging
import os
from pathlib import Path
from typing import Any

import httpx
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

log = logging.getLogger("antwerp")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

# ── Configuration ──────────────────────────────────────────────────────────
KQL_CLUSTER = os.environ["KQL_CLUSTER"]  # Fabric Eventhouse query URI (required)
KQL_DATABASE = os.environ.get("KQL_DATABASE", "antwerp")
AZURE_MAPS_KEY = os.environ.get("AZURE_MAPS_KEY", "")

# DeWaterbus + related Scheldt ferry MMSIs
WATERBUS_MMSIS = [
    205572290, 205572390, 205572490, 205572690,
    205572790, 205572890, 205231590, 205428390, 205305890,
]
_MMSI_LIST = ",".join(str(m) for m in WATERBUS_MMSIS)

# Use ManagedIdentityCredential on App Service (system-assigned, no client_id).
# DefaultAzureCredential picks up AZURE_CLIENT_ID env var which is the SPA
# app reg — not the MI — causing user-assigned MI lookups to fail.
_kql_credential = (
    ManagedIdentityCredential()
    if os.environ.get("WEBSITE_SITE_NAME")
    else DefaultAzureCredential()
)


def _get_kql_token() -> str:
    """Acquire a bearer token for KQL."""
    try:
        return _kql_credential.get_token(f"{KQL_CLUSTER}/.default").token
    except Exception as e:
        log.error("KQL token acquisition failed: %s", e)
        raise HTTPException(502, f"Failed to acquire KQL token: {e}")


async def _run_kql(query: str) -> list[dict[str, Any]]:
    """Execute a KQL query and return rows as list of dicts."""
    token = _get_kql_token()
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{KQL_CLUSTER}/v1/rest/query",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"csl": query, "db": KQL_DATABASE},
        )
    if resp.status_code != 200:
        log.error("KQL error %d: %s", resp.status_code, resp.text[:500])
        raise HTTPException(502, "KQL query failed")

    data = resp.json()
    tables = data.get("Tables", [])
    if not tables or not tables[0].get("Rows"):
        return []
    cols = [c["ColumnName"] for c in tables[0]["Columns"]]
    return [dict(zip(cols, row)) for row in tables[0]["Rows"]]


# ── FastAPI app ────────────────────────────────────────────────────────────
app = FastAPI(title="Antwerp City Reports", docs_url="/api/docs", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Waterbus endpoints ────────────────────────────────────────────────────
@app.get("/api/waterbus/positions")
async def waterbus_positions():
    """Latest position for each waterbus/ferry vessel."""
    rows = await _run_kql(f"""
        PositionReport
        | where UserID in ({_MMSI_LIST})
        | summarize arg_max(['___time'], *) by UserID
        | project mmsi=UserID, lat=Latitude, lon=Longitude,
                  sog=Sog, cog=Cog, status=NavigationalStatus,
                  ts=['___time']
    """)
    return rows


@app.get("/api/waterbus/names")
async def waterbus_names():
    """Latest static data (name, destination, type) for each vessel."""
    rows = await _run_kql(f"""
        ShipStaticData
        | where UserID in ({_MMSI_LIST})
        | summarize arg_max(['___time'], *) by UserID
        | project mmsi=UserID, name=trim(' ', Name),
                  dest=trim(' ', Destination), shiptype=Type
    """)
    return rows


@app.get("/api/waterbus/trails")
async def waterbus_trails(hours: int = Query(default=2, ge=1, le=24)):
    """Position trail for the last N hours, grouped by vessel."""
    rows = await _run_kql(f"""
        PositionReport
        | where ['___time'] > ago({hours}h)
        | where UserID in ({_MMSI_LIST})
        | where isnotnull(Latitude) and isnotnull(Longitude)
        | project mmsi=tostring(UserID), lat=Latitude, lon=Longitude, ['___time']
        | order by mmsi, ['___time'] asc
        | summarize trail=make_list(pack("lat", lat, "lon", lon)) by mmsi
    """)
    return rows


# ── Azure Maps proxy ──────────────────────────────────────────────────────
@app.get("/api/maps/{path:path}")
async def maps_proxy(path: str, request: Request):
    """Proxy Azure Maps REST API calls, injecting the subscription key."""
    if not AZURE_MAPS_KEY:
        raise HTTPException(503, "Azure Maps key not configured")

    params = dict(request.query_params)
    params["subscription-key"] = AZURE_MAPS_KEY
    url = f"https://atlas.microsoft.com/{path}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params=params)
    return Response(
        content=resp.content,
        media_type=resp.headers.get("content-type", "application/json"),
        status_code=resp.status_code,
    )


# ── iRail proxy ───────────────────────────────────────────────────────────
@app.get("/api/irail/{path:path}")
async def irail_proxy(path: str, request: Request):
    """Proxy iRail Belgian Railways API calls."""
    params = dict(request.query_params)
    url = f"https://api.irail.be/{path}"
    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        resp = await client.get(url, params=params)
    return Response(content=resp.content, media_type="application/json",
                    status_code=resp.status_code)


# ── Health ─────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "antwerp-reports"}


# ── Root and callback redirects ───────────────────────────────────────────
@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")


@app.get("/callback")
async def callback():
    return RedirectResponse("/static/index.html")


# ── Static files (mount last) ─────────────────────────────────────────────
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")
else:
    log.warning("Static directory not found at %s", static_dir)


def run():
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    run()
