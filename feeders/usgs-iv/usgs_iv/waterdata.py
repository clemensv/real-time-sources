"""Schema-frozen projection of explicitly enrolled Water Data observations."""

from __future__ import annotations

import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import inspect
import logging
import math
import os
from pathlib import Path
import re
from typing import Any

import usgs_iv_producer_data as models
from usgs_waterdata_core.client import WaterDataClient, utc_datetime
from usgs_waterdata_core.compat import CompatibilityError, Enrollment, LEGACY_SOURCE, qualifiers
from usgs_waterdata_core.state import DeliveryState, write_json

logger = logging.getLogger(__name__)


def api_mode() -> str:
    mode = os.getenv("USGS_API_MODE", "legacy").lower()
    if mode not in {"waterdata", "legacy"}:
        raise ValueError("USGS_API_MODE must be waterdata or legacy")
    return mode


class WaterDataFeed:
    def __init__(self, poller: Any) -> None:
        self.poller = poller
        path = os.getenv("USGS_ENROLLMENT_FILE")
        if not path:
            raise CompatibilityError(
                "USGS_ENROLLMENT_FILE is required for waterdata mode. Capture and review "
                "legacy identities, then select an explicit enrollment; use USGS_API_MODE=legacy "
                "only for temporary rollback before WaterServices retirement."
            )
        self.enrollment = Enrollment.load(Path(path))
        sites = os.getenv("USGS_SITES", "")
        parameters = os.getenv("USGS_PARAMETERS", "")
        if not sites or not parameters:
            raise CompatibilityError("Set explicit USGS_SITES and USGS_PARAMETERS covered by enrollment")
        self.locations = [s if "-" in s else f"USGS-{s}" for s in sites.split(",")]
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
                        "the mapping or select the native usgs-waterdata feeder. Nothing was sent."
                    )
        state_path = os.getenv("USGS_STATE_FILE") or os.getenv("STATE_FILE")
        if not state_path and poller.last_polled_file:
            state_path = poller.last_polled_file + ".waterdata"
        self.state = DeliveryState(Path(state_path) if state_path else None)

    def site(self, location: str) -> Any:
        fields = self.enrollment.site(location)
        numeric = {
            "dec_lat_va", "dec_long_va", "map_scale_fc", "alt_va", "alt_acy_va",
            "drain_area_va", "contrib_drain_area_va", "well_depth_va", "hole_depth_va",
        }
        for key in numeric:
            fields[key] = float(fields[key]) if fields.get(key) not in (None, "") else None
        fields["local_time_fg"] = fields["local_time_fg"] in ("Y", "y", True)
        return models.Site(**fields)

    def project(self, feature: dict[str, Any]) -> tuple[str, Any, dict[str, Any]]:
        properties = feature["properties"]
        entry = self.enrollment.mapping(properties)
        if properties["time_series_id"] not in self.entries:
            raise CompatibilityError(f"Unexpected series outside enrollment selection: {properties['time_series_id']}")
        record = self.enrollment.iv_record(properties)
        parameter = entry["parameter_cd"]
        name = self.poller.PARAMETERS.get(parameter, "OtherParameter")
        model_name = {"pH": "PH", "fDOM": "FDOM"}.get(name, name)
        model = getattr(models, model_name, models.OtherParameter)
        raw = properties["value"]
        fields = dict(
            site_no=entry["site_no"], datetime=record["datetime"],
            parameter_cd=parameter, timeseries_cd=entry["timeseries_cd"],
        )
        if name == "EquipmentStatus":
            fields["status"] = raw
        else:
            try:
                value = float(raw)
                if not math.isfinite(value):
                    raise ValueError("nonfinite")
                fields.update(value=value, exception=None)
            except ValueError:
                fields.update(value=None, exception=raw)
            fields["qualifiers"] = qualifiers(properties, entry.get("qualifier_codes", {}))
        snake = re.sub(r"(?<!^)(?=[A-Z][a-z])", "_", name).lower()
        if name == "pH":
            snake = "p_h"
        if name == "FDOM":
            snake = "fdom"
        return f"send_usgs_instantaneous_values_{snake}", model(**fields), entry

    async def flush(self) -> None:
        seen: set[int] = set()
        for producer in (self.poller.site_producer, self.poller.timeseries_producer, self.poller.values_producer):
            raw = producer.producer
            if id(raw) in seen:
                continue
            seen.add(id(raw))
            result = raw.flush(timeout=120) if not inspect.iscoroutinefunction(raw.flush) else raw.flush()
            if inspect.isawaitable(result):
                result = await result
            if result not in (None, 0):
                raise RuntimeError(f"Broker flush left {result} messages; state retained")

    async def cycle(self, client: WaterDataClient, end: datetime) -> int:
        cursor = self.state.data.get("cursor")
        if cursor:
            start = utc_datetime(cursor)
        else:
            baseline = os.getenv("USGS_REPLAY_START") or self.enrollment.document.get("baseline")
            if not baseline:
                raise CompatibilityError("Enrollment requires baseline or explicit USGS_REPLAY_START")
            start = utc_datetime(baseline)
        if start >= end:
            raise CompatibilityError("USGS replay/checkpoint start must precede the current time")
        end = min(end, start + timedelta(hours=2))
        # A fixed update-time window includes corrections to observations older than the initial baseline.
        features = list(await asyncio.to_thread(
            lambda: list(client.changes(
                start, end, location_ids=",".join(self.locations),
                parameter_codes=",".join(self.parameters),
            ))
        ))
        projected = {id(feature): self.project(feature) for feature in features}
        pending = DeliveryState()
        pending.data = deepcopy(self.state.data)
        selected: list[dict[str, Any]] = []
        pending.deliver(features, selected.append, lambda: 0)
        for index, location in enumerate(self.locations, 1):
            site = self.site(location)
            self.poller.site_producer.send_usgs_sites_site(
                _source_uri=LEGACY_SOURCE, _agency_cd=site.agency_cd, _site_no=site.site_no,
                data=site, flush_producer=False,
            )
            if index % 100 == 0:
                await self.flush()
        for index, entry in enumerate(self.entries.values(), 1):
            self.poller.timeseries_producer.send_usgs_sites_site_timeseries(
                _source_uri=LEGACY_SOURCE, _agency_cd=entry["agency_cd"], _site_no=entry["site_no"],
                _parameter_cd=entry["parameter_cd"], _timeseries_cd=entry["timeseries_cd"],
                data=models.SiteTimeseries(
                    agency_cd=entry["agency_cd"], site_no=entry["site_no"],
                    parameter_cd=entry["parameter_cd"], timeseries_cd=entry["timeseries_cd"],
                    description=entry["parameter_name"],
                ), flush_producer=False,
            )
            if index % 100 == 0:
                await self.flush()
        await self.flush()
        for feature in selected:
            method, data, entry = projected[id(feature)]
            getattr(self.poller.values_producer, method)(
                _source_uri=LEGACY_SOURCE, _agency_cd=entry["agency_cd"], _site_no=entry["site_no"],
                _parameter_cd=entry["parameter_cd"], _timeseries_cd=entry["timeseries_cd"],
                _time=data.datetime, data=data, flush_producer=False,
            )
        await self.flush()
        pending.data["cursor"] = end.isoformat()
        if self.state.path:
            write_json(self.state.path, pending.data)
        self.state.data = pending.data
        return len(selected)

    async def run(self) -> None:
        logger.info("USGS IV waterdata acquisition; historical metadata, %d reviewed series", len(self.entries))
        with WaterDataClient() as client:
            while True:
                now = datetime.now(timezone.utc)
                count = await self.cycle(client, now)
                logger.info("Delivered %d changed IV observations", count)
                if self.poller.once:
                    return
                if utc_datetime(self.state.data["cursor"]) < now:
                    continue
                await asyncio.sleep(float(os.getenv("POLLING_INTERVAL", "300")))
