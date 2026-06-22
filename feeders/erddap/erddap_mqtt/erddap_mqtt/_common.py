
from __future__ import annotations

import argparse
import logging
import os
import time
from typing import Any, Dict, Mapping, Type

from erddap_core import ErddapClient, build_kafka_config, load_state, parse_bool, parse_kafka_connection_string, parse_sources, save_state

DEFAULT_STATE_FILE = os.path.expanduser("~/.erddap_state.json")
logger = logging.getLogger(__name__)

def _build_values(data_pkg: Any, payload: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: data_pkg.MeasurementValue(**v) for k, v in payload.items()}

def _dataset_obj(data_pkg: Any, payload: Mapping[str, Any]) -> Any:
    variables = [data_pkg.VariableMetadata(**v) for v in payload["variables"]]
    return data_pkg.DatasetMetadata(**{**dict(payload), "variables": variables})

def _station_obj(data_pkg: Any, payload: Mapping[str, Any]) -> Any:
    return data_pkg.StationMetadata(**dict(payload))

def _observation_obj(data_pkg: Any, payload: Mapping[str, Any]) -> Any:
    record = dict(payload)
    value = record.get("time")
    if hasattr(value, "isoformat"):
        record["time"] = value.isoformat().replace("+00:00", "Z")
    return data_pkg.Observation(**{**record, "measurements": _build_values(data_pkg, payload["measurements"])})

def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    sub = parser.add_subparsers(dest="command")
    feed = sub.add_parser("feed")
    feed.add_argument("--erddap-sources", default=os.getenv("ERDDAP_SOURCES"), help="Legacy inline semicolon list, JSON array/object, @file, or path; takes precedence over the catalog")
    feed.add_argument("--erddap-sources-file", default=os.getenv("ERDDAP_SOURCES_FILE", ""), help="Path to an ERDDAP source catalog JSON file; defaults to the packaged catalog")
    feed.add_argument("--erddap-select", default=os.getenv("ERDDAP_SELECT", ""), help="Comma-separated catalog entry names, '*' for all, or unset for enabled-only")
    feed.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", os.getenv("POLL_INTERVAL", "300"))))
    feed.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "21600")))
    feed.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed.add_argument("--once", action="store_true", default=parse_bool(os.getenv("ONCE_MODE"), False))
    feed.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("ERDDAP_MOCK"), False), help="Use offline fixture and exit after one cycle")
    return parser

def main_dispatch(parser: argparse.ArgumentParser, feed_func) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s %(message)s")
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        raise SystemExit(2)
    feed_func(args)

