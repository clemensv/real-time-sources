
"""AMQP 1.0 companion feeder for noaa-goes."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import inspect
import json
import logging
import os
import pathlib
import re
import sys
import time
from datetime import datetime, timezone, timedelta, date
from typing import Any, Optional
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "noaa-goes"
PY_MODULE = "noaa_goes"
ENV_PREFIX = "NOAA_GOES"

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _topic_segment(value: Any) -> str:
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _producer_class():
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer")
    classes = [obj for _, obj in vars(mod).items() if inspect.isclass(obj) and any(name.startswith("send_") for name in dir(obj))]
    if not classes:
        raise RuntimeError(f"No AMQP producer class found in {mod.__name__}")
    # xrcg can emit producer classes whose names do not end with "AmqpProducer"
    # (for example after a simplified message-group manifest). Prefer the concrete
    # class with the most send_* methods rather than relying on the old naming rule.
    classes.sort(key=lambda cls: (len([name for name in dir(cls) if name.startswith("send_")]), cls.__name__), reverse=True)
    return classes[0]


def _apply_partition_key_workaround(producer):
    # WORKAROUND(xregistry/codegen#294): xrcg declares AMQP message_annotations
    # but does not emit them yet. Stamp x-opt-partition-key from CE subject.
    def stamp(msg):
        props = dict(getattr(msg, "properties", None) or {})
        ce_subject = props.get("cloudEvents:subject") or getattr(msg, "subject", None)
        if ce_subject:
            annotations = dict(getattr(msg, "annotations", None) or {})
            annotations[symbol("x-opt-partition-key")] = str(ce_subject)
            msg.annotations = annotations
        return msg
    if getattr(producer, "_sender", None) is not None:
        original_send = producer._sender.send
        producer._sender.send = lambda msg, *a, **kw: original_send(stamp(msg), *a, **kw)
    if hasattr(producer, "_send_via_reactor"):
        original_reactor_send = producer._send_via_reactor
        producer._send_via_reactor = lambda msg: original_reactor_send(stamp(msg))
    return producer


def _build_amqp_producer(args):
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        address = path or address
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    kwargs = dict(host=host, address=address, port=port, content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(_producer_class()(**kwargs))


class MqttToAmqpAdapter:
    """Adapter exposing generated MQTT publish_* names over AMQP send_* APIs."""
    def __init__(self, producer: Any):
        self.producer = producer
        self._send_methods = {name: getattr(producer, name) for name in dir(producer) if name.startswith("send_") and not name.endswith("_batch")}
        self.sent = 0

    async def connect(self, *_args, **_kwargs):
        return None

    async def disconnect(self):
        close = getattr(self.producer, "close", None)
        if close:
            close()

    def _choose_method(self, publish_name: str, kwargs: dict[str, Any]):
        route_keys = {"_" + k for k in kwargs if k not in {"data", "qos", "retain", "topic", "content_type", "message_expiry_interval"}}
        candidates = []
        publish_norm = publish_name.replace("publish_", "").replace("mqtt", "amqp")
        words = set(re.split(r"_+", publish_norm))
        compact_publish = re.sub(r"[^a-z0-9]", "", publish_norm.lower())
        for name, method in self._send_methods.items():
            params = inspect.signature(method).parameters
            required_route = {p for p, _param in params.items() if p.startswith("_") and _param.default is inspect.Parameter.empty}
            if not required_route <= route_keys:
                continue
            method_words = set(re.split(r"_+", name))
            compact_method = re.sub(r"[^a-z0-9]", "", name.lower().replace("send", ""))
            score = len(words & method_words)
            if compact_method and compact_method in compact_publish:
                score += 100
            candidates.append((score, len(required_route), name, method, required_route))
        if not candidates:
            raise AttributeError(f"No AMQP send method matches {publish_name} with route keys {sorted(route_keys)}")
        candidates.sort(reverse=True)
        return candidates[0][3], candidates[0][4]

    def __getattr__(self, name: str):
        if not name.startswith("publish_"):
            raise AttributeError(name)
        async def publish(**kwargs):
            method, route = self._choose_method(name, kwargs)
            call_kwargs = {p: _topic_segment(kwargs[p[1:]]) for p in route}
            call_kwargs["data"] = kwargs.get("data")
            if "content_type" in inspect.signature(method).parameters and kwargs.get("content_type"):
                call_kwargs["content_type"] = kwargs["content_type"]
            method(**call_kwargs)
            self.sent += 1
        return publish


def _manifest_path() -> pathlib.Path:
    candidates = [pathlib.Path.cwd(), pathlib.Path(__file__).resolve().parents[2]]
    for root in candidates:
        xreg = root / "xreg"
        if xreg.exists():
            matches = list(xreg.glob("*.json"))
            if matches:
                return matches[0]
    raise FileNotFoundError("xRegistry manifest not found in working directory or package parents")


def _schema_root(schema: dict[str, Any]) -> Any:
    node = schema.get("schema", schema)
    root = node.get("$root")
    if root:
        cur = node
        for part in root.lstrip("#/").split("/"):
            cur = cur[part]
        return cur, node
    return node, node


def _resolve_ref(ref: str, doc: dict[str, Any]) -> Any:
    cur = doc
    for part in ref.lstrip("#/").split("/"):
        cur = cur[part]
    return cur


def _sample_for_type(type_spec: Any, doc: dict[str, Any], name: str = "value") -> Any:
    if isinstance(type_spec, list):
        return _sample_for_type(next((t for t in type_spec if t != "null"), "string"), doc, name)
    if isinstance(type_spec, dict):
        if "$ref" in type_spec:
            return _sample_for_node(_resolve_ref(type_spec["$ref"], doc), doc)
        return _sample_for_node(type_spec, doc)
    if type_spec in ("string", "timestamp"):
        return "2026-01-01T00:00:00Z" if "time" in name or "date" in name else f"sample-{name.replace('_','-')}"
    if type_spec in ("integer", "int32", "int64"):
        return 1
    if type_spec in ("number", "float", "double"):
        return 1.0
    if type_spec == "boolean":
        return True
    if type_spec == "array":
        return []
    if type_spec == "object":
        return {}
    return f"sample-{name}"


def _sample_for_node(node: dict[str, Any], doc: dict[str, Any]) -> Any:
    if "enum" in node and node["enum"]:
        return node["enum"][0]
    t = node.get("type", "string")
    if t == "object" or isinstance(t, dict) and "$ref" in t:
        if isinstance(t, dict) and "$ref" in t:
            return _sample_for_node(_resolve_ref(t["$ref"], doc), doc)
        props = node.get("properties", {})
        return {name: _sample_for_node(prop, doc) for name, prop in props.items()}
    if t == "array":
        return [_sample_for_node(node.get("items", {"type": "string"}), doc)]
    return _sample_for_type(t, doc, node.get("name", "value"))


def _data_class_for(schema_name: str):
    data_mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_data")
    class_name = schema_name.split(".")[-1]
    return getattr(data_mod, class_name)


def _coerce_data(cls: type[Any], payload: dict[str, Any]) -> Any:
    for name in ("from_serializer_dict", "from_dict"):
        if hasattr(cls, name):
            try:
                return getattr(cls, name)(payload)
            except Exception:
                pass
    return cls(**payload)


def emit_mock_corpus(adapter: MqttToAmqpAdapter) -> None:
    manifest = json.loads(_manifest_path().read_text(encoding="utf-8"))
    jstruct_group = next(v for k, v in manifest["schemagroups"].items() if k.endswith(".jstruct"))
    amqp_group = None
    for endpoint in manifest.get("endpoints", {}).values():
        if endpoint.get("protocol") != "AMQP/1.0":
            continue
        for group_uri in endpoint.get("messagegroups", []):
            group_name = group_uri.strip("/").rsplit("/", 1)[-1]
            if group_name in manifest.get("messagegroups", {}):
                amqp_group = manifest["messagegroups"][group_name]
                break
        if amqp_group is not None:
            break
    if amqp_group is None:
        amqp_group = next(v for k, v in manifest["messagegroups"].items() if k.endswith(".amqp"))
    for message_name, message in amqp_group["messages"].items():
        schema_name = None
        if "dataschemauri" in message:
            schema_name = message["dataschemauri"].split("/")[-1]
        else:
            base = message["basemessageuri"].strip("/").split("/")
            base_msg = manifest["messagegroups"][base[1]]["messages"][base[3]]
            schema_name = base_msg["dataschemauri"].split("/")[-1]
        schema_entry = jstruct_group["schemas"][schema_name]["versions"]["1"]["schema"]
        root_node, doc = _schema_root(schema_entry)
        payload = _sample_for_node(root_node, doc)
        data = _coerce_data(_data_class_for(schema_name), payload)
        route = {}
        def collect_templates(node):
            if isinstance(node, dict):
                if node.get("type") == "uritemplate":
                    for key in re.findall(r"\{([A-Za-z0-9_]+)\}", node.get("value", "")):
                        route[key] = payload.get(key, f"sample-{key.replace('_','-')}") if isinstance(payload, dict) else f"sample-{key}"
                for child in node.values():
                    collect_templates(child)
            elif isinstance(node, list):
                for child in node:
                    collect_templates(child)
        collect_templates(message.get("protocoloptions") or {})
        if isinstance(payload, dict):
            for key, value in payload.items():
                route.setdefault(key, value)
        # Pre-fill route with required params from all send methods (dummy values)
        for _m_name, _m_func in adapter._send_methods.items():
            for _p, _param in inspect.signature(_m_func).parameters.items():
                if _p.startswith("_") and _param.default is inspect.Parameter.empty:
                    route.setdefault(_p[1:], f"sample-{_p[1:]}")
        try:
            method, required = adapter._choose_method("publish_" + message_name.lower().replace(".", "_"), {**route, "data": data})
            call_kwargs = {p: _topic_segment(route.get(p[1:], f"sample-{p[1:]}")) for p in required}
            call_kwargs["data"] = data
            method(**call_kwargs)
        except (AttributeError, TypeError, KeyError) as _route_err:
            logger.debug("Skipping message %s: %s", message_name, _route_err)
            continue
        adapter.sent += 1


async def _run_live(args: argparse.Namespace, adapter: MqttToAmqpAdapter) -> None:
    try:
        mqtt_app = importlib.import_module(f"{PY_MODULE}_mqtt.app")
    except (ImportError, ModuleNotFoundError):
        mqtt_app = None
    if mqtt_app is None:
        logger.warning("MQTT bridge not available; emitting sample corpus via AMQP")
        emit_mock_corpus(adapter)
        return
    # Source-specific live acquisition hooks reuse the already-shipped MQTT pollers/bridges.
    if SOURCE_ID == "nws-alerts":
        bridge = mqtt_app.NWSAlertsMqttBridge(adapter, state_file=args.state_file, poll_interval=args.polling_interval)
        await bridge.poll_and_publish(once=args.once)
    elif SOURCE_ID == "ptwc-tsunami":
        core = importlib.import_module("ptwc_tsunami.ptwc_tsunami")
        feeds = [p.strip() for p in args.feeds.split(",") if p.strip()]
        poller = core.PTWCTsunamiPoller(kafka_config=None, kafka_topic="amqp", state_file=args.state_file, poll_interval=args.polling_interval, feeds=feeds)
        while True:
            await mqtt_app._poll_once(poller, adapter)
            if args.once: break
            await asyncio.sleep(args.polling_interval)
    elif SOURCE_ID == "nina-bbk":
        core = importlib.import_module("nina_bbk.nina_bbk")
        providers = [p.strip() for p in args.providers.split(",") if p.strip()]
        poller = core.NINABBKPoller(kafka_config=None, kafka_topic="amqp", state_file=args.state_file, poll_interval=args.polling_interval, providers=providers)
        while True:
            await mqtt_app._poll_once(poller, adapter)
            if args.once: break
            await asyncio.sleep(args.polling_interval)
    elif SOURCE_ID == "gdacs":
        core = importlib.import_module("gdacs.gdacs")
        poller = core.GDACSPoller(kafka_config=None, kafka_topic="amqp", state_file=args.state_file, poll_interval=args.polling_interval)
        while True:
            await mqtt_app._poll_once(poller, adapter)
            if args.once: break
            await asyncio.sleep(args.polling_interval)
    elif SOURCE_ID == "eaws-albina":
        core = importlib.import_module("eaws_albina.eaws_albina")
        regions = [p.strip() for p in args.regions.split(",") if p.strip()]
        poller = core.AlbinaPoller(kafka_config=None, kafka_topic="amqp", last_polled_file=args.state_file, regions=regions, lang=args.lang)
        while True:
            today = date.today()
            await mqtt_app._publish_date(poller, adapter, today.isoformat())
            await mqtt_app._publish_date(poller, adapter, (today - timedelta(days=1)).isoformat())
            if args.once: break
            await asyncio.sleep(args.polling_interval)
    elif SOURCE_ID == "cbp-border-wait":
        logger.info("cbp-border-wait: emitting sample corpus via AMQP")
        emit_mock_corpus(adapter)
    elif SOURCE_ID == "seattle-911":
        core = importlib.import_module("seattle_911.seattle_911")
        # Inline the MQTT feed loop with the adapter to avoid opening an MQTT connection.
        bridge = core.SeattleFire911Bridge(state_file=args.state_file)
        while True:
            since = datetime.utcnow() - timedelta(hours=core.DEFAULT_LOOKBACK_HOURS)
            incidents = bridge.fetch_incidents(since=since)
            for incident in incidents:
                await adapter.publish_us_wa_seattle_fire911_mqtt_incident(incident_number=incident.incident_number, incident_datetime_utc=incident.incident_datetime_utc.isoformat(), incident_type_slug=incident.incident_type_slug, data=incident)
            if args.once: break
            await asyncio.sleep(core.DEFAULT_POLL_INTERVAL_SECONDS)
    elif SOURCE_ID == "autobahn":
        core = importlib.import_module("autobahn.autobahn")
        resources = core.parse_resources_argument(args.resources)
        roads = core.parse_roads_argument(args.roads)
        bridge = mqtt_app.AutobahnMqttBridge(adapter, state_file=args.state_file, poll_interval_seconds=args.polling_interval, resources=resources, roads=roads, request_concurrency=args.request_concurrency)
        await bridge.poll_and_publish(once=args.once)
    elif SOURCE_ID == "tfl-road-traffic":
        bridge = mqtt_app.TflRoadTrafficMqttBridge(adapter, polling_interval=args.polling_interval)
        await bridge.poll_and_publish(once=args.once)
    elif SOURCE_ID == "entur-norway":
        core = importlib.import_module("entur_norway.entur_norway")
        bridge = core.EnturNorwayBridge()
        first = True
        import uuid
        et = str(uuid.uuid4()); vm = str(uuid.uuid4()); sx = str(uuid.uuid4())
        while True:
            await mqtt_app._publish_poll_cycle(bridge, adapter, first_run=first, et_requestor_id=et, vm_requestor_id=vm, sx_requestor_id=sx, max_size=args.max_size)
            first = False
            if args.once: break
            await asyncio.sleep(args.polling_interval)
    elif SOURCE_ID == "irail":
        logger.info("irail: emitting sample corpus via AMQP")
        emit_mock_corpus(adapter)
    elif SOURCE_ID == "paris-bicycle-counters":
        poller = mqtt_app.ParisBicycleCounterMqttPoller(adapter, args.state_file)
        await poller.poll_and_send_async(once=args.once)
    else:
        # Generic fallback: emit mock/sample corpus via AMQP (no source-specific live hook)
        logger.info("No source-specific AMQP handler for %s; emitting sample corpus", SOURCE_ID)
        while True:
            emit_mock_corpus(adapter)
            logger.info("Emitted %d sample AMQP event(s) for %s", adapter.sent, SOURCE_ID)
            if args.once:
                break
            await asyncio.sleep(args.polling_interval)


def _add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", SOURCE_ID))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    parser.add_argument("--mock-mode", action="store_true", default=_env_bool(f"{ENV_PREFIX}_MOCK", False) or _env_bool(f"{ENV_PREFIX}_SAMPLE_MODE", False) or _env_bool(f"{ENV_PREFIX}_AMQP_MOCK", False))
    # Source-specific optional knobs; ignored where not used.
    parser.add_argument("--feeds", default=os.getenv("PTWC_TSUNAMI_FEEDS", "PAAQ,PHEB"))
    parser.add_argument("--providers", default=os.getenv("NINA_BBK_PROVIDERS", "mowas,katwarn,biwapp,dwd,lhp,police"))
    parser.add_argument("--regions", default=os.getenv("EAWS_ALBINA_REGIONS", "AT-07-01"))
    parser.add_argument("--lang", default=os.getenv("EAWS_ALBINA_LANG", "en"))
    parser.add_argument("--resources", default=os.getenv("AUTOBAHN_RESOURCES", "all"))
    parser.add_argument("--roads", default=os.getenv("AUTOBAHN_ROADS", ""))
    parser.add_argument("--request-concurrency", type=int, default=int(os.getenv("AUTOBAHN_REQUEST_CONCURRENCY", "8")))
    parser.add_argument("--station-filter", default=os.getenv("STATION_FILTER", ""))
    parser.add_argument("--max-size", type=int, default=int(os.getenv("MAX_SIZE", "1000")))
    return parser



def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
async def _async_main(args: argparse.Namespace) -> None:
    # Retry producer connection with backoff (RBAC propagation can take minutes)
    producer = None
    for _attempt in range(6):
        try:
            producer = _retry_producer_init(lambda: _build_amqp_producer(args))
            break
        except Exception as _conn_err:
            logger.warning("AMQP connection attempt %d failed: %s", _attempt + 1, _conn_err)
            if _attempt < 5:
                await asyncio.sleep(15 * (_attempt + 1))
    if producer is None:
        logger.error("Failed to connect to AMQP broker after 6 attempts")
        return
    adapter = MqttToAmqpAdapter(producer)
    try:
        if args.mock_mode:
            emit_mock_corpus(adapter)
            logger.info("Published %d mock AMQP event(s)", adapter.sent)
        else:
            await _run_live(args, adapter)
    finally:
        close = getattr(producer, "close", None)
        if close:
            close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
