"""ICON-D2 numerical-weather-prediction grid module.

Polls https://opendata.dwd.de/weather/nwp/icon-d2/grib/{HH}/{param}/ for the
latest model run of each configured parameter, downloads each new lead-hour
GRIB2.bz2 file, decodes it with eccodes, aggregates the native ICON triangular
grid to a regular 0.1 degree lat/lon mean grid, and emits one CloudEvent per
(run, parameter, lead_hour) carrying the parallel `lats`/`lons`/`values`
arrays.

State is checkpointed per (run_id, parameter) -> set(lead_hours_emitted) so
re-polls skip already-emitted hours and detect new runs cheanly.

Heavy dependencies (eccodes, numpy) are imported lazily on first poll so a
bridge that does not enable this module does not require them at install time.
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import tempfile
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Set

from dwd.modules.base import BaseModule
from dwd.util.http_client import DWDHttpClient

logger = logging.getLogger(__name__)

_ICOND2_BASE = "weather/nwp/icon-d2/grib"
_FILE_RE = re.compile(
    r"^icon-d2_germany_icosahedral_single-level_"
    r"(?P<run_date>\d{8})(?P<run_hour>\d{2})_(?P<lead>\d{3})_2d_"
    r"(?P<param>[a-z0-9_]+)\.grib2\.bz2$"
)

# parameter -> (advertised unit string, value transform applied to raw GRIB)
DEFAULT_PARAMETERS: Dict[str, Dict[str, Any]] = {
    "t_2m":     {"unit": "degC", "offset": -273.15, "scale": 1.0},
    "tot_prec": {"unit": "mm",   "offset": 0.0,     "scale": 1.0},
    "vmax_10m": {"unit": "m/s",  "offset": 0.0,     "scale": 1.0},
    "clct":     {"unit": "%",    "offset": 0.0,     "scale": 1.0},
    "cape_ml":  {"unit": "J/kg", "offset": 0.0,     "scale": 1.0},
    "dbz_cmax": {"unit": "dBZ",  "offset": 0.0,     "scale": 1.0},
    "pmsl":     {"unit": "hPa",  "offset": 0.0,     "scale": 0.01},
    "h_snow":   {"unit": "m",    "offset": 0.0,     "scale": 1.0},
}

# DWD encodes some derived fields with 9999 as an in-band missing-value sentinel
# in addition to the GRIB header missingValue. Drop both.
_SENTINEL_9999_TOL = 1e-3


class IconD2GridModule(BaseModule):
    """Polls ICON-D2 forecast grids from DWD Open Data."""

    def __init__(self, http_client: DWDHttpClient,
                 parameters: Optional[Sequence[str]] = None,
                 resolution_deg: float = 0.1,
                 grid_cache_dir: Optional[str] = None,
                 max_files_per_poll: int = 12):
        self._http = http_client
        self._params = list(parameters) if parameters else list(DEFAULT_PARAMETERS.keys())
        for p in self._params:
            if p not in DEFAULT_PARAMETERS:
                raise ValueError(f"unsupported ICON-D2 parameter: {p}")
        self._res = float(resolution_deg)
        self._cache = grid_cache_dir or os.path.join(tempfile.gettempdir(), "icond2_grid_cache")
        os.makedirs(self._cache, exist_ok=True)
        self._max_files = int(max_files_per_poll)
        # ICON grid coordinate arrays (clat/clon) cached once per process.
        self._grid_lat = None
        self._grid_lon = None
        self._grid_bbox = None
        self._grid_ix = None
        self._grid_iy = None
        self._grid_w = None
        self._grid_h = None

    # ---- BaseModule contract ----------------------------------------------

    @property
    def name(self) -> str:
        return "icond2_grid"

    @property
    def default_enabled(self) -> bool:
        # Off by default: requires libeccodes + ~300 MB/day egress.
        return False

    @property
    def default_poll_interval(self) -> int:
        # ICON-D2 publishes 8 runs/day; a 10-min poll catches lead hours
        # as they are published without hammering the directory listings.
        return 600

    # ---- polling -----------------------------------------------------------

    def poll(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        # state shape: {"last_emitted": {run_id: {param: [lead_hours...]}}}
        last_emitted: Dict[str, Dict[str, List[int]]] = state.setdefault("last_emitted", {})
        events: List[Dict[str, Any]] = []
        files_done = 0

        for param in self._params:
            if files_done >= self._max_files:
                break
            try:
                run_id, available = self._discover_latest_run(param)
            except Exception as e:
                logger.warning("icond2_grid: discovery failed for %s: %s", param, e)
                continue
            if run_id is None:
                continue
            already = set(last_emitted.get(run_id, {}).get(param, []))
            todo = sorted(h for h in available if h not in already)
            if not todo:
                continue
            logger.info("icond2_grid: run=%s param=%s leads_todo=%d",
                        run_id, param, len(todo))

            for lead in todo:
                if files_done >= self._max_files:
                    break
                try:
                    ev = self._build_event(run_id, param, lead)
                except Exception as e:
                    logger.warning("icond2_grid: build failed run=%s param=%s lead=%d: %s",
                                   run_id, param, lead, e)
                    continue
                if ev is None:
                    continue
                events.append({"type": "icond2_grid", "data": ev})
                files_done += 1
                run_state = last_emitted.setdefault(run_id, {})
                run_state.setdefault(param, []).append(lead)

        # Garbage-collect state: keep only the 4 most recent run_ids.
        if len(last_emitted) > 4:
            for old in sorted(last_emitted.keys())[:-4]:
                del last_emitted[old]

        if events:
            logger.info("icond2_grid: emitted %d events", len(events))
        return events

    # ---- discovery ---------------------------------------------------------

    def _discover_latest_run(self, param: str):
        """Return (run_id, [lead_hours...]) for the latest run currently
        published for this parameter, or (None, []) if none found."""
        # Walk run-hour directories newest-first.
        best_run_id: Optional[str] = None
        best_leads: List[int] = []
        for hh in ("21", "18", "15", "12", "09", "06", "03", "00"):
            path = f"{_ICOND2_BASE}/{hh}/{param}/"
            try:
                entries = self._http.list_directory(path)
            except Exception as e:
                logger.debug("icond2_grid: list %s failed: %s", path, e)
                continue
            run_leads: Dict[str, List[int]] = {}
            for ent in entries:
                m = _FILE_RE.match(ent.name)
                if not m or m.group("param") != param:
                    continue
                rid = f"{m.group('run_date')}{m.group('run_hour')}"
                run_leads.setdefault(rid, []).append(int(m.group("lead")))
            if not run_leads:
                continue
            # Pick newest run_id in this directory (lexicographic == chronological).
            rid = max(run_leads.keys())
            leads = sorted(run_leads[rid])
            if best_run_id is None or rid > best_run_id:
                best_run_id, best_leads = rid, leads
        return best_run_id, best_leads

    # ---- event construction ------------------------------------------------

    def _build_event(self, run_id: str, param: str, lead: int) -> Optional[Dict[str, Any]]:
        # Import heavy deps lazily so other modules can run without them.
        import numpy as np  # noqa: F401  (kept for type clarity)
        import eccodes      # noqa: F401

        cfg = DEFAULT_PARAMETERS[param]
        run_dt = datetime.strptime(run_id, "%Y%m%d%H").replace(tzinfo=timezone.utc)
        valid_dt = run_dt.replace(hour=run_dt.hour)  # placeholder; computed below
        from datetime import timedelta
        valid_dt = run_dt + timedelta(hours=lead)

        fname = (f"icon-d2_germany_icosahedral_single-level_"
                 f"{run_id}_{lead:03d}_2d_{param}.grib2.bz2")
        url_path = f"{_ICOND2_BASE}/{run_dt.strftime('%H')}/{param}/{fname}"
        source_url = f"{self._http.base_url.rstrip('/')}/{url_path}"

        raw = self._http.download_bytes(url_path)
        if raw is None:
            return None

        cache_path = os.path.join(self._cache, fname[:-4])  # strip .bz2
        if not os.path.exists(cache_path):
            import bz2
            with open(cache_path, "wb") as fh:
                fh.write(bz2.decompress(raw))

        lats, lons, values = self._aggregate(cache_path, cfg["offset"], cfg["scale"])

        # Free the bz2-decoded GRIB after aggregation to keep disk use bounded.
        try:
            os.unlink(cache_path)
        except OSError:
            pass

        if not lats:
            return None

        bbox = self._grid_bbox
        produced_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        return {
            "run_id": run_id,
            "run_time": run_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "parameter": param,
            "unit": cfg["unit"],
            "lead_hour": int(lead),
            "valid_time": valid_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
            "produced_at": produced_at,
            "source_url": source_url,
            "resolution_deg": self._res,
            "bbox_min_lon": bbox[0],
            "bbox_min_lat": bbox[1],
            "bbox_max_lon": bbox[2],
            "bbox_max_lat": bbox[3],
            "lats": lats,
            "lons": lons,
            "values": values,
        }

    # ---- decoding + aggregation -------------------------------------------

    def _aggregate(self, grib_path: str, offset: float, scale: float):
        import numpy as np
        import eccodes

        # Load native coords once.
        if self._grid_lat is None:
            clat = self._load_coords("clat")
            clon = self._load_coords("clon")
            self._grid_lat = clat
            self._grid_lon = clon
            res = self._res
            lat_min = math.floor(clat.min() * 10) / 10
            lat_max = math.ceil(clat.max() * 10) / 10
            lon_min = math.floor(clon.min() * 10) / 10
            lon_max = math.ceil(clon.max() * 10) / 10
            self._grid_w = int(round((lon_max - lon_min) / res))
            self._grid_h = int(round((lat_max - lat_min) / res))
            self._grid_bbox = (float(lon_min), float(lat_min),
                               float(lon_max), float(lat_max))
            self._grid_ix = np.clip(((clon - lon_min) / res).astype(np.int32),
                                    0, self._grid_w - 1)
            self._grid_iy = np.clip(((clat - lat_min) / res).astype(np.int32),
                                    0, self._grid_h - 1)

        with open(grib_path, "rb") as fh:
            gid = eccodes.codes_grib_new_from_file(fh)
        try:
            missing = eccodes.codes_get_double(gid, "missingValue")
        except Exception:
            missing = 9.999e20
        vals = eccodes.codes_get_array(gid, "values").astype(np.float64)
        eccodes.codes_release(gid)

        bad = (~np.isfinite(vals)) | (vals == missing) | (np.abs(vals - 9999.0) < _SENTINEL_9999_TOL)
        good = ~bad
        v = (vals + offset) * scale

        h, w = self._grid_h, self._grid_w
        s = np.zeros((h, w), np.float64)
        c = np.zeros((h, w), np.int32)
        np.add.at(s, (self._grid_iy[good], self._grid_ix[good]), v[good])
        np.add.at(c, (self._grid_iy[good], self._grid_ix[good]), 1)
        ys, xs = np.where(c > 0)
        means = s[ys, xs] / c[ys, xs]
        lon_min, lat_min, _, _ = self._grid_bbox
        res = self._res
        lats = (lat_min + (ys + 0.5) * res).round(3).tolist()
        lons = (lon_min + (xs + 0.5) * res).round(3).tolist()
        values = means.round(3).tolist()
        return lats, lons, values

    def _load_coords(self, kind: str):
        """Load and cache the ICON-D2 native cell-centre lat/lon arrays.

        kind = 'clat' or 'clon'. DWD publishes these as GRIB2 messages at
        /weather/nwp/icon-d2/grib/grid/<kind>/icon-d2-<kind>.grib2.
        """
        import numpy as np
        import eccodes

        cache_file = os.path.join(self._cache, f"icon-d2-{kind}.grib2")
        if not os.path.exists(cache_file):
            path = f"{_ICOND2_BASE}/grid/{kind}/icon-d2-{kind}.grib2"
            data = self._http.download_bytes(path)
            if data is None:
                raise RuntimeError(f"icond2_grid: cannot fetch {path}")
            with open(cache_file, "wb") as fh:
                fh.write(data)

        with open(cache_file, "rb") as fh:
            gid = eccodes.codes_grib_new_from_file(fh)
        vals = eccodes.codes_get_array(gid, "values").astype(np.float64)
        eccodes.codes_release(gid)
        return vals
