"""Parser for DWD semicolon-delimited CSV files from ZIP archives."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Known missing-value sentinels in DWD data
MISSING_VALUES = {"-999", "-999.0", "-999.00", ""}


def parse_dwd_csv(text: str) -> List[Dict[str, Any]]:
    """Parse a DWD semicolon-delimited CSV string into a list of row dicts.

    Handles:
    - Semicolon delimiter with arbitrary whitespace
    - 'eor' end-of-record marker column
    - '-999' / '-999.0' missing value sentinel → None
    - MESS_DATUM column → ISO 8601 timestamp
    """
    lines = text.strip().splitlines()
    if not lines:
        return []

    # Parse header — strip whitespace from column names
    header = [col.strip() for col in lines[0].split(";")]
    # Remove 'eor' column if present
    if header and header[-1].lower() == "eor":
        header = header[:-1]

    rows: List[Dict[str, Any]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(";")]
        # Trim to header length (drop eor column value)
        values = values[: len(header)]
        if len(values) != len(header):
            continue

        row: Dict[str, Any] = {}
        for col, val in zip(header, values):
            if val in MISSING_VALUES:
                row[col] = None
            elif col == "MESS_DATUM":
                row[col] = _parse_mess_datum(val)
            elif col == "STATIONS_ID":
                row[col] = val.lstrip("0") or "0"
            elif col.startswith("QN"):
                row[col] = _safe_int(val)
            else:
                row[col] = _safe_float(val)
        rows.append(row)

    return rows


def _parse_mess_datum(val: str) -> Optional[str]:
    """Convert DWD MESS_DATUM (yyyyMMddHHmm or yyyyMMddHH:mm) to ISO 8601 UTC string."""
    val = val.strip().replace(":", "")
    try:
        if len(val) == 12:
            dt = datetime.strptime(val, "%Y%m%d%H%M")
        elif len(val) == 10:
            dt = datetime.strptime(val, "%Y%m%d%H")
        elif len(val) == 8:
            dt = datetime.strptime(val, "%Y%m%d")
        else:
            return val
        return dt.replace(tzinfo=timezone.utc).isoformat()
    except ValueError:
        return val


def _safe_float(val: str) -> Any:
    """Try to parse a float, return raw string on failure."""
    try:
        f = float(val)
        if f == -999.0:
            return None
        return f
    except (ValueError, TypeError):
        return val


def _safe_int(val: str) -> Any:
    """Try to parse an integer, return raw string on failure."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return val


# Column name mappings for each 10-minute parameter category
COLUMN_MAPS: Dict[str, Dict[str, str]] = {
    "air_temperature": {
        "PP_10": "pressure_station_level",
        "TT_10": "air_temperature_2m",
        "TM5_10": "air_temperature_5cm",
        "RF_10": "relative_humidity",
        "TD_10": "dew_point_temperature",
    },
    "precipitation": {
        "RWS_10": "precipitation_height",
        "RWS_IND_10": "precipitation_indicator",
    },
    "wind": {
        "FF_10": "wind_speed",
        "DD_10": "wind_direction",
    },
    "solar": {
        "GS_10": "global_radiation",
        "SD_10": "sunshine_duration",
        "DS_10": "diffuse_radiation",
        "LS_10": "longwave_radiation",
    },
    "extreme_wind": {
        "FX_10": "wind_speed",
        "FNX_10": "wind_speed",
        "DX_10": "wind_direction",
    },
    "extreme_temperature": {
        "TX_10": "air_temperature_2m",
        "TN_10": "air_temperature_5cm",
    },
}


def map_row(row: Dict[str, Any], category: str) -> Dict[str, Any]:
    """Map a parsed CSV row to the semantic field names for a given category.

    Returns a dict with 'station_id', 'timestamp', 'quality_level', and the
    category-specific measurement fields.
    """
    col_map = COLUMN_MAPS.get(category, {})
    result: Dict[str, Any] = {
        "station_id": str(row.get("STATIONS_ID", "")),
        "timestamp": row.get("MESS_DATUM", ""),
    }
    # Find the QN column (QN, QN_8, QN_3, etc.)
    for k, v in row.items():
        if k.startswith("QN"):
            result["quality_level"] = v if v is not None else 0
            break
    else:
        result["quality_level"] = 0

    for dwd_col, semantic_name in col_map.items():
        if dwd_col in row:
            result[semantic_name] = row[dwd_col]

    return result
