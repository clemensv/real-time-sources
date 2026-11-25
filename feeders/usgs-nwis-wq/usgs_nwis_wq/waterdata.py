"""Reviewed Water Data acquisition against the unchanged legacy WQ contract."""

from __future__ import annotations

import asyncio
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
import inspect
import json
import logging
import os
from pathlib import Path
from typing import Any, overload

from usgs_nwis_wq_producer_data import MonitoringSite, WaterQualityReading

from usgs_waterdata_core.client import WaterDataClient, utc_datetime
from usgs_waterdata_core.compat import CompatibilityError, Enrollment, LEGACY_SOURCE
from usgs_waterdata_core.state import DeliveryState, write_json

logger = logging.getLogger(__name__)


def api_mode() -> str:
    value = os.getenv("USGS_API_MODE", "legacy").lower()
    if value not in {"waterdata", "legacy"}:
        raise ValueError("USGS_API_MODE must be waterdata or legacy")
    return value


# WORKAROUND(https://github.com/xregistry/codegen/issues/698): generated JSON
# emits null for absent fields that the frozen contract permits only to be omitted.
class FrozenMonitoringSite(MonitoringSite):
    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_serializer_dict(), **kwargs)

    def to_serializer_dict(self) -> dict[str, Any]:
        return {key: value for key, value in super().to_serializer_dict().items() if value is not None}


class FrozenWaterQualityReading(WaterQualityReading):
    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_serializer_dict(), **kwargs)

    def to_serializer_dict(self) -> dict[str, Any]:
        return {key: value for key, value in super().to_serializer_dict().items() if value is not None}


@overload
def frozen_payload(data: MonitoringSite) -> FrozenMonitoringSite: ...


@overload
def frozen_payload(data: WaterQualityReading) -> FrozenWaterQualityReading: ...


def frozen_payload(data: MonitoringSite | WaterQualityReading) -> FrozenMonitoringSite | FrozenWaterQualityReading:
    """Omit absent optional fields without changing the generated data classes."""
    if isinstance(data, (FrozenMonitoringSite, FrozenWaterQualityReading)):
        return data
    fields = asdict(data)
    if isinstance(data, MonitoringSite):
        return FrozenMonitoringSite(**fields)
    return FrozenWaterQualityReading(**fields)


class WaterDataFeed:
    def __init__(self, poller: Any) -> None:
        self.poller = poller
        path = os.getenv("USGS_ENROLLMENT_FILE")
        if not path:
            raise CompatibilityError(
                "USGS_ENROLLMENT_FILE is required. Capture and review legacy identity/metadata, "
                "or set USGS_API_MODE=legacy only for temporary rollback before retirement."
            )
        self.enrollment = Enrollment.load(Path(path))
        sites = os.getenv("USGS_SITES", "")
        parameters = os.getenv("USGS_PARAMETERS") or os.getenv("USGS_WQ_PARAMETER_CODES", "")
        if not sites or not parameters:
            raise CompatibilityError("Set explicit USGS_SITES and USGS_PARAMETERS covered by enrollment")
        self.locations = [site if "-" in site else f"USGS-{site}" for site in sites.split(",")]
        self.parameters = parameters.split(",")
        self.entries = {
            sid: entry for sid, entry in self.enrollment.mappings.items()
            if entry.get("status") == "verified"
            and f"{entry['agency_cd']}-{entry['site_no']}" in self.locations
            and entry["parameter_cd"] in self.parameters
        }
        for location in self.locations:
            for parameter in self.parameters:
                if not any(
                    f"{entry['agency_cd']}-{entry['site_no']}" == location
                    and entry["parameter_cd"] == parameter for entry in self.entries.values()
                ):
                    raise CompatibilityError(
                        f"Enrollment does not cover {location}/{parameter}; capture and review "
                        "its mapping or use the native usgs-waterdata feeder. Nothing was sent."
                    )
            snapshot = self.enrollment.sites[location]
            if not snapshot.get("wq_fields") or not snapshot.get("routing_state"):
                raise CompatibilityError(f"Enrollment lacks reviewed WQ metadata/routing_state: {location}")
        state_path = os.getenv("USGS_STATE_FILE") or os.getenv("STATE_FILE")
        if not state_path and poller.last_polled_file:
            state_path = poller.last_polled_file + ".waterdata"
        self.state = DeliveryState(Path(state_path) if state_path else None)
        self.lookback = timedelta(hours=float(os.getenv("WQ_LOOKBACK_HOURS", "2")))
        if self.lookback.total_seconds() <= 0:
            raise ValueError("WQ_LOOKBACK_HOURS must be positive")

    def project(self, feature: dict[str, Any]) -> Any:
        from .usgs_nwis_wq import WaterQualityReading
        properties = feature["properties"]
        if properties.get("time_series_id") not in self.entries:
            raise CompatibilityError(f"Unenrolled WQ series: {properties.get('time_series_id')!r}")
        return frozen_payload(WaterQualityReading(**self.enrollment.wq_reading(properties)))

    async def flush(self) -> None:
        seen: set[int] = set()
        for producer in (self.poller.site_producer, self.poller.readings_producer):
            raw = producer.producer
            if id(raw) in seen:
                continue
            seen.add(id(raw))
            result = raw.flush() if inspect.iscoroutinefunction(raw.flush) else raw.flush(timeout=120)
            if inspect.isawaitable(result):
                result = await result
            if result not in (0, None):
                raise RuntimeError(f"Broker flush left {result} messages; checkpoint retained")

    async def cycle(self, client: WaterDataClient, now: datetime) -> int:
        from .usgs_nwis_wq import MonitoringSite
        baseline = os.getenv("USGS_REPLAY_START") or self.enrollment.document.get("baseline")
        if not baseline:
            raise CompatibilityError("Enrollment requires baseline or explicit USGS_REPLAY_START")
        start = utc_datetime(self.state.data.get("cursor") or baseline)
        if start >= now:
            raise CompatibilityError("USGS replay/checkpoint start must precede the current time")
        end = min(now, start + timedelta(hours=2))
        features = list(await asyncio.to_thread(lambda: list(client.changes(
            start, end, location_ids=",".join(self.locations), parameter_codes=",".join(self.parameters),
        ))))
        # WQ historically emitted an observation-time window, unlike unrestricted IV corrections.
        eligible = [feature for feature in features if utc_datetime(feature["properties"]["time"]) >= end - self.lookback]
        # Validate even rows outside the WQ window: unknown selected series must never disappear silently.
        projected = {id(feature): self.project(feature) for feature in features}
        pending = deepcopy(self.state)
        pending.path = None
        selected: list[dict[str, Any]] = []
        pending.deliver(eligible, selected.append, lambda: 0, retain_since=end - self.lookback)
        for index, location in enumerate(self.locations, 1):
            fields = deepcopy(self.enrollment.sites[location]["wq_fields"])
            site = frozen_payload(MonitoringSite(**fields))
            self.poller.site_producer.send_usgs_water_quality_sites_monitoring_site(
                _source_uri=LEGACY_SOURCE, _site_number=site.site_number,
                data=site, flush_producer=False,
            )
            if index % 100 == 0:
                await self.flush()
        await self.flush()
        for feature in selected:
            reading = projected[id(feature)]
            self.poller.readings_producer.send_usgs_water_quality_readings_water_quality_reading(
                _source_uri=LEGACY_SOURCE, _site_number=reading.site_number,
                _parameter_code=reading.parameter_code, data=reading, flush_producer=False,
            )
        await self.flush()
        pending.data["cursor"] = end.isoformat()
        if self.state.path:
            write_json(self.state.path, pending.data)
        self.state.data = pending.data
        return len(selected)

    async def run(self, once: bool = False) -> None:
        logger.info("USGS WQ waterdata acquisition; historical metadata, %d reviewed series", len(self.entries))
        with WaterDataClient() as client:
            while True:
                now = datetime.now(timezone.utc)
                count = await self.cycle(client, now)
                logger.info("Delivered %d changed WQ observations", count)
                if once:
                    return
                if utc_datetime(self.state.data["cursor"]) < now:
                    continue
                await asyncio.sleep(self.poller.polling_interval)
