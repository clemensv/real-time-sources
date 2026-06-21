"""Delta-detection helpers for normalized features."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, MutableMapping, Optional

from poller_core.models import NormalizedFeature


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def stable_feature_hash(feature: NormalizedFeature) -> str:
    """Return a stable SHA-256 hash of a feature's attributes and geometry.

    Args:
        feature: Normalized feature whose id is excluded from the hash. Excluding
            id means the digest reflects payload changes only.
    """

    payload = {"attributes": feature.get("attributes", {}), "geometry": feature.get("geometry")}
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FeatureState:
    """Persisted delta marker for one feature id.

    Args:
        version: Edit timestamp or stable hash used for change detection.
        mode: Detection mode that produced version, either "timestamp" or
            "hash".
    """

    version: str
    mode: str


class DeltaDetector:
    """Detect new or changed normalized features against persisted state.

    Args:
        timestamp_field: Optional field name or dotted path inside feature
            attributes. When it resolves to a non-empty value for a feature, that
            value is used as the version. Otherwise the detector falls back to a
            stable attributes+geometry hash.
    """

    def __init__(self, timestamp_field: Optional[str] = None) -> None:
        self.timestamp_field = timestamp_field

    def feature_state(self, feature: NormalizedFeature) -> FeatureState:
        """Return the current delta marker for a normalized feature."""
        timestamp = _get_path(feature.get("attributes", {}), self.timestamp_field)
        if timestamp not in (None, ""):
            return FeatureState(version=str(timestamp), mode="timestamp")
        return FeatureState(version=stable_feature_hash(feature), mode="hash")

    def is_changed(self, feature: NormalizedFeature, state: MutableMapping[str, Any]) -> bool:
        """Return True when a feature is new or has a different persisted marker."""
        feature_id = feature["id"]
        current = self.feature_state(feature)
        previous = state.get(feature_id)
        previous_version: Optional[str]
        previous_mode: Optional[str]
        if isinstance(previous, dict):
            previous_version = str(previous.get("version", ""))
            previous_mode = str(previous.get("mode", ""))
        elif previous is not None:
            previous_version = str(previous)
            previous_mode = None
        else:
            previous_version = None
            previous_mode = None
        return previous_version != current.version or (previous_mode not in (None, current.mode))

    def mark_seen(self, feature: NormalizedFeature, state: MutableMapping[str, Any]) -> None:
        """Update state with the current marker for one feature."""
        current = self.feature_state(feature)
        state[feature["id"]] = {"version": current.version, "mode": current.mode}

    def changed_features(
        self,
        features: Iterable[NormalizedFeature],
        state: MutableMapping[str, Any],
        *,
        mark_seen: bool = True,
    ) -> List[NormalizedFeature]:
        """Return features that are new or changed and optionally update state."""
        changed: List[NormalizedFeature] = []
        for feature in features:
            if self.is_changed(feature, state):
                changed.append(feature)
                if mark_seen:
                    self.mark_seen(feature, state)
        return changed


def _get_path(mapping: Dict[str, Any], path: Optional[str]) -> Any:
    if not path:
        return None
    current: Any = mapping
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current
