"""AMQP 1.0 feeder application for CelesTrak.

Wraps the upstream poller from :mod:`celestrak_core` and the generated
:class:`OrgCelestrakAmqpProducer`. Supports two deployment modes, chosen at
runtime:

* **Generic AMQP 1.0** (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid
  Dispatch, ...): SASL PLAIN with ``--username``/``--password`` against
  ``amqp://`` (port 5672) or ``amqps://`` (port 5671).
* **Azure Service Bus / Event Hubs** with Entra ID: pass ``--auth-mode entra``
  and ``DefaultAzureCredential`` is used to acquire a JWT, which the generated
  producer presents via the AMQP CBS ``$cbs`` link (``put-token``). No SAS-key
  minting, no refresh loop in this process -- the generated handler owns the
  connection lifecycle.

Reference data (the SATCAT catalog) is emitted first and refreshed
periodically; General Perturbations (GP) orbital element sets follow as
telemetry, deduplicated on their ``EPOCH``. Optional Supplemental GP (SupGP)
sources are emitted only when ``SUPGP_SOURCES`` is set. All events are written
to a single AMQP address (queue or topic), set via ``--address`` /
``AMQP_ADDRESS``. CloudEvent type, source, and subject metadata are carried as
AMQP message properties (binary mode) or in the JSON body (structured mode).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from celestrak_core import (
    GP_URL,
    SATCAT_URL,
    SUPGP_URL,
    CelesTrakAPI,
    FeedConfig,
    load_state,
    save_state,
)
from celestrak_amqp_producer_data.org.celestrak.orbitmeanelements import OrbitMeanElements
from celestrak_amqp_producer_data.org.celestrak.satellitecatalogentry import SatelliteCatalogEntry
from celestrak_amqp_producer_data.org.celestrak.supplementalorbitmeanelements import (
    SupplementalOrbitMeanElements,
)
from celestrak_amqp_producer_amqp_producer.producer import OrgCelestrakAmqpProducer

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

logger = logging.getLogger(__name__)


def _opt_str(raw: Dict[str, Any], key: str) -> Optional[str]:
    value = raw.get(key)
    return value if value not in (None, "") else None


def _opt_float(raw: Dict[str, Any], key: str) -> Optional[float]:
    value = raw.get(key)
    if value is None or value == "":
        return None
    return float(value)


def _opt_int(raw: Dict[str, Any], key: str) -> Optional[int]:
    value = raw.get(key)
    if value is None or value == "":
        return None
    return int(value)


def _parse_epoch(value: str) -> datetime:
    """Return a tz-aware UTC datetime for a CelesTrak EPOCH.

    CelesTrak/CCSDS orbital epochs are always UTC, but the upstream JSON omits the
    timezone designator (e.g. ``2026-07-15T18:23:37.536288``). Attaching UTC makes
    the serialized value RFC3339-compliant (``...+00:00``) as required by the
    JsonStructure ``datetime`` type.
    """
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _build_satcat(raw: Dict[str, Any]) -> SatelliteCatalogEntry:
    return SatelliteCatalogEntry(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        OBJECT_TYPE=_opt_str(raw, "OBJECT_TYPE"),
        OPS_STATUS_CODE=_opt_str(raw, "OPS_STATUS_CODE"),
        OWNER=_opt_str(raw, "OWNER"),
        LAUNCH_DATE=_opt_str(raw, "LAUNCH_DATE"),
        LAUNCH_SITE=_opt_str(raw, "LAUNCH_SITE"),
        DECAY_DATE=_opt_str(raw, "DECAY_DATE"),
        PERIOD=_opt_float(raw, "PERIOD"),
        INCLINATION=_opt_float(raw, "INCLINATION"),
        APOGEE=_opt_int(raw, "APOGEE"),
        PERIGEE=_opt_int(raw, "PERIGEE"),
        RCS=_opt_float(raw, "RCS"),
        DATA_STATUS_CODE=_opt_str(raw, "DATA_STATUS_CODE"),
        ORBIT_CENTER=_opt_str(raw, "ORBIT_CENTER"),
        ORBIT_TYPE=_opt_str(raw, "ORBIT_TYPE"),
    )


def _build_gp(raw: Dict[str, Any]) -> OrbitMeanElements:
    return OrbitMeanElements(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        EPOCH=_parse_epoch(raw["EPOCH"]),
        MEAN_MOTION=float(raw["MEAN_MOTION"]),
        ECCENTRICITY=float(raw["ECCENTRICITY"]),
        INCLINATION=float(raw["INCLINATION"]),
        RA_OF_ASC_NODE=float(raw["RA_OF_ASC_NODE"]),
        ARG_OF_PERICENTER=float(raw["ARG_OF_PERICENTER"]),
        MEAN_ANOMALY=float(raw["MEAN_ANOMALY"]),
        EPHEMERIS_TYPE=int(raw["EPHEMERIS_TYPE"]),
        CLASSIFICATION_TYPE=raw["CLASSIFICATION_TYPE"],
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        ELEMENT_SET_NO=int(raw["ELEMENT_SET_NO"]),
        REV_AT_EPOCH=int(raw["REV_AT_EPOCH"]),
        BSTAR=float(raw["BSTAR"]),
        MEAN_MOTION_DOT=float(raw["MEAN_MOTION_DOT"]),
        MEAN_MOTION_DDOT=float(raw["MEAN_MOTION_DDOT"]),
    )


def _build_supgp(raw: Dict[str, Any]) -> SupplementalOrbitMeanElements:
    return SupplementalOrbitMeanElements(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        EPOCH=_parse_epoch(raw["EPOCH"]),
        MEAN_MOTION=float(raw["MEAN_MOTION"]),
        ECCENTRICITY=float(raw["ECCENTRICITY"]),
        INCLINATION=float(raw["INCLINATION"]),
        RA_OF_ASC_NODE=float(raw["RA_OF_ASC_NODE"]),
        ARG_OF_PERICENTER=float(raw["ARG_OF_PERICENTER"]),
        MEAN_ANOMALY=float(raw["MEAN_ANOMALY"]),
        EPHEMERIS_TYPE=int(raw["EPHEMERIS_TYPE"]),
        CLASSIFICATION_TYPE=raw["CLASSIFICATION_TYPE"],
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        ELEMENT_SET_NO=int(raw["ELEMENT_SET_NO"]),
        REV_AT_EPOCH=int(raw["REV_AT_EPOCH"]),
        BSTAR=float(raw["BSTAR"]),
        MEAN_MOTION_DOT=float(raw["MEAN_MOTION_DOT"]),
        MEAN_MOTION_DDOT=float(raw["MEAN_MOTION_DDOT"]),
        RMS=_opt_float(raw, "RMS"),
        DATA_SOURCE=_opt_str(raw, "DATA_SOURCE"),
    )


def _satcat_source(norad: int) -> str:
    return f"{SATCAT_URL}?CATNR={norad}&FORMAT=json"


def _gp_source(norad: int) -> str:
    return f"{GP_URL}?CATNR={norad}&FORMAT=json"


def _supgp_source(norad: int) -> str:
    return f"{SUPGP_URL}?CATNR={norad}&FORMAT=json"


def _emit_reference(
    api: CelesTrakAPI,
    producer: OrgCelestrakAmqpProducer,
    cfg: FeedConfig,
) -> int:
    satcat = api.get_satcat(cfg.groups)
    count = 0
    for row in satcat:
        norad = int(row["NORAD_CAT_ID"])
        try:
            producer.send_satellite_catalog_entry(
                data=_build_satcat(row),
                _feedurl=_satcat_source(norad),
                _norad_cat_id=str(norad),
            )
            count += 1
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error sending SATCAT record %s: %s", norad, e)
    logger.info("Emitted %d SATCAT reference records", count)
    return count


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                            attempt + 1, max_attempts, e, delay)
            time.sleep(delay)


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
) -> OrgCelestrakAmqpProducer:
    if auth_mode == "entra":
        try:
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "auth-mode=entra requires azure-identity. Reinstall the package."
            ) from exc

        if entra_client_id:
            credential = ManagedIdentityCredential(client_id=entra_client_id)
        else:
            credential = DefaultAzureCredential()

        logger.info(
            "Using Entra ID auth via CBS (host=%s, address=%s, audience=%s)",
            host, address, entra_audience,
        )
        return OrgCelestrakAmqpProducer(
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
                "auth-mode=sas requires --sas-key-name and --sas-key "
                "(or AMQP_SAS_KEY_NAME / AMQP_SAS_KEY env vars)."
            )
        logger.info(
            "Using SAS auth via CBS (host=%s, address=%s, tls=%s, key_name=%s)",
            host, address, use_tls, sas_key_name,
        )
        return OrgCelestrakAmqpProducer(
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
        host, port, address, use_tls, username or "<anonymous>",
    )
    return OrgCelestrakAmqpProducer(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=content_mode,  # type: ignore[arg-type]
        use_tls=use_tls,
    )


def feed(
    api: CelesTrakAPI,
    producer: OrgCelestrakAmqpProducer,
    cfg: FeedConfig,
) -> None:
    """Emit SATCAT reference data and GP/SupGP telemetry as CloudEvents over AMQP 1.0."""

    state: Dict[str, Any] = load_state(cfg.state_file)
    gp_state: Dict[str, str] = state.get("gp", {})
    supgp_state: Dict[str, str] = state.get("supgp", {})

    logger.info(
        "Starting CelesTrak feed to AMQP (groups=%s, supgp=%s)",
        ",".join(cfg.groups),
        ",".join(cfg.supgp_sources) or "<off>",
    )

    last_reference = 0.0
    try:
        while True:
            try:
                cycle_start = datetime.now(timezone.utc)
                now_mono = time.monotonic()

                if last_reference == 0.0 or (now_mono - last_reference) >= cfg.reference_refresh_interval:
                    _emit_reference(api, producer, cfg)
                    last_reference = now_mono

                gp_count = 0
                for row in api.get_gp(cfg.groups):
                    norad = int(row["NORAD_CAT_ID"])
                    epoch = str(row.get("EPOCH"))
                    if gp_state.get(str(norad)) == epoch:
                        continue
                    try:
                        producer.send_orbit_mean_elements(
                            data=_build_gp(row),
                            _feedurl=_gp_source(norad),
                            _norad_cat_id=str(norad),
                        )
                        gp_state[str(norad)] = epoch
                        gp_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending GP element set %s: %s", norad, e)

                supgp_count = 0
                if cfg.supgp_sources:
                    for row in api.get_supgp(cfg.supgp_sources):
                        norad = int(row["NORAD_CAT_ID"])
                        dedup_key = f"{norad}|{row.get('DATA_SOURCE')}|{row.get('EPOCH')}"
                        if supgp_state.get(dedup_key):
                            continue
                        try:
                            producer.send_supplemental_orbit_mean_elements(
                                data=_build_supgp(row),
                                _feedurl=_supgp_source(norad),
                                _norad_cat_id=str(norad),
                            )
                            supgp_state[dedup_key] = str(row.get("EPOCH"))
                            supgp_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error sending SupGP element set %s: %s", norad, e)

                save_state(cfg.state_file, {"gp": gp_state, "supgp": supgp_state})
                elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
                logger.info(
                    "Sent %d GP + %d SupGP element sets in %.1fs.",
                    gp_count,
                    supgp_count,
                    elapsed,
                )

                if api.halted:
                    backoff = max(cfg.polling_interval, 3600)
                    logger.error(
                        "CelesTrak usage-policy hard stop hit; backing off %ds before retrying.",
                        backoff,
                    )
                    if cfg.once:
                        break
                    time.sleep(backoff)
                    api.reset_halt()
                    continue

                if cfg.once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break

                effective = max(0.0, cfg.polling_interval - elapsed)
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                time.sleep(cfg.polling_interval)
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
    parser = argparse.ArgumentParser(description="CelesTrak -> AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed SATCAT + GP element sets as CloudEvents over AMQP 1.0")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"),
                             help="AMQP broker URL (e.g. amqp://localhost:5672/queue, amqps://ns.servicebus.windows.net:5671/queue)")
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"),
                             help="AMQP broker hostname (alternative to --broker-url)")
    feed_parser.add_argument("--port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None,
                             help="AMQP broker port (default 5672, or 5671 with --tls)")
    feed_parser.add_argument("--address", type=str,
                             default=os.getenv("AMQP_ADDRESS", "celestrak"),
                             help="AMQP address (queue or topic name). Default: celestrak")
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--content-mode", type=str,
                             default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"],
                             help="CloudEvents content mode (default: binary)")
    feed_parser.add_argument("--groups", type=str, default=os.getenv("CELESTRAK_GROUPS"),
                             help="Comma-separated CelesTrak GROUP views (default: stations)")
    feed_parser.add_argument("--supgp-sources", type=str, default=os.getenv("SUPGP_SOURCES"),
                             help="Comma-separated Supplemental GP SOURCE views (default: off)")
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "3600")),
                             help="Telemetry polling interval in seconds (default: 3600)")
    feed_parser.add_argument("--reference-refresh-interval", type=int,
                             default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "86400")),
                             help="SATCAT reference refresh interval in seconds (default: 86400)")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.celestrak_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var).")
    feed_parser.add_argument("--auth-mode", type=str,
                             default=os.getenv("AMQP_AUTH_MODE", "password"),
                             choices=["password", "entra", "sas"],
                             help="Authentication mode: 'password' (default, SASL PLAIN), "
                                  "'entra' (AMQP CBS with Azure Entra ID via DefaultAzureCredential, "
                                  "targets Azure Service Bus / Event Hubs), or 'sas' (AMQP CBS with "
                                  "a Shared Access Signature, for SAS-only namespaces or the Service "
                                  "Bus emulator).")
    feed_parser.add_argument("--entra-audience", type=str,
                             default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
                             help=f"Entra token audience. Default: {DEFAULT_ENTRA_AUDIENCE_SERVICEBUS} "
                                  f"(Service Bus). Use {DEFAULT_ENTRA_AUDIENCE_EVENTHUBS} for Event Hubs.")
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"),
                             help="Optional user-assigned managed identity client id; "
                                  "defaults to DefaultAzureCredential resolution.")
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"),
                             help="SAS policy / key name (e.g. RootManageSharedAccessKey). "
                                  "Required with --auth-mode=sas.")
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"),
                             help="SAS key value (base64) used to sign tokens. "
                                  "Required with --auth-mode=sas.")
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

    groups = [g.strip() for g in args.groups.split(",")] if args.groups else None
    supgp = [s.strip() for s in args.supgp_sources.split(",")] if args.supgp_sources else None
    feed_cfg = FeedConfig.from_env(
        groups=groups,
        supgp_sources=supgp,
        polling_interval=args.polling_interval,
        reference_refresh_interval=args.reference_refresh_interval,
        state_file=args.state_file,
        once=args.once,
    )

    api = CelesTrakAPI()
    producer = _retry_producer_init(lambda: _build_producer(
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
    ))

    feed(api, producer, feed_cfg)


if __name__ == "__main__":
    main()
