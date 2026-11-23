"""Remote-accepted settlement for the frozen generated AMQP producers."""

from typing import Any
from urllib.parse import quote

from proton.reactor import AtLeastOnce
from proton.utils import BlockingConnection
from usgs_nwis_wq_amqp_producer_amqp_producer.producer import (
    USGSWaterQualitySitesAmqpProducer,
    USGSWaterQualityReadingsAmqpProducer,
)


# WORKAROUND(xregistry/codegen#699): password sends must await remote acceptance
# and honor TLS, rather than treating drained local socket buffers as delivery.
class ConfirmedSender:
    host: str
    port: int
    address: str
    username: str | None
    password: str | None
    _use_tls: bool
    _connection: Any
    _sender: Any

    def _build_connection_url(self) -> str:
        scheme = "amqps" if self._use_tls else "amqp"
        auth = ""
        if self.username is not None or self.password is not None:
            auth = f"{quote(self.username or '', safe='')}:{quote(self.password or '', safe='')}@"
        return f"{scheme}://{auth}{self.host}:{self.port}"

    def _init_blocking_sender(self) -> None:
        self._blocking_sender_is_presettled = False
        auth: dict[str, Any] = {}
        if self.username or self.password:
            auth = dict(sasl_enabled=True, allowed_mechs="PLAIN",
                        allow_insecure_mechs=not self._use_tls,
                        user=self.username, password=self.password)
        self._connection = BlockingConnection(self._build_connection_url(), timeout=120, **auth)
        self._sender = self._connection.create_sender(self.address, options=AtLeastOnce())


class ConfirmedSitesProducer(ConfirmedSender, USGSWaterQualitySitesAmqpProducer):
    pass


class ConfirmedReadingsProducer(ConfirmedSender, USGSWaterQualityReadingsAmqpProducer):
    pass
