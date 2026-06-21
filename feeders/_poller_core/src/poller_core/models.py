"""Typed data shapes shared by the ArcGIS and GeoJSON pollers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict


class NormalizedFeature(TypedDict):
    """A source-neutral feature shape returned by the shared pollers."""

    id: str
    attributes: Dict[str, Any]
    geometry: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class PollMetadata:
    """Metadata describing one polling pass.

    Args:
        status_code: HTTP status from the first response, or 0 when no request
            was issued.
        not_modified: True when conditional GET returned HTTP 304.
        etag: Latest ETag value returned by the upstream, if any.
        last_modified: Latest Last-Modified value returned by the upstream, if
            any.
        page_count: Number of HTTP pages fetched.
        source_url: First URL requested for this poll.
    """

    status_code: int
    not_modified: bool = False
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    page_count: int = 0
    source_url: str = ""


@dataclass(frozen=True)
class PollResult:
    """Result returned by poller fetch methods.

    Args:
        features: Normalized features keyed by the configured stable id.
        metadata: Poll metadata, including conditional-GET and paging details.
    """

    features: List[NormalizedFeature] = field(default_factory=list)
    metadata: PollMetadata = field(default_factory=lambda: PollMetadata(status_code=0))
