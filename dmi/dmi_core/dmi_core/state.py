"""Persisted dedup state shared by both DMI transport feeders.

The DMI APIs publish observations as immutable feature collections; we use
the state file to remember the most recent ``observed`` (or ``created``)
timestamp per data family so that polling cycles only emit fresh events.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict


def load_state(state_file: str) -> Dict[str, Any]:
    """Load the persisted dedup dictionary; treat any I/O error as empty state."""
    if not state_file:
        return {}
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def save_state(state_file: str, data: Dict[str, Any]) -> None:
    """Persist the dedup state. Silent on I/O errors (best-effort)."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except Exception as exc:  # pylint: disable=broad-except
        logging.warning("Could not save state to %s: %s", state_file, exc)
