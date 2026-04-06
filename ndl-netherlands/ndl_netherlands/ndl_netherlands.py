"""Netherlands NDL EV charging infrastructure bridge."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import importlib
import json
import logging
import os
import sys
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any, Optional

import aiohttp
from confluent_kafka import Producer


BASE_URL = "https://opendata.ndw.nu"
LOCATIONS_FILE = "charging_point_locations_ocpi.json.gz"
TARIFFS_FILE = "charging_point_tariffs_ocpi.json.gz"
DEFAULT_CHARGING_TOPIC = "ndl-charging"
DEFAULT_TARIFFS_TOPIC = "ndl-charging-tariffs"
DEFAULT_POLL_INTERVAL_SECONDS = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.ndl_netherlands_state.json")

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def _parse_optional_float(value: Any) -> Optional[float]:
    if value in (None, "", "undefined"):
        return None
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def _parse_optional_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    return None


def _safe_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _safe_string_list(value: Any) -> Optional[list[str]]:
    if not isinstance(value, list):
        return None
    result = [str(item) for item in value if item is not None and str(item).strip()]
    return result if result else None


def parse_connection_string(connection_string: str) -> dict[str, str]:
    config_dict: dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def normalize_location(raw: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Extract a flat ChargingLocation dict from an OCPI Location object."""
    location_id = raw.get("id")
    if not location_id:
        return None

    coords = raw.get("coordinates") or {}
    lat = _parse_optional_float(coords.get("latitude"))
    lon = _parse_optional_float(coords.get("longitude"))
    if lat is None or lon is None:
        return None

    operator = raw.get("operator") or {}
    suboperator = raw.get("suboperator") or {}
    owner = raw.get("owner") or {}
    energy_mix = raw.get("energy_mix") or {}
    opening_times = raw.get("opening_times") or {}
    evses = raw.get("evses") or []
    connector_count = sum(len(e.get("connectors") or []) for e in evses if isinstance(e, dict))

    return {
        "location_id": str(location_id),
        "country_code": raw.get("country_code", ""),
        "party_id": raw.get("party_id", ""),
        "publish": raw.get("publish", True),
        "name": _safe_string(raw.get("name")),
        "address": raw.get("address", ""),
        "city": raw.get("city", ""),
        "postal_code": _safe_string(raw.get("postal_code")),
        "state": _safe_string(raw.get("state")),
        "country": raw.get("country", ""),
        "latitude": lat,
        "longitude": lon,
        "parking_type": _safe_string(raw.get("parking_type")),
        "operator_name": _safe_string(operator.get("name")),
        "operator_website": _safe_string(operator.get("website")),
        "suboperator_name": _safe_string(suboperator.get("name")),
        "owner_name": _safe_string(owner.get("name")),
        "facilities": _safe_string_list(raw.get("facilities")),
        "time_zone": raw.get("time_zone", "Europe/Amsterdam"),
        "opening_times_twentyfourseven": _parse_optional_bool(opening_times.get("twentyfourseven")),
        "charging_when_closed": _parse_optional_bool(raw.get("charging_when_closed")),
        "energy_mix_is_green_energy": _parse_optional_bool(energy_mix.get("is_green_energy")),
        "energy_mix_supplier_name": _safe_string(energy_mix.get("supplier_name")),
        "evse_count": len(evses),
        "connector_count": connector_count,
        "last_updated": raw.get("last_updated", datetime.now(timezone.utc).isoformat()),
    }


def normalize_connector(raw_connector: dict[str, Any]) -> dict[str, Any]:
    """Extract a flat ConnectorSummary dict from an OCPI Connector object."""
    return {
        "connector_id": str(raw_connector.get("id", "")),
        "standard": raw_connector.get("standard", ""),
        "format": raw_connector.get("format", "SOCKET"),
        "power_type": raw_connector.get("power_type", "AC_3_PHASE"),
        "max_voltage": int(raw_connector.get("max_voltage", 0)),
        "max_amperage": int(raw_connector.get("max_amperage", 0)),
        "max_electric_power": int(raw_connector["max_electric_power"]) if raw_connector.get("max_electric_power") is not None else None,
        "tariff_ids": _safe_string_list(raw_connector.get("tariff_ids")),
    }


def normalize_evse(location_id: str, raw_evse: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Extract a flat EvseStatus dict from an OCPI EVSE object."""
    evse_uid = raw_evse.get("uid")
    if not evse_uid:
        return None

    coords = raw_evse.get("coordinates") or {}
    connectors_raw = raw_evse.get("connectors") or []
    connectors = [normalize_connector(c) for c in connectors_raw if isinstance(c, dict)]
    if not connectors:
        return None

    return {
        "location_id": str(location_id),
        "evse_uid": str(evse_uid),
        "evse_id": _safe_string(raw_evse.get("evse_id")),
        "status": raw_evse.get("status", "UNKNOWN"),
        "capabilities": _safe_string_list(raw_evse.get("capabilities")),
        "floor_level": _safe_string(raw_evse.get("floor_level")),
        "latitude": _parse_optional_float(coords.get("latitude")),
        "longitude": _parse_optional_float(coords.get("longitude")),
        "physical_reference": _safe_string(raw_evse.get("physical_reference")),
        "parking_restrictions": _safe_string_list(raw_evse.get("parking_restrictions")),
        "connectors": connectors,
        "last_updated": raw_evse.get("last_updated", datetime.now(timezone.utc).isoformat()),
    }


def normalize_tariff(raw: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Extract a flat ChargingTariff dict from an OCPI Tariff object."""
    tariff_id = raw.get("id")
    if not tariff_id:
        return None

    elements_raw = raw.get("elements") or []
    elements = []
    for elem in elements_raw:
        if not isinstance(elem, dict):
            continue
        pcs_raw = elem.get("price_components") or []
        pcs = []
        for pc in pcs_raw:
            if not isinstance(pc, dict):
                continue
            pcs.append({
                "type": pc.get("type", "FLAT"),
                "price": float(pc.get("price", 0)),
                "vat": float(pc["vat"]) if pc.get("vat") is not None else None,
                "step_size": int(pc.get("step_size", 1)),
            })
        if not pcs:
            continue
        restrictions_raw = elem.get("restrictions")
        restrictions = None
        if isinstance(restrictions_raw, dict):
            restrictions = {
                "start_time": _safe_string(restrictions_raw.get("start_time")),
                "end_time": _safe_string(restrictions_raw.get("end_time")),
                "start_date": _safe_string(restrictions_raw.get("start_date")),
                "end_date": _safe_string(restrictions_raw.get("end_date")),
                "min_kwh": _parse_optional_float(restrictions_raw.get("min_kwh")),
                "max_kwh": _parse_optional_float(restrictions_raw.get("max_kwh")),
                "min_current": _parse_optional_float(restrictions_raw.get("min_current")),
                "max_current": _parse_optional_float(restrictions_raw.get("max_current")),
                "min_power": _parse_optional_float(restrictions_raw.get("min_power")),
                "max_power": _parse_optional_float(restrictions_raw.get("max_power")),
                "min_duration": int(restrictions_raw["min_duration"]) if restrictions_raw.get("min_duration") is not None else None,
                "max_duration": int(restrictions_raw["max_duration"]) if restrictions_raw.get("max_duration") is not None else None,
                "day_of_week": _safe_string_list(restrictions_raw.get("day_of_week")),
                "reservation": _safe_string(restrictions_raw.get("reservation")),
            }
        elements.append({
            "price_components": pcs,
            "restrictions": restrictions,
        })

    if not elements:
        return None

    alt_text_list = raw.get("tariff_alt_text") or []
    alt_text = None
    if isinstance(alt_text_list, list) and alt_text_list:
        first = alt_text_list[0] if isinstance(alt_text_list[0], dict) else {}
        alt_text = _safe_string(first.get("text"))

    min_price = raw.get("min_price") or {}
    max_price = raw.get("max_price") or {}

    return {
        "tariff_id": str(tariff_id),
        "country_code": raw.get("country_code", ""),
        "party_id": raw.get("party_id", ""),
        "currency": raw.get("currency", "EUR"),
        "tariff_type": _safe_string(raw.get("type")),
        "tariff_alt_text": alt_text,
        "tariff_alt_url": _safe_string(raw.get("tariff_alt_url")),
        "min_price_excl_vat": _parse_optional_float(min_price.get("excl_vat") if isinstance(min_price, dict) else None),
        "min_price_incl_vat": _parse_optional_float(min_price.get("incl_vat") if isinstance(min_price, dict) else None),
        "max_price_excl_vat": _parse_optional_float(max_price.get("excl_vat") if isinstance(max_price, dict) else None),
        "max_price_incl_vat": _parse_optional_float(max_price.get("incl_vat") if isinstance(max_price, dict) else None),
        "elements": elements,
        "start_date_time": _safe_string(raw.get("start_date_time")),
        "end_date_time": _safe_string(raw.get("end_date_time")),
        "energy_mix_is_green_energy": _parse_optional_bool((raw.get("energy_mix") or {}).get("is_green_energy")),
        "last_updated": raw.get("last_updated", datetime.now(timezone.utc).isoformat()),
    }


def _load_generated_data_classes() -> dict[str, type[Any]]:
    module = importlib.import_module("ndl_netherlands_producer_data")
    classes = {}
    for name in ("ChargingLocation", "EvseStatus", "ChargingTariff", "ConnectorSummary",
                 "PriceComponent", "TariffElement", "TariffRestrictions",
                 "StatusEnum", "FormatEnum", "PowerTypeenum", "ParkingTypeenum",
                 "TariffTypeenum", "TypeEnum", "ReservationEnum"):
        cls = getattr(module, name, None)
        if cls is not None:
            classes[name] = cls
    return classes


def _load_generated_producer_classes() -> dict[str, type[Any]]:
    module = importlib.import_module("ndl_netherlands_producer_kafka_producer.producer")
    producers = {}
    for attr in dir(module):
        obj = getattr(module, attr)
        if isinstance(obj, type) and attr.endswith("EventProducer"):
            producers[attr] = obj
    return producers


def _build_data_object(classes: dict[str, type[Any]], snapshot: dict[str, Any], schema_name: str) -> Any:
    """Build a generated dataclass instance from a normalized snapshot dict."""
    cls = classes[schema_name]

    if schema_name == "ChargingLocation":
        kwargs = dict(snapshot)
        if kwargs.get("parking_type") is not None:
            kwargs["parking_type"] = classes["ParkingTypeenum"](kwargs["parking_type"])
        kwargs["last_updated"] = _to_datetime(kwargs["last_updated"])
        return cls(**kwargs)

    if schema_name == "EvseStatus":
        kwargs = dict(snapshot)
        kwargs["status"] = classes["StatusEnum"](kwargs["status"])
        connectors = []
        for c in kwargs.get("connectors", []):
            c_kwargs = dict(c)
            c_kwargs["format"] = classes["FormatEnum"](c_kwargs["format"])
            c_kwargs["power_type"] = classes["PowerTypeenum"](c_kwargs["power_type"])
            connectors.append(classes["ConnectorSummary"](**c_kwargs))
        kwargs["connectors"] = connectors
        kwargs["last_updated"] = _to_datetime(kwargs["last_updated"])
        return cls(**kwargs)

    if schema_name == "ChargingTariff":
        kwargs = dict(snapshot)
        if kwargs.get("tariff_type") is not None:
            kwargs["tariff_type"] = classes["TariffTypeenum"](kwargs["tariff_type"])
        elements = []
        for elem in kwargs.get("elements", []):
            pcs = []
            for pc in elem.get("price_components", []):
                pc_kwargs = dict(pc)
                pc_kwargs["type"] = classes["TypeEnum"](pc_kwargs["type"])
                pcs.append(classes["PriceComponent"](**pc_kwargs))
            restrictions = None
            if elem.get("restrictions") is not None:
                r = dict(elem["restrictions"])
                if r.get("reservation") is not None:
                    r["reservation"] = classes["ReservationEnum"](r["reservation"])
                restrictions = classes["TariffRestrictions"](**r)
            elements.append(classes["TariffElement"](price_components=pcs, restrictions=restrictions))
        kwargs["elements"] = elements
        kwargs["last_updated"] = _to_datetime(kwargs["last_updated"])
        kwargs["start_date_time"] = _to_datetime(kwargs.get("start_date_time")) if kwargs.get("start_date_time") else None
        kwargs["end_date_time"] = _to_datetime(kwargs.get("end_date_time")) if kwargs.get("end_date_time") else None
        return cls(**kwargs)

    raise ValueError(f"Unknown schema: {schema_name}")


def _to_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        s = value.replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    return datetime.now(timezone.utc)


class NdlPoller:
    """Poll NDL open data files and send changes to Kafka."""

    headers = {
        "Accept": "*/*",
        "User-Agent": "(real-time-sources, clemensv@microsoft.com)",
    }

    def __init__(
        self,
        kafka_config: Optional[dict[str, str]] = None,
        charging_topic: Optional[str] = None,
        tariffs_topic: Optional[str] = None,
        state_file: Optional[str] = None,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
    ):
        self.charging_topic = charging_topic or DEFAULT_CHARGING_TOPIC
        self.tariffs_topic = tariffs_topic or DEFAULT_TARIFFS_TOPIC
        self.state_file = Path(state_file or DEFAULT_STATE_FILE)
        self.poll_interval_seconds = poll_interval_seconds
        self.evse_state: dict[str, str] = {}  # key=location_id/evse_uid -> value=status
        self.data_classes: dict[str, type[Any]] = {}
        self.location_producer: Optional[Any] = None
        self.evse_producer: Optional[Any] = None
        self.tariff_producer: Optional[Any] = None
        self._first_poll = True

        if kafka_config is not None:
            self.data_classes = _load_generated_data_classes()
            producer_classes = _load_generated_producer_classes()
            kafka_producer = Producer(kafka_config)

            for name, cls in producer_classes.items():
                if "Locations" in name:
                    self.location_producer = cls(kafka_producer, self.charging_topic)
                elif "Evse" in name:
                    self.evse_producer = cls(kafka_producer, self.charging_topic)
                elif "Tariffs" in name:
                    self.tariff_producer = cls(kafka_producer, self.tariffs_topic)

    def load_state(self) -> None:
        if self.state_file.exists():
            try:
                with self.state_file.open("r", encoding="utf-8") as f:
                    state = json.load(f)
                    self.evse_state = state.get("evse_state", {})
                    self._first_poll = False
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                logger.warning("Failed to load state: %s", exc)

    def save_state(self) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        temp = self.state_file.with_suffix(self.state_file.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as f:
            json.dump({"evse_state": self.evse_state}, f, separators=(",", ":"))
        temp.replace(self.state_file)

    async def fetch_gzip_json(self, session: aiohttp.ClientSession, filename: str) -> Any:
        url = f"{BASE_URL}/{filename}"
        logger.info("Downloading %s", url)
        async with session.get(url, headers=self.headers) as response:
            response.raise_for_status()
            compressed = await response.read()
        with gzip.GzipFile(fileobj=BytesIO(compressed)) as gz:
            raw = gz.read()
        return json.loads(raw)

    def _send_location(self, snapshot: dict[str, Any]) -> None:
        if not self.location_producer:
            return
        data = _build_data_object(self.data_classes, snapshot, "ChargingLocation")
        self.location_producer.send_nl_ndw_charging_charging_location(
            _location_id=snapshot["location_id"],
            _last_updated=snapshot["last_updated"],
            data=data,
            flush_producer=False,
        )

    def _send_evse_status(self, snapshot: dict[str, Any]) -> None:
        if not self.evse_producer:
            return
        data = _build_data_object(self.data_classes, snapshot, "EvseStatus")
        self.evse_producer.send_nl_ndw_charging_evse_status(
            _location_id=snapshot["location_id"],
            _evse_uid=snapshot["evse_uid"],
            _last_updated=snapshot["last_updated"],
            data=data,
            flush_producer=False,
        )

    def _send_tariff(self, snapshot: dict[str, Any]) -> None:
        if not self.tariff_producer:
            return
        data = _build_data_object(self.data_classes, snapshot, "ChargingTariff")
        self.tariff_producer.send_nl_ndw_charging_charging_tariff(
            _tariff_id=snapshot["tariff_id"],
            _last_updated=snapshot["last_updated"],
            data=data,
            flush_producer=False,
        )

    def process_locations(self, raw_locations: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
        """Process OCPI locations, emit reference data and EVSE status changes."""
        stats: dict[str, dict[str, int]] = {
            "locations": {"emitted": 0, "skipped": 0},
            "evse": {"appeared": 0, "updated": 0, "resolved": 0, "unchanged": 0},
        }
        new_evse_state: dict[str, str] = {}

        for raw_loc in raw_locations:
            if not isinstance(raw_loc, dict):
                continue

            location = normalize_location(raw_loc)
            if location is None:
                stats["locations"]["skipped"] += 1
                continue

            # Emit location reference on first poll
            if self._first_poll:
                self._send_location(location)
                stats["locations"]["emitted"] += 1

            location_id = location["location_id"]
            for raw_evse in (raw_loc.get("evses") or []):
                if not isinstance(raw_evse, dict):
                    continue
                evse = normalize_evse(location_id, raw_evse)
                if evse is None:
                    continue

                key = f"{evse['location_id']}/{evse['evse_uid']}"
                current_status = evse["status"]
                new_evse_state[key] = current_status
                previous_status = self.evse_state.get(key)

                if previous_status is None:
                    if not self._first_poll:
                        self._send_evse_status(evse)
                        stats["evse"]["appeared"] += 1
                    else:
                        self._send_evse_status(evse)
                        stats["evse"]["appeared"] += 1
                elif previous_status != current_status:
                    self._send_evse_status(evse)
                    stats["evse"]["updated"] += 1
                else:
                    stats["evse"]["unchanged"] += 1

        # Detect removed EVSEs
        removed_keys = set(self.evse_state.keys()) - set(new_evse_state.keys())
        stats["evse"]["resolved"] = len(removed_keys)

        self.evse_state = new_evse_state
        return stats

    def process_tariffs(self, raw_tariffs: list[dict[str, Any]]) -> dict[str, int]:
        """Process OCPI tariffs, emit reference data on first poll."""
        stats = {"emitted": 0, "skipped": 0}
        if not self._first_poll:
            return stats

        for raw in raw_tariffs:
            if not isinstance(raw, dict):
                continue
            tariff = normalize_tariff(raw)
            if tariff is None:
                stats["skipped"] += 1
                continue
            self._send_tariff(tariff)
            stats["emitted"] += 1

        return stats

    async def poll_once(self, session: aiohttp.ClientSession) -> dict[str, Any]:
        """Execute one poll cycle."""
        poll_stats: dict[str, Any] = {}

        # Download and process locations + EVSE status
        try:
            raw_locations = await self.fetch_gzip_json(session, LOCATIONS_FILE)
            if not isinstance(raw_locations, list):
                logger.error("Locations file is not a JSON array")
                raw_locations = []
        except Exception as exc:
            logger.error("Failed to download locations: %s", exc)
            raw_locations = []

        if raw_locations:
            loc_stats = self.process_locations(raw_locations)
            poll_stats["locations"] = loc_stats
            logger.info(
                "Locations: %d emitted, EVSE: %d appeared, %d updated, %d resolved, %d unchanged",
                loc_stats["locations"]["emitted"],
                loc_stats["evse"]["appeared"],
                loc_stats["evse"]["updated"],
                loc_stats["evse"]["resolved"],
                loc_stats["evse"]["unchanged"],
            )

        # Download and process tariffs (first poll only)
        if self._first_poll:
            try:
                raw_tariffs = await self.fetch_gzip_json(session, TARIFFS_FILE)
                if not isinstance(raw_tariffs, list):
                    logger.error("Tariffs file is not a JSON array")
                    raw_tariffs = []
            except Exception as exc:
                logger.error("Failed to download tariffs: %s", exc)
                raw_tariffs = []

            if raw_tariffs:
                tariff_stats = self.process_tariffs(raw_tariffs)
                poll_stats["tariffs"] = tariff_stats
                logger.info("Tariffs: %d emitted, %d skipped", tariff_stats["emitted"], tariff_stats["skipped"])

        self._first_poll = False
        self.save_state()
        return poll_stats

    async def run(self, session: aiohttp.ClientSession) -> None:
        """Run the polling loop."""
        self.load_state()
        while True:
            try:
                await self.poll_once(session)
            except Exception:
                logger.exception("Poll cycle failed")
            logger.info("Sleeping %d seconds", self.poll_interval_seconds)
            await asyncio.sleep(self.poll_interval_seconds)


async def async_main(args: argparse.Namespace) -> None:
    kafka_config: Optional[dict[str, str]] = None
    charging_topic = args.charging_topic
    tariffs_topic = args.tariffs_topic

    if args.connection_string:
        kafka_config = parse_connection_string(args.connection_string)
        if "kafka_topic" in kafka_config:
            if not charging_topic:
                charging_topic = kafka_config.pop("kafka_topic")
            else:
                kafka_config.pop("kafka_topic", None)
    elif args.bootstrap_servers:
        kafka_config = {"bootstrap.servers": args.bootstrap_servers}
        if args.sasl_username:
            kafka_config["security.protocol"] = "SASL_SSL"
            kafka_config["sasl.mechanism"] = "PLAIN"
            kafka_config["sasl.username"] = args.sasl_username
            kafka_config["sasl.password"] = args.sasl_password or ""

    poller = NdlPoller(
        kafka_config=kafka_config,
        charging_topic=charging_topic,
        tariffs_topic=tariffs_topic,
        state_file=args.state_file,
        poll_interval_seconds=args.poll_interval,
    )

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        if args.once:
            poller.load_state()
            await poller.poll_once(session)
        else:
            await poller.run(session)


def main() -> None:
    parser = argparse.ArgumentParser(description="NDL Netherlands EV charging bridge")
    parser.add_argument("--connection-string", default=os.environ.get("NDL_CONNECTION_STRING"), help="Event Hubs connection string")
    parser.add_argument("--bootstrap-servers", default=os.environ.get("KAFKA_BOOTSTRAP_SERVERS"), help="Kafka bootstrap servers")
    parser.add_argument("--sasl-username", default=os.environ.get("KAFKA_SASL_USERNAME"), help="SASL username")
    parser.add_argument("--sasl-password", default=os.environ.get("KAFKA_SASL_PASSWORD"), help="SASL password")
    parser.add_argument("--charging-topic", default=os.environ.get("NDL_CHARGING_TOPIC", DEFAULT_CHARGING_TOPIC), help="Kafka topic for charging data")
    parser.add_argument("--tariffs-topic", default=os.environ.get("NDL_TARIFFS_TOPIC", DEFAULT_TARIFFS_TOPIC), help="Kafka topic for tariff data")
    parser.add_argument("--state-file", default=os.environ.get("NDL_STATE_FILE", DEFAULT_STATE_FILE), help="Path to state file")
    parser.add_argument("--poll-interval", type=int, default=int(os.environ.get("NDL_POLL_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)), help="Poll interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run one poll cycle and exit")
    args = parser.parse_args()

    asyncio.run(async_main(args))
