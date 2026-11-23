"""Transport adapters for the frozen WQ producer method names."""

import asyncio
import inspect
import os
from pathlib import Path
from typing import Any

from usgs_waterdata_core.compat import CompatibilityError, Enrollment
from .waterdata import api_mode, frozen_payload


class PublisherAdapter:
    def __init__(self, client: Any, transport: str) -> None:
        self.client = client
        self.transport = transport
        self.producer = self
        self.tasks: list[Any] = []
        path = os.getenv("USGS_ENROLLMENT_FILE")
        self.enrollment = Enrollment.load(Path(path)) if path and api_mode() == "waterdata" else None

    def __getattr__(self, name: str) -> Any:
        if not name.startswith("send_"):
            raise AttributeError(name)
        if self.transport == "mqtt":
            method_name = name.replace("send_", "publish_").replace(
                "_sites_", "_sites_mqtt_"
            ).replace("_readings_", "_readings_mqtt_")
        else:
            method_name = "send_monitoring_site" if name.endswith("_monitoring_site") else "send_water_quality_reading"
        method = getattr(self.client, method_name)

        def send(**kwargs: Any) -> None:
            kwargs.pop("flush_producer", None)
            data = kwargs["data"]
            state = data.state
            if self.enrollment:
                state = self.enrollment.sites[f"USGS-{data.site_number}"]["routing_state"]
            if not state:
                raise CompatibilityError(
                    "MQTT/AMQP routing requires captured routing_state in USGS_ENROLLMENT_FILE "
                    "or a legacy payload state"
                )
            if self.transport == "mqtt":
                call = {key.lstrip("_"): value for key, value in kwargs.items()}
                call["state"] = state
            else:
                call = dict(kwargs, _state=state)
            call["data"] = frozen_payload(data)
            result = method(**call)
            if inspect.isawaitable(result):
                self.tasks.append(asyncio.ensure_future(result))
        return send

    async def flush(self, timeout: float = 120) -> None:
        pending, self.tasks = self.tasks, []
        if pending:
            outcomes = await asyncio.wait_for(asyncio.gather(*pending, return_exceptions=True), timeout)
            failures = [outcome for outcome in outcomes if isinstance(outcome, BaseException)]
            if failures:
                raise RuntimeError("WQ publish failed; delivery state retained") from failures[0]
        if self.transport == "mqtt":
            drain = getattr(getattr(self.client, "client", None), "flush_publishes", None)
            if drain:
                await drain(timeout)
