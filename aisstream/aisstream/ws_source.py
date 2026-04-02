"""WebSocket client for AISstream.io with auto-reconnect and exponential backoff."""

import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional

import websockets.sync.client as ws_client

logger = logging.getLogger(__name__)

AISSTREAM_WS_URL = "wss://stream.aisstream.io/v0/stream"


class WebSocketSource:
    """Connects to AISstream.io WebSocket and delivers parsed JSON messages."""

    def __init__(self, api_key: str,
                 bounding_boxes: Optional[List[List[List[float]]]] = None,
                 mmsi_filter: Optional[List[str]] = None,
                 message_type_filter: Optional[List[str]] = None,
                 url: str = AISSTREAM_WS_URL,
                 max_retry_delay: int = 60):
        self.api_key = api_key
        self.bounding_boxes = bounding_boxes or [[[-90, -180], [90, 180]]]
        self.mmsi_filter = mmsi_filter
        self.message_type_filter = message_type_filter
        self.url = url
        self.max_retry_delay = max_retry_delay

    def _build_subscription(self) -> str:
        """Build the JSON subscription message."""
        sub: Dict[str, Any] = {
            "APIKey": self.api_key,
            "BoundingBoxes": self.bounding_boxes,
        }
        if self.mmsi_filter:
            sub["FiltersShipMMSI"] = self.mmsi_filter
        if self.message_type_filter:
            sub["FilterMessageTypes"] = self.message_type_filter
        return json.dumps(sub)

    def stream(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Connect, subscribe, and stream messages to callback.

        Reconnects with exponential backoff on failure. Runs until interrupted.
        """
        retry_delay = 1
        subscription = self._build_subscription()

        while True:
            try:
                logger.info("Connecting to %s ...", self.url)
                conn = ws_client.connect(
                    self.url,
                    additional_headers={"User-Agent": "aisstream-bridge/1.0"},
                    open_timeout=30,
                    close_timeout=10,
                )
                with conn:
                    logger.info("Connected — sending subscription")
                    conn.send(subscription)
                    retry_delay = 1

                    for raw in conn:
                        try:
                            msg = json.loads(raw)
                        except json.JSONDecodeError as e:
                            logger.debug("Invalid JSON from stream: %s", e)
                            continue

                        if "error" in msg:
                            logger.error("AISstream error: %s", msg["error"])
                            raise ConnectionError(f"AISstream error: {msg['error']}")

                        callback(msg)

            except KeyboardInterrupt:
                logger.info("Interrupted — closing connection.")
                break
            except Exception as e:
                logger.warning("Connection error: %s. Reconnecting in %ds...", e, retry_delay)
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, self.max_retry_delay)
