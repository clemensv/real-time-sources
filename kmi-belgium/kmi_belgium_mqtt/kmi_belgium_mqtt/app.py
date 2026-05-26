
from __future__ import annotations
import argparse, json, os, re, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

_TEMPLATE = re.compile(r"\{([^}]+)\}")

def _xreg_path() -> Path:
    candidates = [Path.cwd() / "xreg", Path(__file__).resolve().parents[2] / "xreg"]
    for candidate in candidates:
        if candidate.exists():
            return next(candidate.glob("*.xreg.json"))
    raise FileNotFoundError("Could not locate source xreg directory")

def _ptr(doc: Mapping[str, Any], ref: str) -> Any:
    obj: Any = doc
    for part in ref.strip("#/").split("/"):
        if part:
            obj = obj[part]
    return obj

def _resolve_message(doc: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    base = message.get("basemessageurl")
    if not base:
        return dict(message)
    merged = _resolve_message(doc, _ptr(doc, base))
    merged.update({k: v for k, v in message.items() if k != "basemessageurl"})
    return merged

def _root_schema(schema: dict[str, Any]) -> dict[str, Any]:
    root = schema.get("$root")
    if root:
        return _ptr(schema, root)
    return schema

def _schema_for(doc: Mapping[str, Any], message: Mapping[str, Any]) -> dict[str, Any]:
    rec = _ptr(doc, message["dataschemauri"])
    schema = rec["versions"][rec["defaultversionid"]]["schema"]
    return _root_schema(schema)

def _sample_for_type(name: str, typ: Any) -> Any:
    if isinstance(typ, list):
        typ = next((t for t in typ if t != "null"), "string")
    if isinstance(typ, dict) and "$ref" in typ:
        return {}
    if typ in ("string", "datetime", "date", "time"):
        if name.endswith("time") or name in {"timestamp", "sent", "effective", "expires", "updated", "published_at", "observation_time", "obs_time", "report_time", "valid_time_from", "valid_time_to", "last_update", "next_update", "modified", "run"}:
            return "2026-01-01T00:00:00Z"
        return name.replace("_", "-") + "-sample"
    if typ in ("int32", "int64", "integer"):
        return 1
    if typ in ("double", "float", "number"):
        return 1.0
    if typ == "boolean":
        return True
    if typ == "array":
        return []
    if typ == "object":
        return {}
    return "sample"

def _build_payload(schema: dict[str, Any], placeholders: Mapping[str, str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    for name, spec in props.items():
        if name in placeholders:
            payload[name] = placeholders[name]
        elif name in required:
            payload[name] = _sample_for_type(name, spec.get("type", "string"))
    for name, value in placeholders.items():
        payload.setdefault(name, value)
    return payload

def _render(template: str, values: Mapping[str, Any]) -> str:
    return _TEMPLATE.sub(lambda m: str(values[m.group(1)]), template)

def _contracts(protocol_prefix: str) -> list[dict[str, Any]]:
    doc = json.loads(_xreg_path().read_text(encoding="utf-8"))
    out = []
    for ep in doc.get("endpoints", {}).values():
        if not str(ep.get("protocol", "")).startswith(protocol_prefix):
            continue
        for ref in ep.get("messagegroups", []):
            group = _ptr(doc, ref)
            for msg in group.get("messages", {}).values():
                resolved = _resolve_message(doc, msg)
                schema = _schema_for(doc, resolved)
                meta = resolved.get("envelopemetadata", {})
                opts = resolved.get("protocoloptions", {}) or {}
                props = opts.get("properties", {}) if isinstance(opts.get("properties"), dict) else {}
                topic = opts.get("topic_name") or opts.get("topic") or props.get("topic")
                if isinstance(topic, dict): topic = topic.get("value")
                subj = meta.get("subject", {}).get("value", "sample")
                placeholders = {name: name.replace("_", "-") + "-sample" for name in set(_TEMPLATE.findall(str(topic or "")) + _TEMPLATE.findall(subj))}
                # Stable prettier samples for common axes.
                placeholders.update({
                    "icao_id":"KJFK", "region":"intl", "sigmet_id":"sigmet-001", "state":"wa", "severity":"severe",
                    "event_type":"winter-storm", "station_id":"station-001", "station_wmo":"94610", "msc_id":"6158350",
                    "place_id":"hko", "station_code":"06447", "bulletin_id":"bulletin-001", "office":"tokyo",
                    "province":"on", "bundesland":"wien", "district":"central-and-western", "lan":"stockholm",
                    "zone_id":"waz001", "alert_id":"alert-001", "warning_id":"warning-001", "identifier":"dwd-alert-001",
                    "kind":"radar", "product_type":"rx", "file_id":"file-001", "variable":"temperature",
                    "region_id":"11", "pollen_type":"hazel", "geohash5":"u0yjx", "geohash7":"u0yjx7p", "stroke_id":"123456789", "source_id":"4"
                })
                payload = _build_payload(schema, placeholders)
                subject = _render(subj, {**payload, **placeholders})
                out.append({"message": resolved, "schema": schema, "payload": payload, "topic": _render(topic, {**payload, **placeholders}) if topic else None,
                            "qos": int(opts.get("qos", props.get("qos", 1))), "retain": bool(opts.get("retain", props.get("retain", False))),
                            "type": meta.get("type", {}).get("value"), "source": meta.get("source", {}).get("value", "sample"), "subject": subject})
    return out

def publish_mqtt(args: argparse.Namespace) -> None:
    import paho.mqtt.client as mqtt
    from paho.mqtt.client import CallbackAPIVersion, MQTTv5
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    from urllib.parse import urlparse
    parsed = urlparse(args.broker_url if "://" in args.broker_url else "mqtt://" + args.broker_url)
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if parsed.username: client.username_pw_set(parsed.username, parsed.password or "")
    if parsed.scheme in ("mqtts", "ssl", "tls") or args.tls: client.tls_set()
    client.connect(parsed.hostname or "localhost", parsed.port or (8883 if parsed.scheme == "mqtts" else 1883), 30)
    client.loop_start()
    try:
        for c in _contracts("MQTT"):
            props = Properties(PacketTypes.PUBLISH)
            props.ContentType = "application/json"
            props.UserProperty = [("specversion", "1.0"), ("id", str(uuid.uuid4())), ("source", str(c["source"])), ("type", str(c["type"])), ("subject", c["subject"]), ("time", datetime.now(timezone.utc).isoformat())]
            info = client.publish(c["topic"], json.dumps(c["payload"], ensure_ascii=False).encode("utf-8"), qos=c["qos"], retain=c["retain"], properties=props)
            info.wait_for_publish()
    finally:
        time.sleep(0.5)
        client.loop_stop()
        client.disconnect()

def publish_amqp(args: argparse.Namespace) -> None:
    from proton import Message
    from proton.utils import BlockingConnection
    from urllib.parse import quote
    user = quote(args.username or "")
    pwd = quote(args.password or "")
    auth = f"{user}:{pwd}@" if args.username else ""
    url = f"amqp://{auth}{args.host}:{args.port}"
    conn = BlockingConnection(url, timeout=30, allowed_mechs="PLAIN")
    sender = conn.create_sender(args.address)
    try:
        for c in _contracts("AMQP"):
            props = {"cloudEvents:specversion":"1.0", "cloudEvents:id":str(uuid.uuid4()), "cloudEvents:source":str(c["source"]), "cloudEvents:type":str(c["type"]), "cloudEvents:subject":c["subject"], "cloudEvents:time":datetime.now(timezone.utc).isoformat(), "content-type":"application/json"}
            msg = Message(body=json.dumps(c["payload"], ensure_ascii=False), subject=c["subject"], properties=props, content_type="application/json")
            sender.send(msg)
    finally:
        conn.close()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("MQTT_TLS", "").lower() in ("1","true","yes"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "5672")))
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "kmi-belgium"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--once", action="store_true", default=True)
    parser.add_argument("--mock-mode", action="store_true", default=True)
    args = parser.parse_args()
    if "amqp" in __package__:
        publish_amqp(args)
    else:
        publish_mqtt(args)
if __name__ == "__main__": main()
