from __future__ import annotations

import csv
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_BASE_URL = "https://timeseries.sepa.org.uk/KiWIS/KiWIS"
STATION_FIELDS = "station_id,station_no,station_name,station_latitude,station_longitude,river_name,catchment_name"
TS_FIELDS = "ts_id,ts_name,ts_shortname,station_id,station_name,parametertype_name,stationparameter_name,ts_unitname,ts_unitsymbol,coverage"
VALUE_FIELDS = "Timestamp,Value,Quality Code"
DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "kiwis-sources.json")
_ENV_REF = re.compile(r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))")
_CATALOG_METADATA_KEYS = {"name", "enabled", "description"}

@dataclass(frozen=True)
class KiWISEndpoint:
    kiwis_id: str
    base_url: str
    datasource: str = "0"
    station_filter: str = "station_no=*"
    timeseries_filter: str = "station_id=36870"
    ts_ids: str = ""
    period: str = "PT6H"
    api_key: str = ""

DEFAULT_ENDPOINTS = [{"kiwis_id": "sepa", "base_url": DEFAULT_BASE_URL, "station_filter": "station_id=36870", "timeseries_filter": "station_id=36870", "ts_ids": "65452010"}]
MOCK_ENDPOINTS = [KiWISEndpoint(**DEFAULT_ENDPOINTS[0])]

def build_retry_session() -> requests.Session:
    retry = Retry(total=3, connect=3, read=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=("GET",))
    adapter = HTTPAdapter(max_retries=retry, pool_connections=4, pool_maxsize=8)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": "real-time-sources-kiwis/0.1"})
    return session

def _expand_env(text: str) -> str:
    return Template(text).safe_substitute(os.environ)

def _interpolate_env(value: Any) -> Any:
    """Expand $VAR / ${VAR} placeholders in strings, recursing into lists/dicts."""
    if isinstance(value, str):
        return _ENV_REF.sub(lambda match: os.environ.get(match.group(1) or match.group(2), ""), value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(item) for key, item in value.items()}
    return value

def _read_config_text(value: str) -> str:
    value = value.strip()
    if value.startswith("@"):
        return Path(value[1:]).read_text(encoding="utf-8")
    if value.startswith("[") or value.startswith("{"):
        return value
    if value and Path(value).exists():
        return Path(value).read_text(encoding="utf-8")
    return value

def _coerce_entries(data: Any) -> List[Dict[str, Any]]:
    """Accept either a {"sources": [...]} catalog or a bare list of entries."""
    if isinstance(data, dict):
        data = data.get("sources", [])
    if not isinstance(data, list):
        return []
    return [dict(item) for item in data if isinstance(item, dict)]

def select_entries(entries: List[Dict[str, Any]], selector: str = "") -> List[Dict[str, Any]]:
    """Filter catalog entries by the KIWIS_SOURCES selector."""
    selector = (selector or "").strip()
    if selector == "*":
        return list(entries)
    if not selector:
        return [entry for entry in entries if entry.get("enabled", True)]
    by_name = {entry["name"]: entry for entry in entries if entry.get("name")}
    chosen: List[Dict[str, Any]] = []
    unknown: List[str] = []
    for token in (part.strip() for part in selector.split(",")):
        if not token:
            continue
        if token in by_name:
            chosen.append(by_name[token])
        else:
            unknown.append(token)
    if unknown:
        known = ", ".join(sorted(by_name)) or "(none)"
        raise ValueError(f"Unknown KIWIS_SOURCES entries: {', '.join(unknown)}. Known names: {known}")
    return chosen

def _entries_to_endpoints(entries: Iterable[Dict[str, Any]]) -> List[KiWISEndpoint]:
    endpoints: List[KiWISEndpoint] = []
    for raw_item in entries:
        item = _interpolate_env(raw_item)
        endpoint_args = {key: value for key, value in item.items() if key not in _CATALOG_METADATA_KEYS}
        endpoints.append(KiWISEndpoint(**endpoint_args))
    return endpoints

def load_endpoints(value: Optional[str] = None, *, mock: bool = False, sources_file: str = "", selector: str = "") -> List[KiWISEndpoint]:
    """Resolve KiWIS endpoints to poll.

    Resolution order: ``mock`` -> inline ``KIWIS_ENDPOINTS`` (legacy CSV/JSON/
    @file/path/inline) -> catalog file override -> packaged default catalog.
    The ``selector`` (KIWIS_SOURCES) then narrows catalog entries.
    """
    if mock:
        return MOCK_ENDPOINTS
    raw = _read_config_text(value or os.getenv("KIWIS_ENDPOINTS") or "")
    if raw.strip():
        raw = _expand_env(raw)
        if raw.lstrip().startswith("[") or raw.lstrip().startswith("{"):
            entries = _coerce_entries(json.loads(raw))
            return _entries_to_endpoints(select_entries(entries, selector))
        endpoints: List[KiWISEndpoint] = []
        for row in csv.reader([line for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")]):
            parts = [p.strip() for p in row]
            while len(parts) < 8:
                parts.append("")
            endpoints.append(KiWISEndpoint(parts[0], parts[1], parts[2] or "0", parts[3] or "station_no=*", parts[4] or "station_id=36870", parts[5], parts[6] or "PT6H", parts[7]))
        return endpoints
    path = sources_file.strip() if sources_file and sources_file.strip() else os.getenv("KIWIS_SOURCES_FILE", "").strip() or DEFAULT_SOURCES_FILE
    if Path(path).exists():
        entries = _coerce_entries(json.loads(Path(path).read_text(encoding="utf-8")))
    else:
        entries = [dict(item) for item in DEFAULT_ENDPOINTS]
    return _entries_to_endpoints(select_entries(entries, selector or os.getenv("KIWIS_SOURCES", "")))

def parse_datetime(value: Any) -> Optional[datetime]:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).replace("Z", "+00:00")
    return datetime.fromisoformat(text)

def _to_float(value: Any) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def _to_int(value: Any) -> Optional[int]:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def _table_rows(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, list) or not payload:
        return []
    header = payload[0]
    if not isinstance(header, list):
        return []
    return [dict(zip(header, row)) for row in payload[1:] if isinstance(row, list)]

class KiWISClient:
    def __init__(self, endpoint: KiWISEndpoint, session: Optional[requests.Session] = None, *, mock: bool = False) -> None:
        self.endpoint = endpoint
        self.session = session or build_retry_session()
        self.mock = mock

    def _get(self, request: str, **params: str) -> Any:
        query = {"service":"kisters", "type":"queryServices", "datasource":self.endpoint.datasource, "format":"json", "request":request}
        query.update(params)
        if self.endpoint.api_key:
            query["key"] = self.endpoint.api_key
        response = self.session.get(self.endpoint.base_url, params=query, timeout=30)
        response.raise_for_status()
        return response.json()

    def stations(self) -> List[Dict[str, Any]]:
        if self.mock:
            return [{"station_id":"36870","station_no":"15018","station_name":"Abbey St Bathans","station_latitude":"55.85329633","station_longitude":"-2.387448356","river_name":"Whiteadder Water","catchment_name":"Tweed"}]
        filt = _filter_dict(self.endpoint.station_filter)
        return _table_rows(self._get("getStationList", returnfields=STATION_FIELDS, **filt))

    def timeseries(self) -> List[Dict[str, Any]]:
        if self.mock:
            return [{"ts_id":"65452010","ts_name":"15minute.Total","ts_shortname":"15m.Total","station_id":"36870","station_name":"Abbey St Bathans","parametertype_name":"Precip","stationparameter_name":"Rain","ts_unitname":"millimeter","ts_unitsymbol":"mm","from":"1990-09-01T09:15:00.000Z","to":"2026-06-20T16:15:00.000Z"}]
        filt = _filter_dict(self.endpoint.timeseries_filter)
        rows = _table_rows(self._get("getTimeseriesList", returnfields=TS_FIELDS, **filt))
        if self.endpoint.ts_ids:
            wanted = set(x.strip() for x in self.endpoint.ts_ids.split(",") if x.strip())
            rows = [r for r in rows if str(r.get("ts_id")) in wanted]
        return rows[: int(os.getenv("KIWIS_MAX_TIMESERIES", "10"))]

    def values(self, ts_ids: Sequence[str]) -> Dict[str, List[Dict[str, Any]]]:
        if self.mock:
            return {"65452010":[{"Timestamp":"2026-06-20T16:15:00.000Z","Value":0.2,"Quality Code":254}]}
        if not ts_ids:
            return {}
        payload = self._get("getTimeseriesValues", ts_id=",".join(ts_ids), period=self.endpoint.period, returnfields=VALUE_FIELDS)
        result: Dict[str, List[Dict[str, Any]]] = {}
        for series in payload if isinstance(payload, list) else []:
            cols = [c.strip() for c in str(series.get("columns", "")).split(",")]
            rows = [dict(zip(cols, row)) for row in series.get("data", []) if isinstance(row, list)]
            result[str(series.get("ts_id"))] = rows
        return result

def _filter_dict(text: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for part in re.split(r"[;&]", text or ""):
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip()] = v.strip()
    return result

def normalize_station(endpoint: KiWISEndpoint, row: Dict[str, Any]) -> Dict[str, Any]:
    return {"kiwis_id": endpoint.kiwis_id, "base_url": endpoint.base_url, "station_id": str(row.get("station_id") or ""), "station_no": _none(row.get("station_no")), "station_name": _none(row.get("station_name")), "latitude": _to_float(row.get("station_latitude")), "longitude": _to_float(row.get("station_longitude")), "river_name": _none(row.get("river_name")), "catchment_name": _none(row.get("catchment_name"))}

def normalize_timeseries(endpoint: KiWISEndpoint, row: Dict[str, Any]) -> Dict[str, Any]:
    return {"kiwis_id": endpoint.kiwis_id, "base_url": endpoint.base_url, "ts_id": str(row.get("ts_id") or ""), "ts_name": _none(row.get("ts_name")), "ts_shortname": _none(row.get("ts_shortname")), "station_id": str(row.get("station_id") or ""), "station_name": _none(row.get("station_name")), "parametertype_name": _none(row.get("parametertype_name")), "stationparameter_name": _none(row.get("stationparameter_name")), "unit_name": _none(row.get("ts_unitname")), "unit_symbol": _none(row.get("ts_unitsymbol")), "coverage_from": parse_datetime(row.get("from")), "coverage_to": parse_datetime(row.get("to"))}

def normalize_value(endpoint: KiWISEndpoint, meta: Dict[str, Any], row: Dict[str, Any]) -> Dict[str, Any]:
    return {"kiwis_id": endpoint.kiwis_id, "base_url": endpoint.base_url, "ts_id": str(meta.get("ts_id") or ""), "station_id": str(meta.get("station_id") or ""), "timestamp": parse_datetime(row.get("Timestamp")) or datetime.now(timezone.utc), "value": _to_float(row.get("Value")), "quality_code": _to_int(row.get("Quality Code")), "unit_name": _none(meta.get("ts_unitname")), "unit_symbol": _none(meta.get("ts_unitsymbol")), "parametertype_name": _none(meta.get("parametertype_name")), "stationparameter_name": _none(meta.get("stationparameter_name"))}

def _none(value: Any) -> Optional[str]:
    text = "" if value is None else str(value)
    return text if text != "" else None

def load_state(path: str) -> Dict[str, str]:
    if not path or not Path(path).exists():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))

def save_state(path: str, state: Dict[str, str]) -> None:
    if not path:
        return
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")

def parse_connection_string(connection_string: str) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    for part in connection_string.split(';'):
        if '=' in part:
            k, v = part.split('=', 1); parsed[k.lower()] = v
    cfg: Dict[str, str] = {}
    if parsed.get('bootstrapserver'):
        cfg['bootstrap.servers'] = parsed['bootstrapserver']
    if parsed.get('entitypath'):
        cfg['kafka_topic'] = parsed['entitypath']
    if parsed.get('sharedaccesskeyname') and parsed.get('sharedaccesskey'):
        cfg.update({'security.protocol':'SASL_SSL','sasl.mechanism':'PLAIN','sasl.username':parsed['sharedaccesskeyname'],'sasl.password':parsed['sharedaccesskey']})
    return cfg

def build_kafka_config(args: Any) -> Dict[str, str]:
    cfg: Dict[str, str] = {}
    if getattr(args, 'connection_string', None):
        cfg.update(parse_connection_string(args.connection_string))
    if getattr(args, 'kafka_bootstrap_servers', None):
        cfg['bootstrap.servers'] = args.kafka_bootstrap_servers
    if getattr(args, 'sasl_username', None) and getattr(args, 'sasl_password', None):
        cfg.update({'security.protocol':'SASL_SSL' if getattr(args, 'kafka_enable_tls', True) else 'SASL_PLAINTEXT','sasl.mechanism':'PLAIN','sasl.username':args.sasl_username,'sasl.password':args.sasl_password})
    if getattr(args, 'kafka_enable_tls', True) is False and 'security.protocol' not in cfg:
        cfg['security.protocol'] = 'PLAINTEXT'
    if 'bootstrap.servers' not in cfg:
        cfg['bootstrap.servers'] = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    return cfg
