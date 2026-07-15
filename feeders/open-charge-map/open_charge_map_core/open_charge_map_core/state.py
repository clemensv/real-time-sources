"""Persisted dedup + watermark state shared by every transport feeder.

The feeder persists a single JSON object carrying the ``modifiedsince``
high-water mark for the POI delta poller plus the per-location and per-reference
change signatures used to avoid re-emitting unchanged records. The structure of
that object is owned by the transport apps; this module only handles durable,
best-effort load/save so a corrupt or unreadable state file can never block the
feeder from starting.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict


def load_state(state_file: str) -> Dict[str, Any]:
    """Load the persisted state object. Missing/unreadable files yield ``{}``."""
    if not state_file:
        return {}
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                return data if isinstance(data, dict) else {}
    except Exception as e:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def save_state(state_file: str, data: Dict[str, Any]) -> None:
    """Persist the state object. Silent on I/O errors (best-effort)."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except Exception as e:  # pylint: disable=broad-except
        logging.warning("Could not save state to %s: %s", state_file, e)
