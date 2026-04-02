"""
Delta state management for ENTSO-E bridge.

Tracks high-water marks per (document_type, area_code) to enable delta-only polling.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict


def load_state(state_file: str) -> Dict[str, Dict[str, str]]:
    """
    Load the checkpoint state from a JSON file.

    Returns:
        Nested dict: {document_type: {area_code: iso_timestamp_str}}
    """
    if not os.path.exists(state_file):
        return {}
    with open(state_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state_file: str, state: Dict[str, Dict[str, str]]) -> None:
    """
    Save the checkpoint state to a JSON file.

    Args:
        state_file: Path to the state file.
        state: Nested dict of {document_type: {area_code: iso_timestamp_str}}.
    """
    os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_last_polled(state: Dict[str, Dict[str, str]],
                    document_type: str, area_code: str) -> datetime:
    """
    Get the last polled timestamp for a (document_type, area_code) pair.

    Returns the stored timestamp or None if no checkpoint exists.
    """
    ts_str = state.get(document_type, {}).get(area_code)
    if ts_str:
        return datetime.fromisoformat(ts_str)
    return None


def set_last_polled(state: Dict[str, Dict[str, str]],
                    document_type: str, area_code: str,
                    timestamp: datetime) -> None:
    """
    Update the last polled timestamp for a (document_type, area_code) pair.

    Args:
        state: The state dict (modified in place).
        document_type: ENTSO-E document type code.
        area_code: EIC area code.
        timestamp: The new high-water mark.
    """
    if document_type not in state:
        state[document_type] = {}
    state[document_type][area_code] = timestamp.isoformat()
