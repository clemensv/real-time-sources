"""HTTP helpers shared by poller implementations."""

from __future__ import annotations

import gzip
import json
from typing import Any, Dict, Mapping, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_STATUS_FORCELIST = (429, 500, 502, 503, 504)
DEFAULT_TIMEOUT_SECONDS = 60.0


class TimeoutSession(requests.Session):
    """Requests session that applies a default timeout to every request.

    Args:
        default_timeout: Timeout in seconds used when callers do not pass a
            per-request timeout.
    """

    def __init__(self, default_timeout: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        super().__init__()
        self.default_timeout = default_timeout

    def request(self, method: Any, url: Any, **kwargs: Any) -> requests.Response:  # type: ignore[override]
        """Send an HTTP request, inserting the configured default timeout."""
        kwargs.setdefault("timeout", self.default_timeout)
        return super().request(method, url, **kwargs)


def create_retrying_session(
    *,
    user_agent: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    total_retries: int = 3,
    backoff_factor: float = 0.5,
    status_forcelist: tuple[int, ...] = DEFAULT_STATUS_FORCELIST,
    headers: Optional[Mapping[str, str]] = None,
) -> requests.Session:
    """Create a requests session with timeout and exponential-backoff retries.

    Args:
        user_agent: Optional User-Agent header to set on the session.
        timeout: Default timeout in seconds for requests made through the
            returned session.
        total_retries: Maximum retry count for connect/read/status failures.
        backoff_factor: urllib3 retry backoff factor; sleep grows
            exponentially between attempts.
        status_forcelist: HTTP status codes retried for idempotent GET calls.
        headers: Additional headers, for example Authorization tokens.
    """

    session = TimeoutSession(default_timeout=timeout)
    if user_agent:
        session.headers["User-Agent"] = user_agent
    if headers:
        session.headers.update(dict(headers))
    retry = Retry(
        total=total_retries,
        connect=total_retries,
        read=total_retries,
        status=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def response_json(response: requests.Response) -> Dict[str, Any]:
    """Decode a JSON response, including manually supplied gzip fixtures.

    Requests normally decompresses gzip/deflate before exposing content. Tests
    and some bespoke callers may construct Response objects directly, so this
    helper also honors Content-Encoding: gzip when raw compressed bytes remain.
    """

    content = response.content
    if response.headers.get("Content-Encoding", "").lower() == "gzip" and content[:2] == b"\x1f\x8b":
        content = gzip.decompress(content)
    if not content:
        return {}
    parsed = json.loads(content.decode(response.encoding or "utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object response")
    return parsed
