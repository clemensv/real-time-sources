"""Delivery confirmation for generated Kafka producers."""

import base64
import importlib
import json
import math
import os
import time
from typing import Any, Mapping
from urllib.parse import urlsplit


def fabric_kafka_config(config: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(config)
    mode = os.getenv("KAFKA_AUTH_MODE", "")
    if not mode:
        return result
    if mode != "fabric-entra":
        raise ValueError("KAFKA_AUTH_MODE must be unset or fabric-entra")
    if result.get("security.protocol") not in ("SSL", "SASL_SSL"):
        raise ValueError("Fabric Entra Kafka authentication requires TLS")
    if any(result.get(key) for key in ("sasl.username", "sasl.password")):
        raise ValueError("Fabric Entra Kafka authentication cannot use SASL username/password")
    bootstrap = result.get("bootstrap.servers")
    if not isinstance(bootstrap, str) or "," in bootstrap:
        raise ValueError("Fabric Entra Kafka authentication requires one namespace endpoint")
    endpoint = urlsplit("//" + bootstrap)
    if (not endpoint.hostname or endpoint.port != 9093 or endpoint.username or endpoint.password
            or endpoint.path or endpoint.query or endpoint.fragment):
        raise ValueError("Fabric Entra Kafka authentication requires a namespace endpoint on port 9093")
    audience = f"https://{endpoint.hostname}/"
    notebookutils = importlib.import_module("notebookutils")

    def oauth(_: str) -> tuple[str, float]:
        token = notebookutils.credentials.getToken(audience)
        if not isinstance(token, str) or len(token.split(".")) != 3:
            raise ValueError("NotebookUtils did not return an Event Hubs JWT")
        payload = token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        if not isinstance(claims, dict) or claims.get("aud") not in (audience, audience.rstrip("/")):
            raise ValueError("NotebookUtils token has an unexpected Event Hubs audience")
        expiry = claims.get("exp")
        if isinstance(expiry, bool) or not isinstance(expiry, (int, float)):
            raise ValueError("NotebookUtils token has no numeric expiration")
        if not math.isfinite(expiry) or expiry <= time.time() + 60:
            raise ValueError("NotebookUtils Event Hubs token is expired or expires within 60 seconds")
        # The broker verifies the signature; these checks prevent sending the wrong cached token.
        return token, float(expiry)

    result.pop("sasl.mechanisms", None)
    result.update({"security.protocol": "SASL_SSL", "sasl.mechanism": "OAUTHBEARER", "oauth_cb": oauth})
    return result


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
