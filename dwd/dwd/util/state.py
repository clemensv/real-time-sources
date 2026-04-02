"""State management — load/save per-module checkpoint state."""

import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger(__name__)


def load_state(state_file: str) -> Dict[str, Any]:
    """Load persisted state from a JSON file. Returns empty dict on error."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("Could not load state from %s: %s", state_file, e)
    return {}


def save_state(state_file: str, data: Dict[str, Any]) -> None:
    """Save state to a JSON file."""
    if not state_file:
        return
    try:
        os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logger.warning("Could not save state to %s: %s", state_file, e)
