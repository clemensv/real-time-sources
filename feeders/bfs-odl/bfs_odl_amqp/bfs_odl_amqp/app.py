"""AMQP feeder application for BfS ODL → Unified Namespace.

Reuses the upstream HTTP client logic from the existing ``bfs_odl`` Kafka
bridge and pushes CloudEvents into AMQP 5.0 using the xrcg-generated
:class:`DeBfsOdlMqttMqttClient`.

Topic tree: ``radiation/de/bfs/bfs-odl/{state}/{station_id}/{info|dose-rate}``.
``{state}`` is derived from the first two digits of the station Kennziffer
(AGS Bundesland code) and normalized to a lowercase kebab-case slug.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse


from bfs_odl.bfs_odl import BfsOdlAPI, _load_state, _save_state, FEED_URL
from bfs_odl_amqp_producer_data import Station, DoseRateMeasurement

# AGS first-two-digit code → Bundesland name
_AGS_TO_STATE: Dict[str, str] = {
    "01": "schleswig-holstein",
    "02": "hamburg",
    "03": "niedersachsen",
    "04": "bremen",
    "05": "nordrhein-westfalen",
    "06": "hessen",
    "07": "rheinland-pfalz",
    "08": "baden-wuerttemberg",
    "09": "bayern",
    "10": "saarland",
    "11": "berlin",
    "12": "brandenburg",
    "13": "mecklenburg-vorpommern",
    "14": "sachsen",
    "15": "sachsen-anhalt",
    "16": "thueringen",
}

_UNS_REPLACEMENTS = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss",
})

from bfs_odl_amqp_producer_amqp_producer.producer import DeBfsOdlAmqpProducer

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
class _AmqpPublishFacade:
    def __init__(self, producers): self._producers=list(producers)
    def close(self):
        for p in self._producers:
            c=getattr(p,"close",None)
            if c: c()
    def __getattr__(self,name):
        if not name.startswith("publish_"): raise AttributeError(name)
        suffix=name.split("_mqtt_",1)[1] if "_mqtt_" in name else name[len("publish_"):]
        target=None
        parts=suffix.split('_')
        for start in range(len(parts)):
            send_name='send_'+'_'.join(parts[start:])
            for p in self._producers:
                target=getattr(p,send_name,None)
                if target: break
            if target: break
        if target is None: raise AttributeError("send_"+suffix)
        async def _publish(**kwargs):
            accepted=set(target.__code__.co_varnames[:target.__code__.co_argcount])
            call={}
            for k,v in kwargs.items():
                if k in ("data","content_type"): call[k]=v
                elif k in ("flush_producer","qos","retain"): continue
                else:
                    candidate="_"+k.lstrip("_")
                    if candidate in accepted: call[candidate]=v
            target(**call)
        return _publish
def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            import logging; logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def _build_publisher(*, host, port, address, use_tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key):
    out=[]
    for cls in (DeBfsOdlAmqpProducer,):
        if auth_mode=="entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            cred=ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
            obj=cls(host=host,address=address,port=port,content_mode=content_mode,credential=cred,entra_audience=entra_audience,use_tls=use_tls)
        elif auth_mode=="sas":
            obj=cls(host=host,address=address,port=port,content_mode=content_mode,sas_key_name=sas_key_name,sas_key=sas_key,use_tls=use_tls)
        else:
            obj=cls(host=host,address=address,port=port,username=username,password=password,content_mode=content_mode,use_tls=use_tls)
        out.append(obj)
    return _AmqpPublishFacade(out)


def _uns_slug(value: str) -> str:
    """Normalize an arbitrary upstream label to a UNS-safe lowercase kebab segment."""
    if not value:
        return "unknown"
    raw = value.translate(_UNS_REPLACEMENTS).lower().strip()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in ("-", "_"):
            out.append(ch)
        else:
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


def _state_from_station_id(station_id: str) -> str:
    """Derive the Bundesland slug from a BfS station Kennziffer (AGS prefix)."""
    prefix = station_id[:2] if len(station_id) >= 2 else ""
    return _AGS_TO_STATE.get(prefix, "unknown")


def _build_station(feature: Dict[str, Any], state: str) -> Station:
    """Build AMQP Station dataclass from a WFS GeoJSON feature."""
    props = feature["properties"]
    geom = feature.get("geometry") or {}
    coords = geom.get("coordinates", [None, None])
    return Station(
        station_id=props["kenn"],
        state=state,
        station_code=props.get("id", ""),
        name=props.get("name", ""),
        postal_code=props.get("plz", ""),
        site_status=props.get("site_status", 0),
        site_status_text=props.get("site_status_text", ""),
        kid=props.get("kid", 0),
        height_above_sea=props.get("height_above_sea"),
        longitude=coords[0] if coords[0] is not None else 0.0,
        latitude=coords[1] if coords[1] is not None else 0.0,
    )


def _build_measurement(feature: Dict[str, Any], state: str) -> DoseRateMeasurement:
    """Build AMQP DoseRateMeasurement dataclass from a WFS GeoJSON feature."""
    props = feature["properties"]
    return DoseRateMeasurement(
        station_id=props["kenn"],
        state=state,
        start_measure=props.get("start_measure", ""),
        end_measure=props.get("end_measure", ""),
        value=props.get("value"),
        value_cosmic=props.get("value_cosmic"),
        value_terrestrial=props.get("value_terrestrial"),
        validated=props.get("validated", 0),
        nuclide=props.get("nuclide", ""),
    )


async def _publish_stations(
    mqtt_client: DeBfsOdlMqttMqttClient,
    stations: list,
) -> None:
    for feature in stations:
        props = feature.get("properties", {})
        station_id = props.get("kenn", "")
        state = _state_from_station_id(station_id)
        try:
            await mqtt_client.publish_de_bfs_odl_mqtt_station(
                feedurl=FEED_URL,
                station_id=station_id,
                state=state,
                data=_build_station(feature, state),
            )
        except Exception as exc:
            logger.error("Error publishing station %s: %s", station_id, exc)


async def _publish_measurements(
    mqtt_client: DeBfsOdlMqttMqttClient,
    measurements: list,
    previous_readings: Dict[str, str],
) -> int:
    sent = 0
    for feature in measurements:
        props = feature.get("properties", {})
        station_id = props.get("kenn", "")
        end_measure = props.get("end_measure", "")
        if station_id in previous_readings and previous_readings[station_id] == end_measure:
            continue
        state = _state_from_station_id(station_id)
        try:
            await mqtt_client.publish_de_bfs_odl_mqtt_dose_rate_measurement(
                feedurl=FEED_URL,
                station_id=station_id,
                state=state,
                data=_build_measurement(feature, state),
            )
            sent += 1
            previous_readings[station_id] = end_measure
        except Exception as exc:
            logger.error("Error publishing measurement for %s: %s", station_id, exc)
    return sent


async def feed(
    api: BfsOdlAPI,
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    previous_readings = _load_state(state_file)

    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "bfs-odl"),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )

    stations = api.fetch_stations()
    logger.info("Publishing %d station info events under radiation/de/bfs/bfs-odl/...", len(stations))
    await _publish_stations(mqtt_client, stations)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                measurements = api.fetch_latest_measurements()
                count = await _publish_measurements(mqtt_client, measurements, previous_readings)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %d dose-rate measurements in %.1fs. Sleeping until %s.",
                    count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:
                logger.error("Error during polling cycle: %s", exc)
                if once:
                    break
                await asyncio.sleep(polling_interval)
    finally:
        mqtt_client.close()


def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BfS ODL → AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and dose-rate as CloudEvents to AMQP")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("AMQP_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "3600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.bfs_odl_mqtt_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

    if args.broker_url:
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (5671 if tls else 5672)
        username = args.username
        password = args.password

    api = BfsOdlAPI()
    asyncio.run(
        feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
        )
    )


if __name__ == "__main__":
    main()