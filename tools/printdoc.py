r"""Generate prose-first GitHub-flavored EVENTS.md from xRegistry manifests."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Environment, BaseLoader

Json = dict[str, Any]
VALIDATION_KEYS = {"pattern","format","minimum","maximum","exclusiveMinimum","exclusiveMaximum","minLength","maxLength","minItems","maxItems","uniqueItems","const","default","examples"}
EXTENSION_KEYS = {"unit","symbol","altnames","altenums","alternates","descriptions","choices","values"}
COMMON_SCHEMA_KEYS = {"$schema","$id","$root","$uses","$ref","name","namespace","doc","description","type","required","properties","fields","definitions","items","additionalProperties","enum","symbols","ordinals","logicalType","ce_type"} | VALIDATION_KEYS | EXTENSION_KEYS
KNOWN_TOP_KEYS={"name","version","description","documentation","endpoints","messagegroups","schemagroups"}
KNOWN_ENDPOINT_KEYS={"usage","protocol","envelope","envelopeoptions","protocoloptions","protocolmetadata","messagegroups","messagegroup","description","endpoints","deployed"}
KNOWN_MESSAGEGROUP_KEYS={"id","messagegroupid","name","description","envelope","messages","createdat","modifiedat","epoch"}
KNOWN_MESSAGE_KEYS={"id","messageid","name","description","envelope","envelopemetadata","dataschemaformat","dataschemauri","basemessageurl","basemessage","protocol","protocoloptions","protocolmetadata","createdat","modifiedat","epoch"}
KNOWN_SCHEMA_CONTAINER_KEYS={"name","format","defaultversionid","versions","schemaid","description"}
KNOWN_SCHEMA_VERSION_KEYS={"format","schema","createdat","modifiedat","versionid","schemaid","epoch","name","description"}

TEMPLATE = r"""
# {{ title }}

{{ summary }}

## At a glance

- **Event types:** {{ glance.event_count }} documented event type{{ '' if glance.event_count == 1 else 's' }}{% if glance.variant_count != glance.event_count %} ({{ glance.variant_count }} transport binding{{ '' if glance.variant_count == 1 else 's' }} in the manifest){% endif %}.
- **Transports:** {{ glance.transports or 'No transport endpoint is declared.' }}
- **Reference vs telemetry:** {{ glance.reference_count }} reference/catalog event type{{ '' if glance.reference_count == 1 else 's' }} and {{ glance.telemetry_count }} telemetry event type{{ '' if glance.telemetry_count == 1 else 's' }}.
- **Identity:** {{ glance.identity }}
{% if operational_summary %}- **Operations:** {{ operational_summary }}
{% endif %}- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

{% if quick.kafka %}
### Kafka

Subscribe to {{ quick.kafka.topics_text }}. The record key is {{ quick.kafka.keys_text }}. {{ quick.kafka.key_explanation }} Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe({{ quick.kafka.topics_list }})
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
{% endif %}
{% if quick.mqtt %}
### MQTT 5

Connect to {{ quick.mqtt.brokers_text }} and subscribe to {{ quick.mqtt.filters_text }}. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe({{ quick.mqtt.subscribe_arg }})
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
{% endif %}
{% if quick.amqp %}
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is {{ quick.amqp.addresses_text }}. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/{{ quick.amqp.sample_address }}')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.
{% endif %}
{% if not quick.kafka and not quick.mqtt and not quick.amqp %}
No concrete transport endpoint is declared in this manifest.
{% endif %}

## Event catalog

{% for event in events %}
### {{ event.heading }}

CloudEvents type: `{{ event.ce_type }}`

#### What it tells you

{{ event.what }}

#### Identity

{{ event.identity_text }}

#### Where to find it

{% if event.where_rows %}
| Transport | Location |
| --- | --- |
{% for row in event.where_rows %}
| {{ row.transport }} | {{ row.location }} |
{% endfor %}
{% else %}
No transport binding is declared for this event type.
{% endif %}

#### Payload

{{ event.payload_intro }}

{% for field in event.fields %}
- **`{{ field.name }}`** ({{ field.type }}, {{ field.required }}{% if field.unit %}, {{ field.unit }}{% endif %}): {{ field.description }}{% if field.validation %} {{ field.validation }}{% endif %}{% if field.link %} See [{{ field.link_label }}](#{{ field.link }}).{% endif %}
{% endfor %}
{% if event.enums %}
{% for enum in event.enums %}
##### `{{ enum.field }}` values

{% for val in enum.values %}
- `{{ val.value }}`{% if val.label %} — {{ val.label }}{% endif %}{% if val.description %}: {{ val.description }}{% endif %}
{% endfor %}
{% endfor %}
{% endif %}
{% for nested in event.nested %}
##### {{ nested.name }}
<a id="{{ nested.anchor }}"></a>

{{ nested.description }}

{% for field in nested.fields %}
- **`{{ field.name }}`** ({{ field.type }}, {{ field.required }}{% if field.unit %}, {{ field.unit }}{% endif %}): {{ field.description }}{% if field.validation %} {{ field.validation }}{% endif %}{% if field.link %} See [{{ field.link_label }}](#{{ field.link }}).{% endif %}
{% endfor %}
{% endfor %}

#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{{ event.example_json }}
```

#### Reference vs telemetry

{{ event.role_note }}

{% endfor %}
## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

{% if operational_notes %}
{% for note in operational_notes %}
- {{ note }}
{% endfor %}
{% else %}
No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.
{% endif %}

## References

- xRegistry manifest: [`{{ manifest_rel }}`]({{ manifest_rel }})
{% if has_readme %}- Source README: [`README.md`](README.md)
{% endif %}{% if has_container %}- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
{% endif %}{% for ref in references %}
- {{ ref }}
{% endfor %}
"""

@dataclass
class WarningCollector:
    paths: set[str] = field(default_factory=set)
    def warn(self, p: str) -> None: self.paths.add(p)
    def missing(self, p: str, what: str="description") -> None: self.paths.add(f"missing {what}: {p}")
    def emit(self) -> None:
        for p in sorted(self.paths): print(f"WARNING: {p}", file=sys.stderr)

@dataclass
class Ctx:
    data: Json
    manifest_path: Path|None = None
    title_arg: str|None = None
    description_arg: str|None = None
    warnings: WarningCollector = field(default_factory=WarningCollector)
    endpoints_by_group: dict[str, list[tuple[str, Json]]] = field(default_factory=dict)
    source_dir: Path|None = None
    readme_text: str = ""
    container_text: str = ""
    def __post_init__(self) -> None:
        for eid,e in (self.data.get("endpoints") or {}).items():
            for ref in nlist(e.get("messagegroups") or e.get("messagegroup")):
                self.endpoints_by_group.setdefault(ref_id(str(ref)), []).append((eid,e))
        if self.manifest_path and self.manifest_path.parent.name.lower()=="xreg":
            self.source_dir=self.manifest_path.parent.parent
            self.readme_text=read_text(self.source_dir/"README.md")
            self.container_text=read_text(self.source_dir/"CONTAINER.md")

@dataclass
class FieldDoc:
    name: str; type: str; required: str; unit: str; description: str; validation: str=""; link: str=""; link_label: str=""

@dataclass
class EnumDoc:
    field: str; values: list[dict[str,str]]

@dataclass
class NestedDoc:
    name: str; anchor: str; description: str; fields: list[FieldDoc]

@dataclass
class EventDoc:
    heading: str; ce_type: str; what: str; identity_text: str; where_rows: list[dict[str,str]]; payload_intro: str; fields: list[FieldDoc]; enums: list[EnumDoc]; nested: list[NestedDoc]; example_json: str; role_note: str


def main() -> None:
    p=argparse.ArgumentParser(description="Generate prose-first EVENTS.md from an xRegistry JSON manifest.")
    p.add_argument("manifest_file")
    p.add_argument("--title")
    p.add_argument("--description")
    p.add_argument("--output")
    a=p.parse_args()
    path=Path(a.manifest_file)
    data=json.loads(path.read_text(encoding="utf-8"))
    if (a.title or a.description) and not os.environ.get("PRINTDOC_SUPPRESS_COMPAT_NOTICE"):
        print("NOTICE: --title/--description are still supported; omit them to use xRegistry/README-derived defaults.", file=sys.stderr)
    doc,warnings=generate_documentation(data, a.title, a.description, path)
    warnings.emit()
    if a.output:
        out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding="utf-8", newline="\n")
    else:
        print(doc, end="")


def generate_documentation(data: Json, title: str|None=None, description: str|None=None, manifest_path: Path|None=None) -> tuple[str, WarningCollector]:
    ctx=Ctx(data=data, manifest_path=manifest_path, title_arg=title, description_arg=description)
    warn_unknowns(data, ctx.warnings); warn_missing_descriptions(ctx)
    events=build_events(ctx)
    protocols=protocols_declared(data)
    quick=build_quick(ctx, events)
    refs=extract_references(ctx)
    operational_notes=extract_operational_notes(ctx)
    summary=description or default_description(ctx) or f"This document describes the CloudEvents emitted by {registry_name(data)}."
    rendered=Environment(loader=BaseLoader(), trim_blocks=True, lstrip_blocks=True).from_string(TEMPLATE.lstrip()).render(
        title=title or default_title(ctx), summary=clean_para(summary),
        glance={
            "event_count": len(events), "variant_count": count_messages(data),
            "transports": ", ".join(protocols) if protocols else "",
                "reference_count": sum(1 for e in events if e.role_note.startswith("This is reference")),
                "telemetry_count": sum(1 for e in events if e.role_note.startswith("This is telemetry")),
            "identity": identity_summary(events),
        },
        operational_summary=(operational_notes[0] if operational_notes else ""), quick=quick, events=events,
        operational_notes=operational_notes, manifest_rel=manifest_rel(ctx), has_readme=bool(ctx.readme_text), has_container=bool(ctx.container_text), references=refs)
    rendered = re.sub(r'(?<!\n)(- \*\*`)', r'\n\1', rendered)
    rendered = re.sub(r'(?<!\n)(- `)', r'\n\1', rendered)
    rendered = re.sub(r'(?<![#\n])(#{2,6} )', r'\n\1', rendered)
    return rendered.strip()+"\n", ctx.warnings


def default_title(ctx: Ctx) -> str:
    if isinstance(ctx.data.get("name"),str) and ctx.data["name"].strip(): return ctx.data["name"].strip()+" Events"
    h=first_heading(ctx.readme_text)
    if h: return h.strip()+" Events"
    if ctx.manifest_path and ctx.manifest_path.parent.name.lower()=="xreg": return human(ctx.manifest_path.parent.parent.name)+" Events"
    return "Bridge Events"

def default_description(ctx: Ctx) -> str:
    if isinstance(ctx.data.get("description"),str) and ctx.data["description"].strip(): return ctx.data["description"].strip()
    para=first_paragraph(ctx.readme_text)
    if para: return para
    doc=ctx.data.get("documentation")
    if isinstance(doc,str): return doc.strip()
    if isinstance(doc,dict):
        for k in ("description","url","uri"):
            if isinstance(doc.get(k),str): return doc[k].strip()
    for g in (ctx.data.get("messagegroups") or {}).values():
        if isinstance(g,dict) and isinstance(g.get("description"),str): return g["description"].strip()
    return ""

def build_events(ctx: Ctx) -> list[EventDoc]:
    collected: dict[str, dict[str,Any]] = {}
    groups=ctx.data.get("messagegroups") or {}
    for gid,g in groups.items():
        if not isinstance(g,dict): continue
        for mid,msg in (g.get("messages") or {}).items():
            if not isinstance(msg,dict): continue
            resolved,chain=resolve_message_chain(msg, groups)
            ce=ce_type(resolved, mid)
            slot=collected.setdefault(ce,{"gid":gid,"mid":mid,"resolved":resolved,"variants":[]})
            if not slot["resolved"].get("dataschemauri") and resolved.get("dataschemauri"): slot["resolved"]=resolved; slot["gid"]=gid; slot["mid"]=mid
            slot["variants"].append((gid,mid,msg,resolved))
    return [event_doc(ctx, v) for v in collected.values()]

def event_doc(ctx: Ctx, item: dict[str,Any]) -> EventDoc:
    resolved=item["resolved"]; ce=ce_type(resolved,item["mid"]); heading=human(resolved.get("name") or ce.split('.')[-1])
    schema=resolve_schema(resolved.get("dataschemauri"), ctx.data.get("schemagroups") or {})
    root=resolve_root(schema) if isinstance(schema,dict) else {}
    desc=clean_para(resolved.get("description") or root.get("description") or "No description provided.")
    what=join_sentences(desc, clean_para(root.get("description") if root.get("description") != resolved.get("description") else ""), max_sent=3)
    if not informative_description(what, heading):
        what=f"This event carries {heading.lower()} data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest."
    subject=metadata_value(resolved,"subject") or infer_subject_from_variants(item["variants"])
    identity_text=identity_text_for(subject, resolved, root)
    where=where_rows(ctx, item["variants"], subject)
    fields,enums,nested=schema_docs(root, schema or {}, ctx.warnings, ce)
    payload_intro=payload_intro_for(heading, root, fields)
    example=json.dumps(example_for_schema(root, schema or {}, set()), indent=2, ensure_ascii=False)
    role=role_note(item["variants"], resolved)
    return EventDoc(heading,ce,what,identity_text,where,payload_intro,fields,enums,nested,example,role)


def where_rows(ctx: Ctx, variants: list[tuple[str,str,Json,Json]], subject: str|None) -> list[dict[str,str]]:
    rows=[]; seen=set()
    for gid,mid,msg,resolved in variants:
        for eid,e in ctx.endpoints_by_group.get(gid,[]):
            proto=str(e.get("protocol","")); up=proto.upper(); loc=""
            eopts=e.get("protocoloptions") if isinstance(e.get("protocoloptions"),dict) else {}; opts=eopts.get("options") if isinstance(eopts.get("options"),dict) else {}
            mopts=msg.get("protocoloptions") if isinstance(msg.get("protocoloptions"),dict) else {}
            if "KAFKA" in up:
                loc=f"topic {code_inline(opts.get('topic') or eopts.get('topic') or 'not declared')}, key {code_inline(opts.get('key') or eopts.get('key') or metadata_value(resolved,'partitionkey') or subject or 'not declared')}"
            elif "MQTT" in up:
                topic=mopts.get("topic_name") or mopts.get("topic") or eopts.get("topic") or "not declared"; qos=mopts.get("qos", eopts.get("qos","not declared")); retain=mopts.get("retain", eopts.get("retain","not declared"))
                loc=f"topic {code_inline(topic)}, retain {code_inline(str(retain).lower())}, QoS {code_inline(qos)}"
            elif "AMQP" in up:
                props=mopts.get("properties") if isinstance(mopts.get("properties"),dict) else {}; aps=mopts.get("application_properties") if isinstance(mopts.get("application_properties"),dict) else {}
                addr=mopts.get("address") or mopts.get("address_name") or eopts.get("address") or ((eopts.get("endpoints") or [{}])[0].get("uri") if isinstance(eopts.get("endpoints"),list) and eopts.get("endpoints") else None) or "broker-configured node"
                subj=(props.get("subject") or {}).get("value") if isinstance(props.get("subject"),dict) else subject
                apbits=[f"{k} {template_value(v)}" for k,v in aps.items()]
                loc=f"source address {code_inline(addr)}, message subject {code_inline(subj or 'not declared')}" + ("; application properties " + ", ".join(apbits) if apbits else "")
            else: loc=f"endpoint `{eid}`"
            key=(proto,loc)
            if key not in seen: rows.append({"transport": code_inline(proto or eid), "location": loc}); seen.add(key)
    return rows


def schema_docs(root: Json, doc: Json, warnings: WarningCollector, prefix: str) -> tuple[list[FieldDoc], list[EnumDoc], list[NestedDoc]]:
    q: list[tuple[str,Json]]=[]; enums=[]; nested=[]
    fields=fields_for_node(root, doc, q, enums, warnings, prefix)
    seen={id(root)}
    while q:
        name,node=q.pop(0)
        if id(node) in seen: continue
        seen.add(id(node))
        nested.append(NestedDoc(name=name, anchor=f"payload-{anchor(prefix+'-'+name)}", description=clean_para(node.get("description") or "Nested record."), fields=fields_for_node(node, doc, q, enums, warnings, prefix+"."+name)))
    return fields,enums,nested

def fields_for_node(node: Json, doc: Json, q: list[tuple[str,Json]], enums: list[EnumDoc], warnings: WarningCollector, path: str) -> list[FieldDoc]:
    if not is_obj(node): return []
    req=set(node.get("required") or []); out=[]
    for fn,fs0 in (node.get("properties") or {}).items():
        fs=fs0 if isinstance(fs0,dict) else {"type":fs0}
        target=resolve_field_target(fs,doc)
        link=""; link_label=""
        if isinstance(target,dict) and target is not fs and is_obj(target):
            nm=str(target.get("name") or fn); q.append((nm,target)); link=f"payload-{anchor(path+'.'+nm)}"; link_label=nm
        elif isinstance(target,dict) and is_obj(target):
            nm=str(target.get("name") or fn); q.append((nm,target)); link=f"payload-{anchor(path+'.'+nm)}"; link_label=nm
        desc=clean_para(fs.get("description") or (target.get("description") if isinstance(target,dict) else "") or "No description provided.")
        if desc == "No description provided.": warnings.missing(f"schema field {path}.{fn}")
        if has_enum(fs): enums.append(enum_doc(fn, fs))
        elif isinstance(target,dict) and has_enum(target): enums.append(enum_doc(fn, target))
        out.append(FieldDoc(fn, type_name(fs, doc), "required" if fn in req else "optional", unit_text(fs), desc, validation_text(fs), link, link_label))
    return out


def enum_doc(field: str, node: Json) -> EnumDoc:
    vals=node.get("enum") or node.get("symbols") or []
    desc=node.get("descriptions") if isinstance(node.get("descriptions"),dict) else {}
    alt=node.get("altenums") if isinstance(node.get("altenums"),dict) else {}
    out=[]
    for v in vals:
        key=str(v); label=""; explanation=""
        if key in desc: explanation=str(desc[key])
        elif v in desc: explanation=str(desc[v])
        if isinstance(alt.get("lang:en"),dict): label=str(alt["lang:en"].get(key) or alt["lang:en"].get(v) or "")
        elif key in alt: label=str(alt[key])
        elif v in alt: label=str(alt[v])
        out.append({"value": key, "label": clean_para(label), "description": clean_para(explanation)})
    return EnumDoc(field,out)


def build_quick(ctx: Ctx, events: list[EventDoc]) -> dict[str,Any]:
    endpoints=ctx.data.get("endpoints") or {}; out={"kafka":None,"mqtt":None,"amqp":None}
    topics=[]; keys=[]; brokers=[]; filters=[]; addrs=[]
    for _,e in endpoints.items():
        proto=str(e.get("protocol","")); opts=e.get("protocoloptions") if isinstance(e.get("protocoloptions"),dict) else {}; options=opts.get("options") if isinstance(opts.get("options"),dict) else {}
        if "KAFKA" in proto.upper(): topics.append(options.get("topic") or opts.get("topic")); keys.append(options.get("key") or opts.get("key"))
        if "MQTT" in proto.upper():
            for ep in opts.get("endpoints") or []:
                if isinstance(ep,dict) and ep.get("uri"): brokers.append(ep["uri"])
        if "AMQP" in proto.upper():
            if opts.get("address"): addrs.append(opts.get("address"))
            for ep in opts.get("endpoints") or []:
                if isinstance(ep,dict) and ep.get("uri"): addrs.append(amqp_path(ep["uri"]))
    for groups in (ctx.data.get("messagegroups") or {}).values():
        for msg in (groups.get("messages") if isinstance(groups,dict) else {} or {}).values():
            if isinstance(msg,dict):
                mo=msg.get("protocoloptions") if isinstance(msg.get("protocoloptions"),dict) else {}
                if mo.get("topic_name") or mo.get("topic"): filters.append(mqtt_filter(mo.get("topic_name") or mo.get("topic")))
                if mo.get("address") or mo.get("address_name"): addrs.append(mo.get("address") or mo.get("address_name"))
    topics=uniq([x for x in topics if x]); keys=uniq([x for x in keys if x]); brokers=uniq(brokers or ["mqtt://localhost:1883"] if any("MQTT" in str(e.get("protocol","")).upper() for e in endpoints.values()) else [])
    filters=uniq(filters); addrs=uniq([x for x in addrs if x])
    if topics: out["kafka"]={"topics_text": ", ".join(code_inline(t) for t in topics), "topics_list": repr(topics), "keys_text": ", ".join(code_inline(k) for k in keys) if keys else "not declared", "key_explanation": key_explanation(keys, events)}
    if brokers or filters: out["mqtt"]={"brokers_text": ", ".join(code_inline(b) for b in brokers), "filters_text": ", ".join(code_inline(f) for f in filters) if filters else "the topic filters documented per event below", "subscribe_arg": repr((filters[0] if filters else "#", 1))}
    if addrs or any("AMQP" in str(e.get("protocol","")).upper() for e in endpoints.values()):
        sample=(addrs[0] if addrs else "events").strip('/') or "events"; out["amqp"]={"addresses_text": ", ".join(code_inline(a) for a in (addrs or ["broker-configured address"])), "sample_address": sample}
    return out


def extract_operational_notes(ctx: Ctx) -> list[str]:
    text="\n".join([ctx.readme_text, ctx.container_text])
    low=text.lower(); notes=[]
    m=re.search(r"default\s+`?(\d+)`?\s*(?:s|sec|seconds)", text, re.I)
    if m and "poll" in low: notes.append(f"The checked-in guide documents a default polling interval of {m.group(1)} seconds.")
    if "etag" in low: notes.append("The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.")
    if "dedupe" in low or "dedup" in low: notes.append("The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.")
    if "retained" in low and "qos 1" in low: notes.append("The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.")
    if "startup" in low and ("station" in low or "catalog" in low or "metadata" in low): notes.append("Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.")
    return uniq(notes)[:5]

def extract_references(ctx: Ctx) -> list[str]:
    refs=[]; doc=ctx.data.get("documentation")
    def add(label: str, url: str):
        if url and url.startswith(("http://","https://")) and url not in "\n".join(refs): refs.append(f"{label}: <{url}>")
    if isinstance(doc,str): add("Upstream/documentation", doc)
    elif isinstance(doc,dict):
        for k,v in doc.items():
            if isinstance(v,str): add(human(k), v)
    for text in (ctx.readme_text, ctx.container_text):
        for label,url in re.findall(r"\[([^\]]{2,80})\]\((https?://[^)\s]+)\)", text):
            if any(w in label.lower() for w in ("api","docs","documentation","opendata","pegelonline","platform","service")): add(label, url)
            if len(refs) >= 8: return refs
    return refs

# Schema and manifest helpers

def resolve_message_chain(msg: Json, groups: Json) -> tuple[Json,list[str]]:
    merged=dict(msg); chain=[]; ref=msg.get("basemessageurl")
    if isinstance(ref,str):
        base=resolve_base(ref,groups)
        if base:
            bmerged,bchain=resolve_message_chain(base,groups); chain=bchain+[ref]
            meta=dict(bmerged.get("envelopemetadata") or {}); meta.update(merged.get("envelopemetadata") or {})
            tmp=dict(bmerged); tmp.update(merged); tmp["envelopemetadata"]=meta; merged=tmp
    return merged, chain

def resolve_base(ref: str, groups: Json) -> Json|None:
    p=ref.lstrip('/').split('/')
    return (((groups.get(p[1]) or {}).get("messages") or {}).get(p[3])) if len(p)>=4 and p[0]=="messagegroups" and p[2]=="messages" else None

def resolve_schema(uri: str|None, schemagroups: Json) -> Json|None:
    if not uri or not uri.startswith("#/"): return None
    node: Any={"schemagroups":schemagroups}
    for p in uri[2:].split('/'):
        node=node.get(p) if isinstance(node,dict) else None
    if not isinstance(node,dict): return None
    versions=node.get("versions") or {}
    return versions[sorted(versions.keys(),key=version_key)[-1]].get("schema") if versions else node.get("schema")

def resolve_root(schema: Json|None) -> Json:
    if not isinstance(schema,dict): return {}
    r=schema.get("$root"); target=ptr(schema,r) if isinstance(r,str) else None
    return target if isinstance(target,dict) else schema

def ptr(doc: Json, pointer: str|None) -> Any:
    if not pointer or not pointer.startswith("#/"): return None
    node: Any=doc
    for raw in pointer[2:].split('/'):
        if not isinstance(node,dict): return None
        node=node.get(raw.replace("~1","/").replace("~0","~"))
    return node

def resolve_field_target(fs: Json, doc: Json) -> Any:
    if isinstance(fs.get("$ref"),str): return ptr(doc,fs["$ref"])
    t=fs.get("type")
    if isinstance(t,dict) and isinstance(t.get("$ref"),str): return ptr(doc,t["$ref"])
    if isinstance(t,list):
        for x in t:
            if isinstance(x,dict): return resolve_field_target({"type":x},doc) or x
    return fs

def example_for_schema(node: Any, doc: Json, seen: set[int]) -> Any:
    if isinstance(node,dict):
        if "const" in node: return node["const"]
        if "default" in node and node["default"] is not None: return node["default"]
        if isinstance(node.get("examples"),list) and node["examples"]: return node["examples"][0]
        target=resolve_field_target(node,doc)
        if isinstance(target,dict) and target is not node: return example_for_schema(target,doc,seen)
        if has_enum(node): return (node.get("enum") or node.get("symbols") or ["string"])[0]
        t=node.get("type")
        if isinstance(t,list):
            non=[x for x in t if x != "null"]
            return example_for_schema({"type": non[0] if non else "null"},doc,seen)
        if t in ("datetime","date-time") or node.get("format")=="date-time": return "2024-01-01T00:00:00Z"
        if t in ("string","uri","uritemplate") or not t and not node.get("properties"): return "string"
        if t in ("integer","int","int8","int16","int32","int64","long","float","double","number"): return 0
        if t == "boolean": return False
        if t == "array": return [example_for_schema(node.get("items",{"type":"string"}),doc,seen)]
        if is_obj(node):
            if id(node) in seen: return {}
            seen.add(id(node)); return {k: example_for_schema(v if isinstance(v,dict) else {"type":v},doc,seen) for k,v in (node.get("properties") or {}).items()}
    if isinstance(node,str): return example_for_schema({"type":node},doc,seen)
    return None

# Text/render helpers

def ce_type(msg: Json, fallback: str) -> str: return str(metadata_value(msg,"type") or fallback)
def metadata_value(msg: Json, name: str) -> str|None:
    md=msg.get("envelopemetadata") if isinstance(msg.get("envelopemetadata"),dict) else {}; v=md.get(name)
    if isinstance(v,dict): return str(v.get("value")) if v.get("value") is not None else None
    return str(v) if v is not None else None

def role_note(variants: list[tuple[str,str,Json,Json]], resolved: Json) -> str:
    name=str(resolved.get("name", "")).lower()
    text=(name + " " + str(resolved.get("description", ""))).lower()
    retained=any((msg.get("protocoloptions") if isinstance(msg.get("protocoloptions"),dict) else {}).get("retain") is True for _,_,msg,_ in variants)
    if any(w in name for w in ("measurement","reading","observation","position","alert","event")) or any(w in text for w in (" telemetry","live ","latest ","current ","candidate")):
        return "This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history."
    if any(w in name for w in ("station","catalog","metadata","status","configuration","reference")) or any(w in text for w in ("reference catalog","station catalog","configuration")):
        suffix=" MQTT may retain the latest copy so late subscribers can build local context immediately." if retained else ""
        return "This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity."+suffix
    return "This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog."

def identity_text_for(subject: str|None, msg: Json, root: Json) -> str:
    if not subject: return "No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below."
    names=re.findall(r"{([^}]+)}", subject); parts=[]
    props=root.get("properties") if isinstance(root.get("properties"),dict) else {}
    for n in names:
        d=(props.get(n) or {}).get("description") if isinstance(props.get(n),dict) else ""
        bit = decap(first_sentence(d)).rstrip('.') if d else 'a payload field with the same name'
        parts.append(f"`{{{n}}}` is {bit}")
    return f"Each event identifies the real-world resource with `{subject}`. " + ("; ".join(parts)+". " if parts else "") + "That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them."

def identity_summary(events: list[EventDoc]) -> str:
    vals=[]
    for e in events:
        m=re.search(r"with `([^`]+)`", e.identity_text)
        if m: vals.append(m.group(1))
    vals=uniq(vals)
    return (", ".join(code_inline(v) for v in vals) + " identifies the resource each event is about.") if vals else "Each event documents its subject/key identity in the catalog below."

def infer_subject_from_variants(variants: list[tuple[str,str,Json,Json]]) -> str|None:
    for _,_,_,r in variants:
        v=metadata_value(r,"subject")
        if v: return v
    return None

def payload_intro_for(name: str, root: Json, fields: list[FieldDoc]) -> str:
    req=[f.name for f in fields if f.required=="required"]
    base=f"`{name}` payloads are JSON {type_name(root,{})}."
    return base + (" Required fields: " + ", ".join(f"`{x}`" for x in req) + "." if req else " No required field list is declared.")

def key_explanation(keys: list[str], events: list[EventDoc]) -> str:
    if len(keys)==1: return f"In plain language, {code_inline(keys[0])} is the stable identity of the resource described by the event."
    return "Each key template is explained in the event catalog below."

def type_name(s: Any, doc: Json) -> str:
    if isinstance(s,str): return s
    if not isinstance(s,dict): return "schema"
    target=resolve_field_target(s,doc)
    if isinstance(target,dict) and target is not s: return type_name(target,doc)
    t=s.get("type")
    if isinstance(t,list): return " or ".join(type_name(x,doc) for x in t)
    if isinstance(t,dict): return type_name(t,doc)
    if has_enum(s): return "enum"
    if t=="array": return "array of "+type_name(s.get("items",{}),doc)
    if is_obj(s): return "object"
    return str(t or "schema")

def has_enum(s: Json) -> bool: return "enum" in s or "symbols" in s or s.get("type")=="enum"
def is_obj(s: Json) -> bool: return isinstance(s,dict) and (s.get("type")=="object" or (isinstance(s.get("type"),list) and "object" in s.get("type")) or "properties" in s)
def unit_text(s: Json) -> str:
    unit=str(s.get("unit") or ""); sym=str(s.get("symbol") or "")
    return unit if unit and (not sym or sym == unit) else (f"{unit} ({sym})" if unit and sym else (unit or sym))
def validation_text(s: Json) -> str:
    bits=[]
    for k in ("minimum","maximum","exclusiveMinimum","exclusiveMaximum","minLength","maxLength","pattern","format"):
        if k in s: bits.append(f"{k} `{s[k]}`")
    return "Constraints: "+", ".join(bits)+"." if bits else ""
def template_value(v: Any) -> str:
    return code_inline(v.get("value")) if isinstance(v,dict) and v.get("value") is not None else code_inline(v)

def protocols_declared(data: Json) -> list[str]: return uniq([str(e.get("protocol")) for e in (data.get("endpoints") or {}).values() if e.get("protocol")])
def count_messages(data: Json) -> int: return sum(len((g or {}).get("messages") or {}) for g in (data.get("messagegroups") or {}).values())
def registry_name(data: Json) -> str: return str(data.get("name") or "this source")
def manifest_rel(ctx: Ctx) -> str: return "xreg/"+ctx.manifest_path.name if ctx.manifest_path else "xreg manifest"
def read_text(p: Path) -> str: return p.read_text(encoding="utf-8") if p.exists() else ""
def first_heading(text: str) -> str:
    m=re.search(r"^#\s+(.+)$", text, re.M); return m.group(1).strip() if m else ""
def first_paragraph(text: str) -> str:
    lines=text.splitlines(); seen=False; para=[]
    for line in lines:
        if not seen:
            if line.startswith("# "): seen=True
            continue
        if not line.strip():
            if para: break
            continue
        if re.match(r"^(#|```|\||!\[)", line):
            if para: break
            continue
        para.append(line.strip())
    return clean_para(" ".join(para))
def clean_para(v: Any) -> str: return re.sub(r"\s+", " ", str(v or "")).strip()
def first_sentence(s: str) -> str:
    s=clean_para(s)
    protected=s.replace("e.g.", "e§g§").replace("i.e.", "i§e§")
    parts=re.split(r"(?<=[.!?])\s+", protected, maxsplit=1)
    return (parts[0] if parts else protected).replace("e§g§", "e.g.").replace("i§e§", "i.e.")

def join_sentences(*parts: str, max_sent: int=3) -> str:
    text=" ".join(p for p in parts if p)
    raw=re.split(r"(?<=[.!?])\s+", text)
    sent=[]; seen=set()
    for item in raw:
        item=item.strip()
        key=item.lower()
        if item and key not in seen:
            sent.append(item); seen.add(key)
    return " ".join(sent[:max_sent]).strip() if sent else (text or "No description provided.")


def informative_description(text: str, heading: str) -> bool:
    t=clean_para(text).strip('.')
    if not t or t.lower()=="no description provided": return False
    squashed=re.sub(r"[^a-z0-9]", "", t.lower())
    h=re.sub(r"[^a-z0-9]", "", heading.lower())
    return bool(squashed and squashed not in {h, h+h})

def human(s: Any) -> str:
    s=str(s); s=re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s.split('.')[-1]); return " ".join(p.capitalize() if not p.isupper() else p for p in re.split(r"[-_\s]+",s) if p)
def anchor(s: str) -> str:
    s=str(s).replace(".", "-")
    return re.sub(r"[\s-]+","-",re.sub(r"[^a-z0-9\s-]","",s.lower())).strip('-')
def decap(s: str) -> str:
    if len(s) > 1 and s[0].isupper() and s[1].isupper(): return s
    return s[:1].lower()+s[1:] if s else s

def code_inline(v: Any) -> str: return "`"+str(v).replace("`","\\`")+"`"
def uniq(xs: list[Any]) -> list[Any]:
    out=[]
    for x in xs:
        if x not in out: out.append(x)
    return out
def nlist(v: Any) -> list[Any]: return [] if v is None else (v if isinstance(v,list) else [v])
def ref_id(ref: str) -> str: return ref.rstrip('/').split('/')[-1] if '/' in ref else ref
def version_key(v: str) -> tuple[int,str]: return (0,f"{int(v):010d}") if str(v).isdigit() else (1,str(v))
def mqtt_filter(topic: str) -> str: return re.sub(r"{[^}/]+}", "+", topic)
def amqp_path(uri: str) -> str:
    m=re.match(r"^[a-z][a-z0-9+.-]*://[^/]+/(.+)$", uri, re.I); return m.group(1) if m else uri

# Warnings

def warn_missing_descriptions(ctx: Ctx) -> None:
    if not default_description(ctx): ctx.warnings.missing("registry", "description")
    for gid,g in (ctx.data.get("messagegroups") or {}).items():
        if not isinstance(g,dict): continue
        for mid,m in (g.get("messages") or {}).items():
            r,_=resolve_message_chain(m, ctx.data.get("messagegroups") or {})
            if not r.get("description"): ctx.warnings.missing(f"message {mid}")
    for sgid,sg in (ctx.data.get("schemagroups") or {}).items():
        for sid,c in ((sg or {}).get("schemas") or {}).items():
            sch=resolve_schema(f"#/schemagroups/{sgid}/schemas/{sid}", ctx.data.get("schemagroups") or {})
            root=resolve_root(sch)
            if isinstance(root,dict) and not root.get("description"): ctx.warnings.missing(f"schema {sid}")

def warn_unknowns(data: Json, w: WarningCollector) -> None:
    warn_keys(data,KNOWN_TOP_KEYS,"unknown xRegistry field not rendered: registry",w)
    for eid,e in (data.get("endpoints") or {}).items():
        if isinstance(e,dict): warn_keys(e,KNOWN_ENDPOINT_KEYS,f"unknown xRegistry field not rendered: endpoints.{eid}",w)
    for gid,g in (data.get("messagegroups") or {}).items():
        if not isinstance(g,dict): continue
        warn_keys(g,KNOWN_MESSAGEGROUP_KEYS,f"unknown xRegistry field not rendered: messagegroups.{gid}",w)
        for mid,m in (g.get("messages") or {}).items():
            if isinstance(m,dict): warn_keys(m,KNOWN_MESSAGE_KEYS,f"unknown xRegistry field not rendered: messagegroups.{gid}.messages.{mid}",w)
    for gid,g in (data.get("schemagroups") or {}).items():
        for sid,c in ((g or {}).get("schemas") or {}).items():
            if isinstance(c,dict):
                warn_keys(c,KNOWN_SCHEMA_CONTAINER_KEYS,f"unknown xRegistry field not rendered: schemagroups.{gid}.schemas.{sid}",w)
                for vid,v in (c.get("versions") or {}).items():
                    if isinstance(v,dict):
                        warn_keys(v,KNOWN_SCHEMA_VERSION_KEYS,f"unknown xRegistry field not rendered: schemagroups.{gid}.schemas.{sid}.versions.{vid}",w)
                        if isinstance(v.get("schema"),dict): warn_schema(v["schema"],f"unknown xRegistry field not rendered: schemagroups.{gid}.schemas.{sid}.versions.{vid}.schema",w)
def warn_keys(o: Json, known: set[str], path: str, w: WarningCollector) -> None:
    for k in o:
        if k not in known: w.warn(f"{path}.{k}")
def warn_schema(node: Any, path: str, w: WarningCollector) -> None:
    if isinstance(node,dict):
        ext=any(m in path for m in (".altnames",".altenums",".alternates",".descriptions",".ordinals")); ns=".definitions" in path and not any(k in node for k in COMMON_SCHEMA_KEYS); dyn=path.endswith(".properties") or ext or ns
        for k,v in node.items():
            if not dyn and k not in COMMON_SCHEMA_KEYS: w.warn(f"{path}.{k}")
            warn_schema(v,f"{path}.{k}",w)
    elif isinstance(node,list):
        for i,v in enumerate(node): warn_schema(v,f"{path}[{i}]",w)

# Backwards-compatible functions used by older tests/importers.
def process_message(msg: Json, schemagroups: Json, messagegroups: Json|None=None) -> list[str]: return [generate_documentation({"messagegroups":{"default":{"messages":{"message":msg}}},"schemagroups":schemagroups})[0]]
def print_schema(schema: Json) -> list[str]: return [json.dumps(schema, indent=2, ensure_ascii=False)]
def generate_anchor(name: str) -> str: return anchor(name)

if __name__ == "__main__": main()
