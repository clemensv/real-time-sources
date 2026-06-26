
from __future__ import annotations

import datetime as dt
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ErddapSource

logger = logging.getLogger(__name__)
COMMON_COLUMNS = ["time", "latitude", "longitude", "depth", "z"]

@dataclass
class VariableInfo:
    name: str
    data_type: Optional[str] = None
    unit: Optional[str] = None
    long_name: Optional[str] = None
    standard_name: Optional[str] = None
    ioos_category: Optional[str] = None
    cf_role: Optional[str] = None

@dataclass
class DatasetSnapshot:
    dataset: Dict[str, Any]
    station: Dict[str, Any]
    observations: List[Dict[str, Any]]
    state_updates: Dict[str, str]
    variables: Dict[str, VariableInfo]


def _parse_time(value: Any) -> Optional[dt.datetime]:
    if value in (None, ""):
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def _iso_datetime(value: Any) -> Optional[str]:
    parsed = _parse_time(value)
    return parsed.isoformat().replace("+00:00", "Z") if parsed else None


def _numeric(value: Any) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_id(value: str) -> str:
    out = []
    for ch in str(value):
        out.append(ch if ch.isalnum() or ch in ("-", "_", ".") else "-")
    return "".join(out).strip("-") or "unknown"

class ErddapClient:
    def __init__(self, fixture_path: Optional[str] = None) -> None:
        self.fixture_path = fixture_path
        self.session = requests.Session()
        retry = Retry(total=3, connect=3, read=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=("GET",))
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _get_json(self, url: str, source: ErddapSource) -> Mapping[str, Any]:
        if source.auth_header:
            headers = {"Authorization": source.auth_header}
        else:
            headers = {}
        resp = self.session.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _load_fixture(self) -> Mapping[str, Any]:
        path = Path(self.fixture_path) if self.fixture_path else Path("fixtures/mock_erddap.json")
        if not path.exists():
            path = Path(__file__).resolve().parents[2] / "fixtures" / "mock_erddap.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def fetch_dataset(self, source: ErddapSource, state: Mapping[str, str], mock: bool = False) -> DatasetSnapshot:
        if mock:
            fixture = self._load_fixture()
            info_payload = fixture["info"]
            table_payload = fixture["table"]
            catalog = fixture.get("catalog", {})
        else:
            info_payload = self._get_json(f"{source.base_url}/info/{source.dataset_id}/index.json", source)
            query_columns = self._select_columns(source, info_payload)
            query = quote(",".join(query_columns), safe=",") + "&" + source.time_constraint + "&orderBy(%22time%22)"
            table_payload = self._get_json(f"{source.base_url}/tabledap/{source.dataset_id}.json?{query}", source)
            catalog = {}
        variables, globals_ = parse_info(info_payload)
        station_var = source.station_id_variable or next((v.name for v in variables.values() if v.cf_role == "timeseries_id"), None)
        station_id = _safe_id(source.dataset_id)
        rows = table_payload.get("table", {}).get("rows", [])
        col_names = list(table_payload.get("table", {}).get("columnNames", []))
        col_units = list(table_payload.get("table", {}).get("columnUnits", []))
        if rows and station_var in col_names:
            val = rows[0][col_names.index(station_var)]
            if val not in (None, ""):
                station_id = _safe_id(str(val))
        station_attrs = {k: str(v) for k, v in globals_.items() if k in ("title", "summary", "institution", "creator_name", "license") and v is not None}
        if station_var and station_var in variables:
            vi = variables[station_var]
            station_attrs.update({k: str(v) for k, v in {"long_name": vi.long_name, "cf_role": vi.cf_role, "ioos_category": vi.ioos_category}.items() if v})
        lat = _first_numeric(rows, col_names, "latitude")
        lon = _first_numeric(rows, col_names, "longitude")
        depth = _first_numeric(rows, col_names, "depth") or _first_numeric(rows, col_names, "z")
        station = {"erddap_id": source.erddap_id, "dataset_id": source.dataset_id, "base_url": source.base_url, "station_id": station_id, "station_name": (variables.get(station_var).long_name if station_var and station_var in variables else catalog.get("title")), "station_id_variable": station_var, "latitude": lat, "longitude": lon, "depth": depth, "attributes": station_attrs}
        dataset = {"erddap_id": source.erddap_id, "dataset_id": source.dataset_id, "base_url": source.base_url, "title": catalog.get("title") or globals_.get("title"), "cdm_data_type": catalog.get("cdm_data_type") or globals_.get("cdm_data_type"), "min_time": _iso_datetime(catalog.get("minTime") or globals_.get("time_coverage_start")), "max_time": _iso_datetime(catalog.get("maxTime") or globals_.get("time_coverage_end")), "info_url": f"{source.base_url}/info/{source.dataset_id}/index.json", "time_variable": "time", "station_id_variable": station_var, "global_attributes": {str(k): str(v) for k, v in globals_.items() if v is not None}, "variables": [vars(v) for v in variables.values()]}
        observations: List[Dict[str, Any]] = []
        updates: Dict[str, str] = {}
        for row in rows:
            rec = dict(zip(col_names, row))
            obs_time = _parse_time(rec.get("time"))
            if not obs_time:
                continue
            key = f"{source.erddap_id}/{source.dataset_id}/{station_id}"
            iso = obs_time.isoformat().replace("+00:00", "Z")
            if state.get(key, "") >= iso:
                continue
            measurements: Dict[str, Dict[str, Any]] = {}
            for idx, name in enumerate(col_names):
                if name in {station_var, "time", "latitude", "longitude", "depth", "z"}:
                    continue
                if name not in source.variables:
                    continue
                value = rec.get(name)
                vi = variables.get(name, VariableInfo(name=name, unit=(col_units[idx] if idx < len(col_units) else None)))
                val_double = _numeric(value)
                measurements[name] = {"variable_name": name, "value_double": val_double, "value_string": None if val_double is not None or value is None else str(value), "unit": vi.unit or (col_units[idx] if idx < len(col_units) else None), "long_name": vi.long_name, "standard_name": vi.standard_name, "ioos_category": vi.ioos_category, "quality_flag": None}
            if not measurements:
                continue
            observations.append({"erddap_id": source.erddap_id, "dataset_id": source.dataset_id, "base_url": source.base_url, "station_id": station_id, "time": obs_time, "latitude": _numeric(rec.get("latitude")) or lat, "longitude": _numeric(rec.get("longitude")) or lon, "depth": _numeric(rec.get("depth")) or _numeric(rec.get("z")) or depth, "measurements": measurements})
            updates[key] = max(updates.get(key, ""), iso)
        return DatasetSnapshot(dataset, station, observations, updates, variables)

    def _select_columns(self, source: ErddapSource, info_payload: Mapping[str, Any]) -> List[str]:
        variables, _ = parse_info(info_payload)
        station_var = source.station_id_variable or next((v.name for v in variables.values() if v.cf_role == "timeseries_id"), None)
        cols: List[str] = []
        for c in [station_var, "time", "latitude", "longitude", "depth", "z", *source.variables]:
            if c and c in variables and c not in cols:
                cols.append(c)
        return cols or ["time", *source.variables]

def _first_numeric(rows: List[List[Any]], names: List[str], col: str) -> Optional[float]:
    if col not in names:
        return None
    idx = names.index(col)
    for row in rows:
        val = _numeric(row[idx])
        if val is not None:
            return val
    return None

def parse_info(payload: Mapping[str, Any]) -> Tuple[Dict[str, VariableInfo], Dict[str, Any]]:
    variables: Dict[str, VariableInfo] = {}
    globals_: Dict[str, Any] = {}
    for row in payload.get("table", {}).get("rows", []):
        row_type, variable, attr, data_type, value = (list(row) + [None] * 5)[:5]
        if row_type == "variable" and variable:
            variables.setdefault(variable, VariableInfo(name=variable)).data_type = data_type
        elif row_type == "attribute" and variable == "NC_GLOBAL" and attr:
            globals_[attr] = value
        elif row_type == "attribute" and variable:
            vi = variables.setdefault(variable, VariableInfo(name=variable))
            if attr == "units": vi.unit = value
            elif attr == "long_name": vi.long_name = value
            elif attr == "standard_name": vi.standard_name = value
            elif attr == "ioos_category": vi.ioos_category = value
            elif attr == "cf_role": vi.cf_role = value
    return variables, globals_
