"""Shared polling primitives for bespoke real-time-sources feeders.

The package intentionally contains no source contract, CloudEvents producer, or
transport application. Feeders import these helpers to fetch ArcGIS
FeatureServer or GeoJSON FeatureCollection payloads, then map the returned
normalized features into their own generated data classes.
"""

from poller_core.arcgis import ArcGisFeatureServerPoller
from poller_core.delta import DeltaDetector, FeatureState, stable_feature_hash
from poller_core.geojson import GeoJsonFeatureCollectionPoller, OffsetLimitPagination
from poller_core.http import create_retrying_session
from poller_core.models import NormalizedFeature, PollMetadata, PollResult
from poller_core.state import JsonFileStateStore

__all__ = [
    "ArcGisFeatureServerPoller",
    "DeltaDetector",
    "FeatureState",
    "GeoJsonFeatureCollectionPoller",
    "JsonFileStateStore",
    "NormalizedFeature",
    "OffsetLimitPagination",
    "PollMetadata",
    "PollResult",
    "create_retrying_session",
    "stable_feature_hash",
]
