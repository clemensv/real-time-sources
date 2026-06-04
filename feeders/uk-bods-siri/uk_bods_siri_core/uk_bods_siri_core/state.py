from __future__ import annotations

import json
import os
from typing import Dict


def load_state(state_file: str) -> Dict[str, str]:
    if not state_file or not os.path.exists(state_file):
        return {}
    try:
        with open(state_file, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        if isinstance(raw, dict):
            return {str(k): str(v) for k, v in raw.items()}
    except (OSError, ValueError, TypeError):
        return {}
    return {}


def save_state(state_file: str, state: Dict[str, str]) -> None:
    if not state_file:
        return
    parent = os.path.dirname(state_file)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
