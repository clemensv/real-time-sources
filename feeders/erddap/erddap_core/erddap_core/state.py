
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict

State = Dict[str, str]

def load_state(path: str) -> State:
    if not path:
        return {}
    p = Path(path).expanduser()
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.items()}
    except Exception:
        return {}

def save_state(path: str, state: State) -> None:
    if not path:
        return
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
