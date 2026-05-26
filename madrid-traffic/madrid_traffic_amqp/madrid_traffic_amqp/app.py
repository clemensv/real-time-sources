from __future__ import annotations

import argparse, json, os, re, time, uuid
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

PROJECT_DIR = "madrid-traffic"
XREG_FILE = "madrid_traffic.xreg.json"
TRANSPORT = "amqp"
ROOT = Path(os.getenv("SOURCE_ROOT", os.getcwd()))
if not (ROOT / "xreg" / XREG_FILE).exists():
    ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "xreg" / XREG_FILE
TEMPLATE_RE = re.compile(r"{([^{}]+)}")
NOW = "2025-01-15T12:00:00Z"

DEFAULTS = {
    "agencyid": "sample-agency", "agency_id": "sample-agency", "route_id": "sample-route", "route_tag": "sample-route",
    "vehicle_id": "sample-vehicle", "trip_id": "sample-trip", "alert_id": "sample-alert", "row_id": "sample-row",
    "road": "A1", "site_id": "sample-site", "situation_id": "sample-situation", "situation_record_id": "sample-situation",
    "district": "centro", "sensor_id": "sample-sensor", "counter_id": "sample-counter", "neighborhood": "downtown",
    "closure_id": "sample-closure", "road_id": "A1", "severity": "moderate", "disruption_id": "sample-disruption",
    "system_id": "docomo-cycle", "ward": "chiyoda", "station_id": "sample-station", "region": "seattle",
    "crossing_name": "sample-crossing", "vessel_id": "sample-vessel", "mountain_pass_id": "sample-pass",
    "state_route_id": "SR-520", "bridge_number": "sample-bridge", "flow_data_id": "sample-flow",
    "travel_time_id": "sample-travel-time", "trip_name": "sample-trip", "vms_controller_id": "sample-controller",
    "vms_index": "1", "sign_id": "sample-sign", "measurement_site_id": "sample-site", "id": "sample-id",
    "identifier": "sample-identifier", "event": "event", "ce_id": "sample-event", "date": NOW, "event_time": NOW,
}

def load_manifest() -> Dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def resolve_pointer(document: Mapping[str, Any], pointer: str) -> Any:
    if pointer.startswith('#'):
        pointer = pointer[1:]
    cur: Any = document
    for raw in pointer.strip('/').split('/'):
        if not raw:
            continue
        cur = cur[raw.replace('~1','/').replace('~0','~')]
    return cur

def resolve_message(document: Mapping[str, Any], message: Mapping[str, Any]) -> Dict[str, Any]:
    base_url = message.get('basemessageuri')
    if not base_url:
        return dict(message)
    base = resolve_message(document, resolve_pointer(document, str(base_url)))
    base.update({k:v for k,v in message.items() if k != 'basemessageuri'})
    return base

def render(template: str | None, context: Mapping[str, Any]) -> str:
    if not template:
        return ""
    def repl(match):
        name = match.group(1)
        return str(context.get(name, DEFAULTS.get(name, f"sample-{name.replace('_','-')}")))
    return TEMPLATE_RE.sub(repl, template)

def sample_for_type(spec: Any, defs: Mapping[str, Any]) -> Any:
    if isinstance(spec, list):
        non_null = [x for x in spec if x != 'null']
        return sample_for_type(non_null[0] if non_null else 'string', defs)
    if isinstance(spec, dict):
        if '$ref' in spec:
            resolved = resolve_pointer(defs, spec['$ref'])
            if isinstance(resolved, Mapping) and resolved.get('enum'):
                return resolved['enum'][0]
            if isinstance(resolved, Mapping) and resolved.get('type') not in (None, 'object'):
                return sample_for_type(resolved.get('type'), defs)
            return sample_from_schema(resolved, defs)
        if spec.get('enum'):
            return spec['enum'][0]
        if spec.get('type') == 'choice' and spec.get('choices'):
            choice_name, first = next(iter(spec['choices'].items()))
            return {choice_name: sample_for_type(first, defs)}
        if 'type' in spec:
            return sample_for_type(spec['type'], defs)
    t = str(spec or 'string').lower()
    if t in ('int','integer','long','int32','int64','uint32','uint64'): return 1
    if t in ('float','double','number','decimal'): return 1.0
    if t in ('bool','boolean'): return True
    if t == 'array': return []
    if t == 'object': return {}
    if 'date' in t or 'time' in t: return NOW
    return 'sample'

def sample_from_schema(schema: Mapping[str, Any], defs: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    root_doc = defs or schema
    if isinstance(schema, Mapping) and "$root" in schema:
        schema = resolve_pointer(schema, str(schema["$root"]))
    defs = root_doc
    if isinstance(schema.get('type'), dict) or schema.get('type') not in (None, 'object'):
        val = sample_for_type(schema.get('type'), defs)
        return val if isinstance(val, dict) else {"value": val}
    props = schema.get('properties') or {}
    required = set(schema.get('required') or [])
    data: Dict[str, Any] = {}
    for name, prop in props.items():
        if name in required:
            if isinstance(prop, Mapping) and 'enum' in prop:
                data[name] = prop['enum'][0]
            else:
                data[name] = sample_for_type(prop if isinstance(prop, Mapping) else 'string', defs)
    return data

def topic_options(message: Mapping[str, Any]) -> tuple[str,int,bool]:
    po = message.get('protocoloptions') or {}
    props = po.get('properties') or {}
    topic = po.get('topic_name') or po.get('topic') or props.get('topic')
    if isinstance(topic, Mapping): topic = topic.get('value')
    return str(topic), int(po.get('qos', props.get('qos', 1))), bool(po.get('retain', props.get('retain', False)))

def iter_contracts(protocol_prefix: str) -> Iterable[Dict[str, Any]]:
    manifest = load_manifest()
    for endpoint in manifest.get('endpoints', {}).values():
        if not str(endpoint.get('protocol','')).upper().startswith(protocol_prefix.upper()):
            continue
        for group_ref in endpoint.get('messagegroups', []):
            group = resolve_pointer(manifest, group_ref)
            for key, m in (group.get('messages') or {}).items():
                msg = resolve_message(manifest, m)
                ce = msg.get('envelopemetadata') or {}
                schema = resolve_pointer(manifest, msg['dataschemauri'])
                version = schema.get('defaultversionid','1')
                jschema = schema['versions'][version]['schema']
                data = sample_from_schema(jschema)
                context = dict(DEFAULTS)
                context.update(data if isinstance(data, dict) else {})
                subject = render((ce.get('subject') or {}).get('value'), context) or 'sample'
                _merge_subject_context((ce.get('subject') or {}).get('value'), subject, context)
                ce_type = (ce.get('type') or {}).get('value') or key
                source = render((ce.get('source') or {}).get('value'), context) or f"https://example.invalid/{PROJECT_DIR}"
                ce_id = render((ce.get('id') or {}).get('value'), context) or str(uuid.uuid4())
                ce_time = render((ce.get('time') or {}).get('value'), context) or NOW
                for pname in set(TEMPLATE_RE.findall(subject) + TEMPLATE_RE.findall(source) + TEMPLATE_RE.findall(ce_id) + TEMPLATE_RE.findall(ce_time)):
                    context.setdefault(pname, DEFAULTS.get(pname, f"sample-{pname.replace('_','-')}"))
                if isinstance(data, dict):
                    for k,v in context.items(): data.setdefault(k, v)
                yield {"type": ce_type, "source": source, "subject": subject, "id": ce_id, "time": ce_time, "data": data, "message": msg, "context": context}

def _merge_subject_context(template: str | None, rendered: str, context: Dict[str, Any]) -> None:
    if not template:
        return
    names = TEMPLATE_RE.findall(template)
    pattern = '^' + re.escape(template) + '$'
    for name in names:
        pattern = pattern.replace('\\{' + name + '\\}', f'(?P<{name}>[^/]+)')
    match = re.match(pattern, rendered)
    if match:
        context.update(match.groupdict())

def mqtt_feed() -> None:
    import paho.mqtt.client as mqtt
    from paho.mqtt.client import CallbackAPIVersion, MQTTv5
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    from urllib.parse import urlparse
    url = os.getenv('MQTT_BROKER_URL') or f"mqtt://{os.getenv('MQTT_HOST','localhost')}:{os.getenv('MQTT_PORT','1883')}"
    parsed = urlparse(url if '://' in url else f'mqtt://{url}')
    host = parsed.hostname or 'localhost'; port = parsed.port or (8883 if parsed.scheme == 'mqtts' else 1883)
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if os.getenv('MQTT_USERNAME'):
        client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD',''))
    if parsed.scheme == 'mqtts' or os.getenv('MQTT_TLS','').lower() in ('1','true','yes'):
        client.tls_set()
    client.connect(host, port, 30); client.loop_start(); time.sleep(0.5)
    for c in iter_contracts('MQTT'):
        topic, qos, retain = topic_options(c['message'])
        topic = render(topic, {**c['context'], **(c['data'] if isinstance(c['data'],dict) else {})})
        props = Properties(PacketTypes.PUBLISH)
        props.ContentType = 'application/json'
        props.UserProperty = [('specversion','1.0'),('type',c['type']),('source',c['source']),('subject',c['subject']),('id',c['id']),('time',c['time'])]
        client.publish(topic, json.dumps(c['data'], ensure_ascii=False).encode('utf-8'), qos=qos, retain=retain, properties=props).wait_for_publish()
    time.sleep(1.0); client.loop_stop(); client.disconnect()

def amqp_feed() -> None:
    from proton import Message
    from proton.utils import BlockingConnection
    from urllib.parse import quote
    host=os.getenv('AMQP_HOST','localhost'); port=int(os.getenv('AMQP_PORT','5672')); address=os.getenv('AMQP_ADDRESS') or PROJECT_DIR
    user=os.getenv('AMQP_USERNAME'); pwd=os.getenv('AMQP_PASSWORD') or ''
    auth = f"{quote(user)}:{quote(pwd)}@" if user else ''
    conn=BlockingConnection(f"amqp://{auth}{host}:{port}", timeout=30, allowed_mechs='PLAIN' if user else None)
    sender=conn.create_sender(address)
    for c in iter_contracts('AMQP'):
        props={f'cloudEvents:{k}':str(v) for k,v in {'specversion':'1.0','type':c['type'],'source':c['source'],'subject':c['subject'],'id':c['id'],'time':c['time']}.items()}
        sender.send(Message(body=json.dumps(c['data'], ensure_ascii=False), subject=c['subject'], properties=props, content_type='application/json'))
    conn.close()

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('command', nargs='?', default='feed'); parser.add_argument('--once', action='store_true')
    args=parser.parse_args()
    if args.command != 'feed': parser.error("only 'feed' is supported")
    if TRANSPORT == 'mqtt': mqtt_feed()
    else: amqp_feed()
if __name__ == '__main__': main()
