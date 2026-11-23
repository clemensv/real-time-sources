"""PUBACK tracking for generated publishers sharing one Paho connection."""

import asyncio
from time import monotonic
from typing import Any, Callable


class PublishAcknowledgements:
    def __init__(self, publish: Callable[..., Any]) -> None:
        self._publish = publish
        self.pending: list[Any] = []
        self.outcomes: dict[int, int] = {}

    def publish(self, *args: Any, **kwargs: Any) -> Any:
        info = self._publish(*args, **kwargs)
        if info.rc != 0:
            raise RuntimeError(f"MQTT PUBLISH enqueue failed: {info.rc}")
        self.pending.append(info)
        return info

    def on_publish(self, client: Any, userdata: Any, mid: int,
                   reason_code: Any, properties: Any = None) -> None:
        self.outcomes[mid] = int(getattr(reason_code, "value", reason_code))

    def _confirm(self, pending: list[Any], timeout: float) -> None:
        deadline = monotonic() + timeout
        for info in pending:
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise TimeoutError("MQTT PUBACK timed out; delivery state retained")
            info.wait_for_publish(timeout=remaining)
            if not info.is_published():
                raise TimeoutError("MQTT PUBACK timed out; delivery state retained")
            reason = self.outcomes.pop(info.mid, None)
            if reason is None or reason >= 128:
                raise RuntimeError(f"MQTT PUBACK missing or rejected: {reason}; delivery state retained")

    async def flush_publishes(self, timeout: float = 120) -> None:
        pending, self.pending = self.pending, []
        if pending:
            await asyncio.wait_for(asyncio.to_thread(self._confirm, pending, timeout), timeout)
