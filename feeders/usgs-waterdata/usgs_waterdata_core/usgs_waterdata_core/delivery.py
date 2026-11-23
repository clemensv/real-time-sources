"""Delivery confirmation for generated Kafka producers."""

from typing import Any


class AcknowledgedKafkaProducer:
    def __init__(self, raw: Any) -> None:
        self.raw = raw
        self.pending = 0
        self.errors: list[str] = []

    def produce(self, *args: Any, **kwargs: Any) -> None:
        previous = kwargs.pop("on_delivery", kwargs.pop("callback", None))
        self.pending += 1

        def delivered(error: Any, message: Any) -> None:
            self.pending -= 1
            if error is not None:
                self.errors.append(str(error))
            if previous is not None:
                previous(error, message)

        try:
            self.raw.produce(*args, on_delivery=delivered, **kwargs)
        except Exception:
            self.pending -= 1
            raise

    def flush(self, timeout: float = 120) -> int:
        remaining = self.raw.flush(timeout)
        errors, self.errors = self.errors, []
        if remaining != 0 or self.pending != 0 or errors:
            raise RuntimeError(
                f"Kafka delivery failed: queued={remaining}, callbacks_pending={self.pending}, errors={errors}"
            )
        return 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self.raw, name)
