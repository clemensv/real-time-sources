"""Build the dwd_ingest Fabric notebook programmatically.

Run::

    python build_notebook.py

Outputs ``dwd_ingest.ipynb`` next to this script.

The notebook is **workspace-agnostic**: parameter cells carry empty defaults
for ``LAKEHOUSE_PATH``, ``KUSTO_URI`` and ``KUSTO_DATABASE``; the deploy
script (``tools/deploy-fabric/deploy-fabric-notebook.ps1`` invoked via
``setup.ps1`` in this directory) patches them and binds the notebook to
the resolved KQL database.

The notebook reads new DWD CloudEvents from the Eventhouse
``_cloudevents_dispatch`` landing table (populated by the ``dwd-ingest``
Eventstream) using a watermark stored in
``Files/_state/dwd_ingest_watermark.json``. For every file-reference event
(``DE.DWD.Radar.RadarFileProduct`` and ``DE.DWD.Forecast.IconD2ForecastFile``)
it fetches ``file_url`` anonymously, lands the raw bytes under
``Files/bronze/<channel>/...`` and, where decoders are available, converts
the payload to a Cloud Optimized GeoTIFF under ``Files/gold/<channel>_cog/...``
and inserts an index row into the KQL ``CogCatalog`` table so Fabric Maps
imagery layers can find the latest tile.

Triggering: run the notebook on a schedule for the simple case, or wire an
Activator (Reflex) destination on the Eventstream (``setup.ps1
-ActivatorName <name>``) and have its rule invoke this notebook via the
"Run Fabric item" action.
"""

from __future__ import annotations

import json
from pathlib import Path

NB_PATH = Path(__file__).parent / "dwd_ingest.ipynb"


def code(src: str, tags: list[str] | None = None) -> dict:
    cell = {
        "cell_type": "code",
        "metadata": {"language": "python"},
        "execution_count": None,
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }
    if tags:
        cell["metadata"]["tags"] = tags
    return cell


def md(src: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": src.splitlines(keepends=True),
    }


CELLS = [
    md(
        "# DWD Ingest — Eventhouse → Lakehouse (bronze + silver + COG gold)\n\n"
        "Reads new DWD CloudEvents from the Eventhouse `_cloudevents_dispatch` "
        "landing table (populated by the `dwd-ingest` Eventstream) and, for every "
        "file-reference event (radar composite, ICON-D2 forecast file), fetches "
        "`file_url` anonymously, writes raw bytes to `Files/bronze/<channel>/...`, "
        "and—when GIS decoders are available—publishes a Cloud Optimized GeoTIFF "
        "to `Files/gold/<channel>_cog/...` and registers it in the KQL "
        "`CogCatalog` table for Fabric Maps imagery layers.\n\n"
        "**Bound automatically by `tools/dwd/fabric/setup.ps1`:**\n"
        "- `LAKEHOUSE_PATH` — abfss URI of the default Lakehouse for this notebook\n"
        "- `KUSTO_URI` / `KUSTO_DATABASE` — DWD KQL database\n\n"
        "**Triggering:**\n"
        "1. *Scheduled* (default): attach this notebook to a Fabric schedule "
        "(every N minutes); each run advances a watermark stored in "
        "`Files/_state/dwd_ingest_watermark.json`.\n"
        "2. *Event-driven*: add an Activator (Reflex) destination to the "
        "Eventstream, then create an Activator rule with a *Run Fabric item* "
        "action targeting this notebook. `setup.ps1 -ActivatorName <name>` "
        "wires the Activator destination."
    ),
    code(
        "# Install GIS decoders if not already in the Fabric environment.\n"
        "# In production these belong in a Fabric Environment item attached to the\n"
        "# notebook; the install here is a fallback for ad-hoc runs.\n"
        "%pip install -q --no-cache-dir cfgrib eccodes h5py rasterio rio-cogeo requests\n",
    ),
    code(
        "# === PARAMETERS ===\n"
        "# Patched per workspace by tools/dwd/fabric/setup.ps1.\n"
        '\n'
        '# OneLake Lakehouse root for bronze/gold files (abfss://...).\n'
        'LAKEHOUSE_PATH       = ""\n'
        '\n'
        '# Eventhouse / KQL database that holds the CogCatalog table.\n'
        'KUSTO_URI            = ""\n'
        'KUSTO_DATABASE       = "dwd"\n'
        '\n'
        '# DWD upstream guidance: identify yourself in the User-Agent.\n'
        'USER_AGENT           = "fabric-dwd-ingest/1.0 (+https://github.com/clemensv/real-time-sources)"\n'
        '\n'
        '# Streaming knobs.\n'
        'TRIGGER_SECONDS      = 30\n'
        'FETCH_CONCURRENCY    = 16\n'
        '\n'
        '# ICON-D2 parameters that get rendered to COG in gold (the bronze copy is\n'
        '# always written regardless). Keep this list small — full archive lives in\n'
        '# bronze.\n'
        'ICON_D2_COG_PARAMS   = {"t_2m", "tot_prec", "td_2m", "u_10m", "v_10m", "ww"}\n'
        '\n'
        '# Reprojection target for all gold COGs. EPSG:3857 is the native CRS of\n'
        '# Azure Maps basemaps used by Fabric Maps.\n'
        'COG_TARGET_CRS       = "EPSG:3857"\n',
        tags=["parameters"],
    ),
    code(
        "import os, io, bz2, hashlib, json, time, datetime as _dt, traceback\n"
        "from urllib.parse import urlparse\n"
        "from concurrent.futures import ThreadPoolExecutor, as_completed\n"
        "\n"
        "import requests\n"
        "from pyspark.sql import functions as F\n"
        "from pyspark.sql.types import (\n"
        "    StructType, StructField, StringType, LongType, IntegerType, TimestampType,\n"
        "    DoubleType, ArrayType\n"
        ")\n"
        "\n"
        "# Optional decoders — gated so the notebook still runs on a vanilla pool.\n"
        "try:\n"
        "    import cfgrib  # noqa: F401\n"
        "    import xarray as xr\n"
        "    HAVE_CFGRIB = True\n"
        "except Exception:\n"
        "    HAVE_CFGRIB = False\n"
        "try:\n"
        "    import h5py  # noqa: F401\n"
        "    HAVE_H5 = True\n"
        "except Exception:\n"
        "    HAVE_H5 = False\n"
        "try:\n"
        "    import rasterio\n"
        "    from rasterio.io import MemoryFile\n"
        "    from rasterio.warp import calculate_default_transform, reproject, Resampling\n"
        "    from rio_cogeo.cogeo import cog_translate\n"
        "    from rio_cogeo.profiles import cog_profiles\n"
        "    HAVE_COG = True\n"
        "except Exception:\n"
        "    HAVE_COG = False\n"
        "\n"
        "print(f\"HAVE_CFGRIB={HAVE_CFGRIB}  HAVE_H5={HAVE_H5}  HAVE_COG={HAVE_COG}\")\n"
    ),
    md(
        "## Helpers — fetch, bronze write, COG render, KQL index update"
    ),
    code(
        "def _bronze_path(channel: str, file_name: str, *parts: str) -> str:\n"
        "    return f\"{LAKEHOUSE_PATH}/Files/bronze/{channel}/\" + \"/\".join([*parts, file_name])\n"
        "\n"
        "def _gold_path(channel: str, file_name: str, *parts: str) -> str:\n"
        "    return f\"{LAKEHOUSE_PATH}/Files/gold/{channel}_cog/\" + \"/\".join([*parts, file_name])\n"
        "\n"
        "def _write_atomic(target: str, body: bytes) -> int:\n"
        "    tmp = target + \".tmp\"\n"
        "    # Spark / OneLake uses the Hadoop FS API; use mssparkutils for fast writes.\n"
        "    from notebookutils import mssparkutils  # type: ignore\n"
        "    mssparkutils.fs.put(tmp, body, overwrite=True)  # text/bytes\n"
        "    mssparkutils.fs.mv(tmp, target, overwrite=True)\n"
        "    return len(body)\n"
        "\n"
        "def _exists(path: str) -> bool:\n"
        "    from notebookutils import mssparkutils  # type: ignore\n"
        "    try:\n"
        "        mssparkutils.fs.ls(path)\n"
        "        return True\n"
        "    except Exception:\n"
        "        return False\n"
        "\n"
        "def _http_get(url: str) -> bytes:\n"
        "    r = requests.get(url, headers={\"User-Agent\": USER_AGENT}, timeout=60)\n"
        "    r.raise_for_status()\n"
        "    return r.content\n"
    ),
    code(
        "def _to_cog_from_array(array_2d, transform, src_crs, target_path: str) -> dict:\n"
        "    \"\"\"Reproject a 2D numpy array into a Cloud Optimized GeoTIFF at target_path.\n"
        "    Returns {bbox: [...], crs: 'EPSG:3857', bytes: N, sha256: ...}.\n"
        "    \"\"\"\n"
        "    assert HAVE_COG, \"rasterio/rio-cogeo not available\"\n"
        "    import numpy as np\n"
        "    height, width = array_2d.shape\n"
        "    src_profile = {\n"
        "        'driver': 'GTiff', 'height': height, 'width': width, 'count': 1,\n"
        "        'dtype': str(array_2d.dtype), 'crs': src_crs, 'transform': transform,\n"
        "        'nodata': float('nan') if np.issubdtype(array_2d.dtype, np.floating) else None,\n"
        "    }\n"
        "    with MemoryFile() as mem:\n"
        "        with mem.open(**src_profile) as ds:\n"
        "            ds.write(array_2d, 1)\n"
        "        # Reproject + COG-encode into a second memfile.\n"
        "        with MemoryFile() as cog_mem:\n"
        "            cog_profile = cog_profiles.get('deflate')\n"
        "            cog_profile.update(dict(BIGTIFF='IF_SAFER'))\n"
        "            cog_translate(\n"
        "                mem.open(),\n"
        "                cog_mem.name,\n"
        "                cog_profile,\n"
        "                in_memory=True,\n"
        "                dst_kwargs={'crs': COG_TARGET_CRS},\n"
        "                quiet=True,\n"
        "                web_optimized=True,\n"
        "                overview_resampling='average',\n"
        "                overview_level=4,\n"
        "            )\n"
        "            cog_bytes = cog_mem.read()\n"
        "    written = _write_atomic(target_path, cog_bytes)\n"
        "    with MemoryFile(cog_bytes) as mf, mf.open() as ds:\n"
        "        b = ds.bounds\n"
        "        return {\n"
        "            'bbox': [b.left, b.bottom, b.right, b.top],\n"
        "            'crs': str(ds.crs),\n"
        "            'bytes': written,\n"
        "            'sha256': hashlib.sha256(cog_bytes).hexdigest(),\n"
        "        }\n"
    ),
    code(
        "def _kql_ingest_cog(rows: list[dict]) -> None:\n"
        "    if not rows or not KUSTO_URI or not KUSTO_DATABASE:\n"
        "        return\n"
        "    try:\n"
        "        from azure.kusto.data import KustoConnectionStringBuilder\n"
        "        from azure.kusto.ingest import QueuedIngestClient, IngestionProperties, DataFormat\n"
        "        from azure.kusto.data.helpers import dataframe_from_result_table  # noqa\n"
        "    except ImportError:\n"
        "        # Fall back to .ingest inline via management endpoint if SDK absent.\n"
        "        from azure.identity import DefaultAzureCredential\n"
        "        cred = DefaultAzureCredential()\n"
        "        tok = cred.get_token('https://kusto.kusto.windows.net/.default').token\n"
        "        body = '\\n'.join(json.dumps(r, default=str) for r in rows)\n"
        "        csl = f\".ingest inline into table CogCatalog with (format='multijson') <|\\n{body}\"\n"
        "        requests.post(f\"{KUSTO_URI}/v1/rest/mgmt\",\n"
        "            headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},\n"
        "            json={'db': KUSTO_DATABASE, 'csl': csl}, timeout=60).raise_for_status()\n"
        "        return\n"
        "    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(KUSTO_URI)\n"
        "    client = QueuedIngestClient(kcsb)\n"
        "    buf = io.BytesIO('\\n'.join(json.dumps(r, default=str) for r in rows).encode('utf-8'))\n"
        "    client.ingest_from_stream(buf, IngestionProperties(\n"
        "        database=KUSTO_DATABASE, table='CogCatalog', data_format=DataFormat.MULTIJSON\n"
        "    ))\n"
    ),
    md(
        "## Per-channel handlers"
    ),
    code(
        "def _radar_handle(ev: dict) -> dict | None:\n"
        "    data = ev.get('data') or {}\n"
        "    url = data.get('file_url')\n"
        "    product = data.get('product') or 'unknown'\n"
        "    file_name = data.get('file_name') or os.path.basename(urlparse(url).path)\n"
        "    if not url:\n"
        "        return None\n"
        "    modified = data.get('modified') or ev.get('time')\n"
        "    dt = _dt.datetime.fromisoformat(modified.replace('Z','+00:00')) if modified else _dt.datetime.utcnow()\n"
        "    parts = (f\"yyyy={dt.year:04d}\", f\"mm={dt.month:02d}\", f\"dd={dt.day:02d}\", f\"HH={dt.hour:02d}\")\n"
        "    bronze = _bronze_path('radar', file_name, product, *parts)\n"
        "    if not _exists(bronze):\n"
        "        body = _http_get(url)\n"
        "        if file_name.endswith('.bz2'):\n"
        "            body = bz2.decompress(body)\n"
        "            file_name = file_name[:-4]\n"
        "            bronze = _bronze_path('radar', file_name, product, *parts)\n"
        "        _write_atomic(bronze, body)\n"
        "    # COG rendering only for ODIM-H5 sources we can decode.\n"
        "    if not (HAVE_H5 and HAVE_COG):\n"
        "        return None\n"
        "    if not file_name.endswith('.h5'):\n"
        "        return None\n"
        "    try:\n"
        "        import numpy as np\n"
        "        import h5py\n"
        "        from rasterio.transform import from_origin\n"
        "        with h5py.File(io.BytesIO(_http_get(url)), 'r') as f:\n"
        "            ds = f['/dataset1/data1/data'][...]\n"
        "            where = f['/where'].attrs\n"
        "            ll_lon = float(where.get('LL_lon', 5.0))\n"
        "            ll_lat = float(where.get('LL_lat', 47.0))\n"
        "            ur_lon = float(where.get('UR_lon', 16.0))\n"
        "            ur_lat = float(where.get('UR_lat', 55.0))\n"
        "        h, w = ds.shape\n"
        "        transform = from_origin(ll_lon, ur_lat, (ur_lon-ll_lon)/w, (ur_lat-ll_lat)/h)\n"
        "        gold = _gold_path('radar', file_name.replace('.h5','.tif'), product, *parts)\n"
        "        info = _to_cog_from_array(ds.astype('float32'), transform, 'EPSG:4326', gold)\n"
        "    except Exception as ex:\n"
        "        print(f\"radar COG failed for {url}: {ex}\")\n"
        "        return None\n"
        "    return {\n"
        "        'channel': 'radar', 'product': product,\n"
        "        'valid_time': dt.isoformat(), 'run': None, 'lead_hour': None,\n"
        "        'parameter': None, 'level_type': None, 'level': None,\n"
        "        'file_url': url, 'cog_path': gold,\n"
        "        'bbox': info['bbox'], 'crs': info['crs'],\n"
        "        'bytes': info['bytes'], 'sha256': info['sha256'],\n"
        "        'written_at': _dt.datetime.utcnow().isoformat(),\n"
        "    }\n"
    ),
    code(
        "def _icon_d2_handle(ev: dict) -> dict | None:\n"
        "    data = ev.get('data') or {}\n"
        "    url = data.get('file_url')\n"
        "    if not url:\n"
        "        return None\n"
        "    parameter = data.get('parameter') or 'unknown'\n"
        "    level_type = data.get('level_type') or 'unknown'\n"
        "    level = str(data.get('level') or 'na')\n"
        "    run_iso = data.get('run')\n"
        "    lead = int(data.get('forecast_hour') or 0)\n"
        "    file_name = data.get('file_name') or os.path.basename(urlparse(url).path)\n"
        "    run_dt = _dt.datetime.fromisoformat(run_iso.replace('Z','+00:00')) if run_iso else _dt.datetime.utcnow()\n"
        "    run_tag = run_dt.strftime('%Y%m%d%H')\n"
        "    parts = (f\"run={run_tag}\", f\"lead={lead:03d}\", parameter, level_type, level)\n"
        "    bronze = _bronze_path('icon-d2', file_name, *parts)\n"
        "    payload_grib2 = None\n"
        "    if not _exists(bronze):\n"
        "        body = _http_get(url)\n"
        "        _write_atomic(bronze, body)\n"
        "        payload_grib2 = bz2.decompress(body) if file_name.endswith('.bz2') else body\n"
        "    # Render to COG only for the configured parameter set and only if cfgrib is around.\n"
        "    if parameter not in ICON_D2_COG_PARAMS:\n"
        "        return None\n"
        "    if not (HAVE_CFGRIB and HAVE_COG):\n"
        "        return None\n"
        "    try:\n"
        "        if payload_grib2 is None:\n"
        "            body = _http_get(url)\n"
        "            payload_grib2 = bz2.decompress(body) if file_name.endswith('.bz2') else body\n"
        "        # cfgrib needs a real path.\n"
        "        scratch = f\"/tmp/{run_tag}_{lead:03d}_{parameter}_{level}.grib2\"\n"
        "        with open(scratch, 'wb') as f:\n"
        "            f.write(payload_grib2)\n"
        "        ds = xr.open_dataset(scratch, engine='cfgrib')\n"
        "        var = list(ds.data_vars)[0]\n"
        "        arr = ds[var].values\n"
        "        if arr.ndim == 3:  # collapse leading singletons\n"
        "            arr = arr[0]\n"
        "        lats = ds['latitude'].values\n"
        "        lons = ds['longitude'].values\n"
        "        from rasterio.transform import from_bounds\n"
        "        transform = from_bounds(float(lons.min()), float(lats.min()),\n"
        "                                float(lons.max()), float(lats.max()),\n"
        "                                arr.shape[1], arr.shape[0])\n"
        "        gold = _gold_path('icon-d2', file_name.replace('.grib2.bz2', '.tif').replace('.grib2', '.tif'), *parts)\n"
        "        info = _to_cog_from_array(arr.astype('float32'), transform, 'EPSG:4326', gold)\n"
        "    except Exception as ex:\n"
        "        print(f\"icon-d2 COG failed for {url}: {ex}\")\n"
        "        return None\n"
        "    return {\n"
        "        'channel': 'icon-d2',\n"
        "        'product': f\"{parameter}/{level_type}/{level}\",\n"
        "        'valid_time': (run_dt + _dt.timedelta(hours=lead)).isoformat(),\n"
        "        'run': run_dt.isoformat(), 'lead_hour': lead,\n"
        "        'parameter': parameter, 'level_type': level_type, 'level': level,\n"
        "        'file_url': url, 'cog_path': gold,\n"
        "        'bbox': info['bbox'], 'crs': info['crs'],\n"
        "        'bytes': info['bytes'], 'sha256': info['sha256'],\n"
        "        'written_at': _dt.datetime.utcnow().isoformat(),\n"
        "    }\n"
    ),
    md(
        "## Driver: watermark-driven KQL pull + `process_batch`\n\n"
        "Each notebook run reads new rows from `_cloudevents_dispatch` since the "
        "stored watermark, classifies each event by CloudEvents `type`, dispatches "
        "to the per-channel handler with a bounded thread pool, writes any "
        "resulting `CogCatalog` rows in one KQL ingest, and advances the watermark."
    ),
    code(
        "def _classify(row) -> str:\n"
        "    t = (row.get('type') or '').lower()\n"
        "    if t.endswith('.radarfileproduct'):     return 'radar'\n"
        "    if t.endswith('.icond2forecastfile'):   return 'icon-d2'\n"
        "    return 'ignore'\n"
        "\n"
        "def _dispatch(row: dict):\n"
        "    kind = _classify(row)\n"
        "    if kind == 'radar':   return _radar_handle(row)\n"
        "    if kind == 'icon-d2': return _icon_d2_handle(row)\n"
        "    return None\n"
        "\n"
        "def process_batch(rows: list, epoch_id):\n"
        "    if not rows:\n"
        "        return\n"
        "    cog_rows: list[dict] = []\n"
        "    with ThreadPoolExecutor(max_workers=FETCH_CONCURRENCY) as pool:\n"
        "        for fut in as_completed(pool.submit(_dispatch, r) for r in rows):\n"
        "            try:\n"
        "                out = fut.result()\n"
        "                if out is not None:\n"
        "                    cog_rows.append(out)\n"
        "            except Exception as ex:\n"
        "                print(f\"batch handler error: {ex}\\n{traceback.format_exc()}\")\n"
        "    if cog_rows:\n"
        "        _kql_ingest_cog(cog_rows)\n"
        "    print(f\"epoch={epoch_id} events={len(rows)} cog_rows={len(cog_rows)}\")\n"
    ),
    code(
        "# Watermark stored in the Lakehouse so each run picks up where the last left off.\n"
        "import json as _json\n"
        "from datetime import datetime, timezone\n"
        "\n"
        "WATERMARK_PATH = f\"{LAKEHOUSE_PATH}/Files/_state/dwd_ingest_watermark.json\"\n"
        "\n"
        "def _load_watermark() -> str:\n"
        "    try:\n"
        "        raw = mssparkutils.fs.head(WATERMARK_PATH, 4096)\n"
        "        return _json.loads(raw)['since']\n"
        "    except Exception:\n"
        "        # First run: start from 'now - 10 minutes' to avoid huge backfill.\n"
        "        return (datetime.now(timezone.utc).replace(microsecond=0).isoformat()\n"
        "                .replace('+00:00', 'Z'))\n"
        "\n"
        "def _save_watermark(ts: str) -> None:\n"
        "    payload = _json.dumps({'since': ts})\n"
        "    mssparkutils.fs.put(WATERMARK_PATH, payload, overwrite=True)\n"
        "\n"
        "def _kql_query(csl: str) -> list[dict]:\n"
        "    cred = DefaultAzureCredential()\n"
        "    tok = cred.get_token('https://kusto.kusto.windows.net/.default').token\n"
        "    resp = requests.post(f\"{KUSTO_URI}/v1/rest/query\",\n"
        "        headers={'Authorization': f'Bearer {tok}'},\n"
        "        json={'db': KUSTO_DATABASE, 'csl': csl}, timeout=120)\n"
        "    resp.raise_for_status()\n"
        "    tables = resp.json().get('Tables') or resp.json().get('tables') or []\n"
        "    if not tables: return []\n"
        "    t = tables[0]\n"
        "    cols = [c['ColumnName'] if 'ColumnName' in c else c['name'] for c in t.get('Columns') or t.get('columns')]\n"
        "    return [dict(zip(cols, r)) for r in (t.get('Rows') or t.get('rows') or [])]\n"
        "\n"
        "since = _load_watermark()\n"
        "print(f\"reading _cloudevents_dispatch since {since}\")\n"
        "csl = (f\"_cloudevents_dispatch \"\n"
        "       f\"| where ['time'] > datetime({since}) \"\n"
        "       f\"| where type startswith 'DE.DWD.' \"\n"
        "       f\"| project ['time'], specversion, type, source, ['id'], subject, data \"\n"
        "       f\"| order by ['time'] asc\")\n"
        "rows = _kql_query(csl)\n"
        "process_batch(rows, epoch_id=since)\n"
        "if rows:\n"
        "    _save_watermark(rows[-1]['time'])\n"
        "    print(f\"watermark advanced to {rows[-1]['time']}\")\n"
    ),
]


def build() -> None:
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"name": "synapse_pyspark", "display_name": "Synapse PySpark"},
            "language_info": {"name": "python"},
            "dependencies": {"kqlDatabases": []},
        },
        "cells": CELLS,
    }
    NB_PATH.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    print(f"Wrote {NB_PATH} ({NB_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
