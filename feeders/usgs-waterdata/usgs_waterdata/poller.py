"""Shared native acquisition, reference ordering and delivery checkpoints."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Protocol

from usgs_waterdata_core.client import WaterDataClient, utc_datetime
from usgs_waterdata_core.state import DeliveryState, fingerprint, observation_key

logger = logging.getLogger(__name__)


class Sink(Protocol):
    async def send(self, family: str, series_id: str, payload: dict[str, Any]) -> None: ...
    async def flush(self) -> None: ...


def resource(feature: dict[str, Any]) -> dict[str, Any]:
    return {**feature["properties"], "geometry": feature.get("geometry")}


def series_resource(feature: dict[str, Any]) -> dict[str, Any]:
    payload = resource(feature)
    payload["time_series_id"] = payload.pop("id")
    thresholds = []
    names = {
        "Name": "name", "Type": "type", "Periods": "periods", "Severity": "severity",
        "Description": "description", "DisplayColor": "display_color",
        "ReferenceCode": "reference_code", "ProcessingOrder": "processing_order",
        "StartTime": "start_time", "EndTime": "end_time", "AppliedTime": "applied_time",
        "SuppressData": "suppress_data", "ReferenceValue": "reference_value",
        "SecondaryReferenceValue": "secondary_reference_value", "Comments": "comments",
    }
    for raw in payload.get("thresholds") or []:
        unknown = set(raw) - names.keys()
        if unknown:
            raise ValueError(f"Unmodeled USGS threshold fields: {sorted(unknown)}")
        threshold = {names[key]: value for key, value in raw.items() if key != "Periods"}
        periods = []
        for period in raw.get("Periods", []):
            unknown = set(period) - names.keys()
            if unknown:
                raise ValueError(f"Unmodeled USGS threshold-period fields: {sorted(unknown)}")
            periods.append({names[key]: value for key, value in period.items()})
        threshold["periods"] = periods
        thresholds.append(threshold)
    payload["thresholds"] = thresholds
    return payload


class NativePoller:
    def __init__(
        self, client: WaterDataClient, sink: Sink, state: DeliveryState, *,
        sites: list[str], parameters: str = "", lookback_hours: float = 2,
        reference_interval: float = 86400, overlap_seconds: float = 300,
    ) -> None:
        self.client, self.sink, self.state = client, sink, state
        self.sites, self.parameters = sites, parameters
        self.lookback = timedelta(hours=lookback_hours)
        self.reference_interval = timedelta(seconds=reference_interval)
        self.overlap = timedelta(seconds=overlap_seconds)
        self.catalog: dict[str, dict[str, dict[str, Any]]] = {}
        self.refreshed: dict[str, datetime] = {}

    async def _references(self, site: str, now: datetime) -> None:
        if site in self.catalog and now - self.refreshed[site] < self.reference_interval:
            return
        try:
            location = self.client.item("monitoring-locations", site)
            series = list(self.client.features(
                "time-series-metadata", monitoring_location_id=site,
                **({"parameter_code": self.parameters} if self.parameters else {}),
                computation_identifier="Instantaneous", computation_period_identifier="Points",
            ))
            candidate = {}
            parameters: dict[str, dict[str, Any]] = {}
            for entry in series:
                props = entry["properties"]
                if props.get("computation_identifier") != "Instantaneous" or props.get("computation_period_identifier") != "Points":
                    continue
                parameter_id = props["parameter_code"]
                if parameter_id not in parameters:
                    parameters[parameter_id] = self.client.item("parameter-codes", parameter_id)
                candidate[props["id"]] = {
                    "MonitoringLocation": {"time_series_id": props["id"], "location": resource(location)},
                    "Parameter": {"time_series_id": props["id"], "parameter": resource(parameters[parameter_id])},
                    "TimeSeries": series_resource(entry),
                }
            if not candidate:
                raise RuntimeError(f"No instantaneous series metadata for {site}")
            sent = 0
            for series_id, families in candidate.items():
                for family, payload in families.items():
                    await self.sink.send(family, series_id, payload)
                    sent += 1
                    if sent % 100 == 0:
                        await self.sink.flush()
            await self.sink.flush()
            self.catalog[site] = candidate
            self.refreshed[site] = now
        except Exception:
            if site not in self.catalog:
                raise
            logger.exception("Reference refresh failed for %s; retaining acknowledged catalog", site)

    async def cycle(self, now: datetime | None = None) -> int:
        now = now or datetime.now(timezone.utc)
        emitted, failures = 0, []
        for site in self.sites:
            try:
                await self._references(site, now)
                features = list(self.client.observations(
                    now - self.lookback, now, location_ids=site, parameter_codes=self.parameters))
                modified_until = self.state.data.get("modified_until", {}).get(site)
                if modified_until:
                    features.extend(self.client.changes(
                        utc_datetime(modified_until) - self.overlap, now,
                        location_ids=site, parameter_codes=self.parameters))
                unique = {}
                for feature in features:
                    props = feature["properties"]
                    if props["time_series_id"] not in self.catalog[site]:
                        # Re-discover before emitting a newly appearing series.
                        self.refreshed[site] = datetime.min.replace(tzinfo=timezone.utc)
                        await self._references(site, now)
                    if props["time_series_id"] not in self.catalog[site]:
                        raise RuntimeError(f"No acknowledged references for native series {props['time_series_id']}")
                    unique[observation_key(props)] = feature
                pending = [
                    feature for key, feature in unique.items()
                    if self.state.data["observations"].get(key) != fingerprint(feature["properties"])
                ]
                for index, feature in enumerate(pending, 1):
                    props = feature["properties"]
                    await self.sink.send("ContinuousObservation", props["time_series_id"],
                                         {**resource(feature), "feature_id": str(feature.get("id")) if feature.get("id") is not None else None})
                    if index % 100 == 0:
                        await self.sink.flush()
                await self.sink.flush()
                # DeliveryState owns atomic persistence; publish acknowledgements precede every mutation.
                prior = self.state.data.get("modified_until", {}).copy()
                self.state.data.setdefault("modified_until", {})[site] = now.isoformat()
                try:
                    emitted += self.state.deliver(pending, lambda _: None, lambda: 0)
                except Exception:
                    self.state.data["modified_until"] = prior
                    raise
            except Exception:
                logger.exception("Native USGS polling slice failed for %s", site)
                failures.append(site)
        if failures:
            raise RuntimeError(f"USGS poll failed for sites: {', '.join(failures)}")
        logger.info("USGS native cycle acknowledged %d observations", emitted)
        return emitted

    async def run(self, interval: float, once: bool = False) -> None:
        while True:
            try:
                await self.cycle()
            except Exception:
                if once:
                    raise
                logger.exception("Poll incomplete; failed slices retain their checkpoints")
            if once:
                return
            await asyncio.sleep(interval)
