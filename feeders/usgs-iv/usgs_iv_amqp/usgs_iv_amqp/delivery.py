"""Remote-accepted settlement for the frozen legacy AMQP producer layout."""

import inspect
from typing import Any, Callable
from urllib.parse import quote

from proton import Message, symbol
from proton.reactor import AtLeastOnce
from proton.utils import BlockingConnection
from usgs_iv_amqp_producer_amqp_producer.producer import (
    USGSSitesAmqpProducer,
    USGSSiteTimeseriesAmqpProducer,
    USGSInstantaneousValuesAmqpProducer,
)


def subject_partitioned(send: Callable[..., Any]) -> Callable[..., Any]:
    # WORKAROUND(xregistry/codegen#294): frozen IV producers predate annotations.
    def publish(message: Message, *args: Any, **kwargs: Any) -> Any:
        subject = message.subject
        if not isinstance(subject, str) or not subject or len(subject) > 128:
            raise ValueError("AMQP partition identity requires a nonempty subject of at most 128 characters")
        annotations = dict(message.annotations or {})
        annotations[symbol("x-opt-partition-key")] = subject
        message.annotations = annotations
        return send(message, *args, **kwargs)
    return publish


# WORKAROUND(xregistry/codegen#699): the older generator opens its blocking
# sender inline; initialize password connections here with explicit settlement
# and SASL policy. CBS initialization remains generated.
class ConfirmedSender:
    host: str
    port: int
    address: str
    username: str | None
    password: str | None
    _use_tls: bool
    _cbs_enabled: bool
    _connection: Any
    _sender: Any

    def _build_connection_url(self) -> str:
        scheme = "amqps" if self._use_tls else "amqp"
        auth = ""
        if self.username is not None or self.password is not None:
            auth = f"{quote(self.username or '', safe='')}:{quote(self.password or '', safe='')}@"
        return f"{scheme}://{auth}{self.host}:{self.port}"

    def _initialize(self, generated_init: Callable[..., None], *args: Any, **kwargs: Any) -> None:
        bound = inspect.signature(generated_init).bind(*args, **kwargs)
        bound.apply_defaults()
        config = bound.arguments
        if config["credential"] is not None or config["sas_key_name"] or config["sas_key"]:
            generated_init(*args, **kwargs)
            send = getattr(self, "_send_via_reactor")
            setattr(self, "_send_via_reactor", subject_partitioned(send))
            return
        for field in ("host", "port", "address", "username", "password", "content_mode", "format_type"):
            setattr(self, field, config[field])
        self._use_tls = config["use_tls"]
        self._cbs_enabled = False
        self._credential = None
        auth: dict[str, Any] = {}
        if self.username or self.password:
            auth = dict(sasl_enabled=True, allowed_mechs="PLAIN",
                        allow_insecure_mechs=not self._use_tls,
                        user=self.username, password=self.password)
        self._connection = BlockingConnection(self._build_connection_url(), timeout=120, **auth)
        self._sender = self._connection.create_sender(self.address, options=AtLeastOnce())
        self._sender.send = subject_partitioned(self._sender.send)


class ConfirmedSitesProducer(ConfirmedSender, USGSSitesAmqpProducer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._initialize(super().__init__, *args, **kwargs)


class ConfirmedTimeseriesProducer(ConfirmedSender, USGSSiteTimeseriesAmqpProducer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._initialize(super().__init__, *args, **kwargs)


class ConfirmedValuesProducer(ConfirmedSender, USGSInstantaneousValuesAmqpProducer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._initialize(super().__init__, *args, **kwargs)
