from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


StateDict = Dict[str, Any]


def load_state(state_file: str) -> StateDict:
    if not state_file:
        return {"station_status": {}, "free_bike_status": {}}
    path = Path(state_file)
    if not path.exists():
        return {"station_status": {}, "free_bike_status": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"station_status": {}, "free_bike_status": {}}
    data.setdefault("station_status", {})
    data.setdefault("free_bike_status", {})
    return data


def save_state(state_file: str, state: StateDict) -> None:
    if not state_file:
        return
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
