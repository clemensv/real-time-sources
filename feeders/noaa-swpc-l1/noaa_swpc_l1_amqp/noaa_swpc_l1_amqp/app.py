"""AMQP 1.0 feeder for NOAA SWPC L1 propagated solar wind.

Sends each new row to a single AMQP address (queue or topic), set via
``--address`` / ``AMQP_ADDRESS``. CloudEvent metadata travels in AMQP
message properties (binary content mode).

Supports three deployment modes chosen at runtime:

* **Generic AMQP 1.0** (RabbitMQ, ActiveMQ Artemis, Qpid Dispatch, …):
  SASL PLAIN with ``--username``/``--password``.
* **Azure Service Bus / Event Hubs with Entra ID**: ``--auth-mode entra``;
  ``DefaultAzureCredential`` mints a JWT and the generated producer
  presents it via AMQP CBS put-token.
* **SAS** (Service Bus emulator or SAS-only namespaces):
  ``--auth-mode sas`` with key name + key value.

**Partition-key annotation workaround:**
The xrcg-generated producer does not (as of 0.10.6) emit the
``x-opt-partition-key`` message annotation that Service Bus and Event Hubs
expect to align AMQP-side partitioning with Kafka-side partitioning.
This bridge installs a thin wrapper around the producer's send paths
(both the ``BlockingConnection`` direct-send and the CBS reactor send)
that copies ``amqp_msg.subject`` into a UTF-8 annotation under the
``x-opt-partition-key`` symbol immediately before the message goes on the
wire. Behaviour is identical for SB and EH; non-Azure brokers ignore the
annotation harmlessly. See xrcg issue for upstream tracking.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from urllib.parse import urlparse

from proton import Message as ProtonMessage, symbol  # type: ignore

from noaa_swpc_l1_core import (
    FEED_URL,
    PropagatedSolarWindRow,
    SwpcL1API,
    load_state,
    save_state,
)
from noaa_swpc_l1_amqp_producer_data.gov.noaa.swpc.l1.propagatedsolarwind import (
    PropagatedSolarWind,
)
from noaa_swpc_l1_amqp_producer_data.gov.noaa.swpc.l1.spacecraftenum import (
    SpacecraftEnum,
)
from noaa_swpc_l1_amqp_producer_amqp_producer.producer import (
    GovNoaaSwpcL1AmqpProducer,
)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"
PARTITION_KEY_ANNOTATION = symbol("x-opt-partition-key")

logger = logging.getLogger(__name__)


def _row_to_data(row: PropagatedSolarWindRow) -> PropagatedSolarWind:
    return PropagatedSolarWind(
        spacecraft=SpacecraftEnum(row.spacecraft),
        time_tag=row.time_tag,
        propagated_time_tag=row.propagated_time_tag,
        speed=row.speed,
        density=row.density,
        temperature=row.temperature,
        bx=row.bx,
        by=row.by,
        bz=row.bz,
        bt=row.bt,
        vx=row.vx,
        vy=row.vy,
        vz=row.vz,
    )


def _stamp_partition_key(amqp_msg: ProtonMessage) -> None:
    """Mirror ``amqp_msg.subject`` into the ``x-opt-partition-key`` annotation.

    Service Bus reads this annotation as the PartitionKey; Event Hubs hashes
    it to pick a partition. Together with the Kafka key (also ``{spacecraft}``)
    this keeps partitioning consistent across all three transports.

    The annotation value must be a UTF-8 string. We trust ``subject`` because
    the generated producer sets it to ``{spacecraft}`` per the xreg contract.
    """
    subj = amqp_msg.subject
    if not subj:
        return
    annotations = amqp_msg.annotations or {}
    annotations[PARTITION_KEY_ANNOTATION] = str(subj)
    amqp_msg.annotations = annotations


def _install_partition_key_wrapper(producer: GovNoaaSwpcL1AmqpProducer) -> None:
    """Wrap the producer's send paths so every outgoing message carries the annotation.

    The generated producer has two send paths depending on the auth mode:

    * **BlockingConnection** path (SASL PLAIN / anonymous): writes via
      ``producer._sender.send(amqp_msg)``.
    * **Reactor** path (CBS for SB/EH): writes via
      ``producer._send_via_reactor(amqp_msg)``.

    We wrap both so the bridge does not need to care which mode is active.
    """
    # Reactor path
    if hasattr(producer, "_send_via_reactor"):
        original_reactor = producer._send_via_reactor  # type: ignore[attr-defined]

        def wrapped_reactor(amqp_msg: ProtonMessage, timeout: float = 30.0) -> Any:
            _stamp_partition_key(amqp_msg)
            return original_reactor(amqp_msg, timeout=timeout)

        producer._send_via_reactor = wrapped_reactor  # type: ignore[attr-defined]

    # BlockingConnection path
    sender = getattr(producer, "_sender", None)
    if sender is not None and hasattr(sender, "send"):
        original_send = sender.send

        def wrapped_send(amqp_msg: ProtonMessage, *args: Any, **kwargs: Any) -> Any:
            _stamp_partition_key(amqp_msg)
            return original_send(amqp_msg, *args, **kwargs)

        sender.send = wrapped_send  # type: ignore[assignment]


def _build_producer(
    *,
    host: str,
    port: int,
    address: str,
    use_tls: bool,
    content_mode: str,
    auth_mode: str,
    username: Optional[str],
    password: Optional[str],
    entra_audience: str,
    entra_client_id: Optional[str],
    sas_key_name: Optional[str],
    sas_key: Optional[str],
) -> GovNoaaSwpcL1AmqpProducer:
    if auth_mode == "entra":
        try:
            from azure.identity import (
                DefaultAzureCredential,
                ManagedIdentityCredential,
            )
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "auth-mode=entra requires azure-identity."
            ) from exc

        credential = (
            ManagedIdentityCredential(client_id=entra_client_id)
            if entra_client_id
            else DefaultAzureCredential()
        )
        logger.info(
            "Using Entra ID auth via CBS (host=%s, address=%s, audience=%s)",
            host,
            address,
            entra_audience,
        )
        return GovNoaaSwpcL1AmqpProducer(
            host=host,
            address=address,
            port=port,
            content_mode=content_mode,  # type: ignore[arg-type]
            credential=credential,
            entra_audience=entra_audience,
            use_tls=use_tls,
        )

    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError(
                "auth-mode=sas requires --sas-key-name and --sas-key."
            )
        logger.info(
            "Using SAS auth via CBS (host=%s, address=%s, tls=%s, key_name=%s)",
            host,
            address,
            use_tls,
            sas_key_name,
        )
        return GovNoaaSwpcL1AmqpProducer(
            host=host,
            address=address,
            port=port,
            content_mode=content_mode,  # type: ignore[arg-type]
            sas_key_name=sas_key_name,
            sas_key=sas_key,
            use_tls=use_tls,
        )

    logger.info(
        "Using SASL PLAIN auth (host=%s:%s, address=%s, tls=%s, user=%s)",
        host,
        port,
        address,
        use_tls,
        username or "<anonymous>",
    )
    return GovNoaaSwpcL1AmqpProducer(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=content_mode,  # type: ignore[arg-type]
        use_tls=use_tls,
    )


def feed(
    api: SwpcL1API,
    producer: GovNoaaSwpcL1AmqpProducer,
    *,
    spacecraft: str,
    polling_interval: int,
    state_file: str = "",
    once: bool = False,
    backfill_minutes: int = 5,
) -> None:
    state = load_state(state_file)
    last_seen_iso: Optional[str] = state.get("last_time_tag")
    last_seen: Optional[datetime]
    if last_seen_iso:
        try:
            last_seen = datetime.fromisoformat(last_seen_iso)
        except ValueError:
            last_seen = None
    else:
        last_seen = None
    if last_seen is None:
        last_seen = datetime.now(timezone.utc) - timedelta(minutes=backfill_minutes)
        logger.info(
            "No prior state; starting from %s (last %d minutes)",
            last_seen.isoformat(),
            backfill_minutes,
        )

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                new_rows = list(api.fetch_new_rows(spacecraft, since=last_seen))
                count = 0
                for row in new_rows:
                    try:
                        producer.send_propagated_solar_wind(
                            data=_row_to_data(row),
                            _feedurl=FEED_URL,
                            _spacecraft=row.spacecraft,
                            _time=row.time_tag.isoformat(),
                        )
                        count += 1
                        last_seen = row.time_tag
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending row %s: %s", row.time_tag, e)
                if last_seen is not None:
                    save_state(
                        state_file, {"last_time_tag": last_seen.isoformat()}
                    )
                end_time = datetime.now(timezone.utc)
                effective = max(
                    0,
                    polling_interval - (end_time - start_time).total_seconds(),
                )
                logger.info(
                    "Sent %s rows in %.2fs (last_time_tag=%s). Sleeping %.1fs.",
                    count,
                    (end_time - start_time).total_seconds(),
                    last_seen.isoformat() if last_seen else "<none>",
                    effective,
                )
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Polling error: %s — retrying in %ds", e, polling_interval)
                time.sleep(polling_interval)
    finally:
        try:
            producer.close()
        except Exception:  # pylint: disable=broad-except
            pass


def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NOAA SWPC L1 propagated solar wind → AMQP 1.0 bridge."
    )
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed", help="Feed rows as CloudEvents over AMQP 1.0"
    )
    feed_parser.add_argument(
        "--broker-url",
        type=str,
        default=os.getenv("AMQP_BROKER_URL"),
        help="AMQP broker URL (amqp://host:5672/address or amqps://host:5671/address)",
    )
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("AMQP_PORT", "0")) or None,
    )
    feed_parser.add_argument(
        "--address",
        type=str,
        default=os.getenv("AMQP_ADDRESS", "noaa-swpc-l1"),
        help="AMQP address (queue/topic name). Default: noaa-swpc-l1",
    )
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument(
        "--tls",
        action="store_true",
        default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"),
    )
    feed_parser.add_argument(
        "--content-mode",
        type=str,
        default=os.getenv("AMQP_CONTENT_MODE", "binary"),
        choices=["binary", "structured"],
    )
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument(
        "-i", "--polling-interval", type=int, default=polling_interval_default
    )
    feed_parser.add_argument(
        "--spacecraft",
        type=str,
        default=os.getenv("SPACECRAFT", "dscovr"),
        choices=["dscovr", "ace"],
    )
    feed_parser.add_argument(
        "--backfill-minutes",
        type=int,
        default=int(os.getenv("BACKFILL_MINUTES", "5")),
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv(
            "STATE_FILE", os.path.expanduser("~/.noaa_swpc_l1_state.json")
        ),
    )
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
    )
    feed_parser.add_argument(
        "--auth-mode",
        type=str,
        default=os.getenv("AMQP_AUTH_MODE", "password"),
        choices=["password", "entra", "sas"],
    )
    feed_parser.add_argument(
        "--entra-audience",
        type=str,
        default=os.getenv(
            "AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS
        ),
        help=f"Default: {DEFAULT_ENTRA_AUDIENCE_SERVICEBUS} (Service Bus). "
        f"Use {DEFAULT_ENTRA_AUDIENCE_EVENTHUBS} for Event Hubs.",
    )
    feed_parser.add_argument(
        "--entra-client-id",
        type=str,
        default=os.getenv("AMQP_ENTRA_CLIENT_ID"),
    )
    feed_parser.add_argument(
        "--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME")
    )
    feed_parser.add_argument(
        "--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY")
    )
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password

    if not address:
        parser.error("--address is required (or include it in --broker-url path)")

    api = SwpcL1API()
    producer = _build_producer(
        host=host,
        port=port,
        address=address,
        use_tls=tls,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        username=username,
        password=password,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
    )
    _install_partition_key_wrapper(producer)

    feed(
        api,
        producer,
        spacecraft=args.spacecraft,
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        backfill_minutes=args.backfill_minutes,
    )


if __name__ == "__main__":
    main()
