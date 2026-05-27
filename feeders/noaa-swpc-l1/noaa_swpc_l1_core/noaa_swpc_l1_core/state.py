"""Persisted dedup state shared by every transport feeder.

The SWPC propagated-solar-wind feed is a 7-day rolling window of ~10,080
1-minute rows. We persist only the last emitted ``time_tag`` so that
container restarts don't re-emit the entire window. Missing or unreadable
state files are treated as empty state — best effort, never raises.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict


def load_state(state_file: str) -> Dict[str, Any]:
    """Load persisted ``{"last_time_tag": "..."}`` dict; ``{}`` on miss/error."""
    if not state_file:
        return {}
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception as e:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def save_state(state_file: str, data: Dict[str, Any]) -> None:
    """Persist the dedup state. Silent on I/O errors (best-effort)."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except Exception as e:  # pylint: disable=broad-except
        logging.warning("Could not save state to %s: %s", state_file, e)
