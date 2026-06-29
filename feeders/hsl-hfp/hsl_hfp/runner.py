"""Reference-first orchestration shared by all three transport apps.

The Kafka, MQTT, and AMQP apps differ only in *how* a normalized record is
turned into a CloudEvent on the wire -- which generated producer class and send
method they call. Everything else (emit operators + GTFS routes/stops first,
then stream telemetry, periodically refresh reference data, dispatch each HFP
event type to the right schema mapper) is identical and lives here.

Each app supplies a :class:`Sink` implementation that owns its producer and
knows how to construct its own producer-package data classes; the runner drives
it.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Dict, Optional, Protocol

from .config import HFP_FEED_URL, FeedConfig
from .hfp_gtfs import GtfsStatic
from .hfp_source import HfpSource
from .mapping import (
    DRIVER_BLOCK_EVENTS,
    TRAFFIC_LIGHT_EVENTS,
    VEHICLE_EVENTS,
    driver_block_event_kwargs,
    operator_kwargs,
    route_kwargs,
    stop_kwargs,
    traffic_light_event_kwargs,
    vehicle_event_kwargs,
)
from .operators import iter_operators

logger = logging.getLogger(__name__)


class Sink(Protocol):
    """Transport-specific emission surface implemented by each app."""

    def send_operator(self, operator_id: str, kwargs: Dict[str, Any]) -> None: ...

    def send_route(self, route_id: str, kwargs: Dict[str, Any]) -> None: ...

    def send_stop(self, stop_id: str, kwargs: Dict[str, Any]) -> None: ...

    def send_vehicle(self, event_type: str, params: Dict[str, str],
                     kwargs: Dict[str, Any]) -> None: ...

    def send_traffic_light(self, event_type: str, params: Dict[str, str],
                           kwargs: Dict[str, Any]) -> None: ...

    def send_driver_block(self, event_type: str, params: Dict[str, str],
                          kwargs: Dict[str, Any]) -> None: ...

    def flush(self) -> None: ...

    def poll(self) -> None: ...


class BridgeRunner:
    """Drives reference-first emission and the telemetry stream against a Sink."""

    def __init__(self, config: FeedConfig, feed_url: str = HFP_FEED_URL,
                 poll_every: int = 200) -> None:
        self.config = config
        self.feed_url = feed_url
        self.poll_every = poll_every
        self._dispatched = 0
        self._refresh_stop = threading.Event()
        self._refresh_thread: Optional[threading.Thread] = None

    # -- reference data -----------------------------------------------------

    def emit_reference(self, sink: Sink) -> int:
        """Emit operators (always) and GTFS routes/stops (unless disabled)."""
        count = 0
        for operator_id, operator_number, name, note in iter_operators():
            sink.send_operator(operator_id, operator_kwargs(operator_id, operator_number, name, note))
            count += 1
        if not self.config.skip_reference:
            try:
                snapshot = GtfsStatic(self.config.gtfs_url).fetch()
                for row in snapshot.routes:
                    rid = row.get("route_id")
                    if rid:
                        sink.send_route(str(rid), route_kwargs(row))
                        count += 1
                for row in snapshot.stops:
                    sid = row.get("stop_id")
                    if sid:
                        sink.send_stop(str(sid), stop_kwargs(row))
                        count += 1
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("GTFS-static reference fetch failed: %s", exc)
        sink.flush()
        logger.info("Emitted %d reference events", count)
        return count

    def _refresh_loop(self, sink: Sink) -> None:
        interval = self.config.reference_refresh_interval
        while not self._refresh_stop.wait(interval):
            logger.info("Refreshing reference data ...")
            try:
                self.emit_reference(sink)
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Reference refresh failed: %s", exc)

    # -- telemetry ----------------------------------------------------------

    def _dispatch(self, sink: Sink, event_type: str, params: Dict[str, str],
                  payload: Dict[str, Any]) -> None:
        operator_id = params.get("operator_id")
        vehicle_number = params.get("vehicle_number")
        if not operator_id or not vehicle_number:
            return
        if event_type in VEHICLE_EVENTS:
            sink.send_vehicle(event_type, params, vehicle_event_kwargs(payload, params))
        elif event_type in TRAFFIC_LIGHT_EVENTS:
            sink.send_traffic_light(event_type, params, traffic_light_event_kwargs(payload, params))
        elif event_type in DRIVER_BLOCK_EVENTS:
            sink.send_driver_block(event_type, params, driver_block_event_kwargs(payload, params))
        else:
            return
        self._dispatched += 1
        if self._dispatched % self.poll_every == 0:
            sink.poll()

    def run(self, sink: Sink) -> None:
        """Emit reference data, then stream telemetry until stopped."""
        self.emit_reference(sink)

        once = self.config.once
        if not once and self.config.reference_refresh_interval > 0:
            self._refresh_thread = threading.Thread(
                target=self._refresh_loop, args=(sink,), daemon=True, name="hfp-reference-refresh")
            self._refresh_thread.start()

        source = HfpSource(
            host=self.config.upstream_host,
            port=self.config.upstream_port,
            topic_filters=self.config.topic_filters,
            tls=self.config.upstream_tls,
        )

        def _callback(event_type: str, params: Dict[str, str], payload: Dict[str, Any],
                      topic: str) -> None:
            try:
                self._dispatch(sink, event_type, params, payload)
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Failed to dispatch %s: %s", topic, exc)

        max_messages = self._once_max_messages() if once else None
        max_seconds = self._once_max_seconds() if once else None
        try:
            delivered = source.stream(_callback, max_messages=max_messages, max_seconds=max_seconds)
            logger.info("Telemetry stream ended after %d upstream messages", delivered)
        finally:
            self._refresh_stop.set()
            sink.flush()

    @staticmethod
    def _once_max_messages() -> int:
        import os
        return int(os.getenv("ONCE_MAX_EVENTS", "50"))

    @staticmethod
    def _once_max_seconds() -> float:
        import os
        return float(os.getenv("ONCE_MAX_SECONDS", "60"))
