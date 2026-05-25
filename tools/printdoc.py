r"""Generate GitHub-flavored EVENTS.md from xRegistry manifests.

The companion generate-events-md.ps1 discovers every top-level
<source>\xreg\*.xreg.json file. To add a source, commit the xRegistry manifest;
discovery will pick it up and write <source>\EVENTS.md.
"""
from __future__ import annotations

import argparse, io, json, os, re, sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

Json = dict[str, Any]
VALIDATION_KEYS = {"pattern","format","minimum","maximum","exclusiveMinimum","exclusiveMaximum","minLength","maxLength","minItems","maxItems","uniqueItems","const","default"}
EXTENSION_KEYS = {"unit","symbol","altnames","altenums","alternates","descriptions","choices","values"}
COMMON_SCHEMA_KEYS = {"$schema","$id","$root","$uses","$ref","name","namespace","doc","description","type","required","properties","fields","definitions","items","additionalProperties","enum","symbols","ordinals","logicalType","ce_type"} | VALIDATION_KEYS | EXTENSION_KEYS
KNOWN_TOP_KEYS={"name","version","description","documentation","endpoints","messagegroups","schemagroups"}
KNOWN_ENDPOINT_KEYS={"usage","protocol","envelope","envelopeoptions","protocoloptions","protocolmetadata","messagegroups","messagegroup","description","endpoints","deployed"}
KNOWN_MESSAGEGROUP_KEYS={"id","messagegroupid","name","description","envelope","messages","createdat","modifiedat","epoch"}
KNOWN_MESSAGE_KEYS={"id","messageid","name","description","envelope","envelopemetadata","dataschemaformat","dataschemauri","basemessageurl","basemessage","protocol","protocoloptions","protocolmetadata","createdat","modifiedat","epoch"}
KNOWN_SCHEMA_CONTAINER_KEYS={"name","format","defaultversionid","versions","schemaid","description"}
KNOWN_SCHEMA_VERSION_KEYS={"format","schema","createdat","modifiedat","versionid","schemaid","epoch","name","description"}

@dataclass
class WarningCollector:
    paths: set[str] = field(default_factory=set)
    def warn(self, p: str) -> None: self.paths.add(p)
    def emit(self) -> None:
        for p in sorted(self.paths): print(f"WARNING: unknown xRegistry field not rendered: {p}", file=sys.stderr)

@dataclass
class Ctx:
    data: Json
    warnings: WarningCollector = field(default_factory=WarningCollector)
    endpoints_by_group: dict[str, list[tuple[str, Json]]] = field(default_factory=dict)
    def __post_init__(self) -> None:
        for eid,e in (self.data.get("endpoints") or {}).items():
            for ref in nlist(e.get("messagegroups") or e.get("messagegroup")):
                self.endpoints_by_group.setdefault(ref_id(str(ref)), []).append((eid,e))

def main() -> None:
    p=argparse.ArgumentParser(description="Generate EVENTS.md from an xRegistry JSON manifest.")
    p.add_argument("manifest_file")
    p.add_argument("--title")
    p.add_argument("--description")
    p.add_argument("--output")
    a=p.parse_args()
    path=Path(a.manifest_file)
    data=json.loads(path.read_text(encoding="utf-8"))
    if (a.title or a.description) and not os.environ.get("PRINTDOC_SUPPRESS_COMPAT_NOTICE"):
        print("NOTICE: --title/--description are still supported; omit them to use xRegistry-derived defaults.", file=sys.stderr)
    doc,warnings=generate_documentation(data, a.title or default_title(data,path), a.description if a.description is not None else default_description(data))
    warnings.emit()
    if a.output:
        out=Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding="utf-8", newline="\n")
    else: print(doc, end="")

def default_title(data: Json, manifest_path: Path|None=None) -> str:
    if isinstance(data.get("name"),str) and data["name"].strip(): return data["name"].strip()+" Events"
    if manifest_path and manifest_path.parent.name=="xreg": return human(manifest_path.parent.parent.name)+" Bridge Events"
    return "Bridge Events"

def default_description(data: Json) -> str:
    d=data.get("description")
    if isinstance(d,str): return d.strip()
    doc=data.get("documentation")
    if isinstance(doc,str): return doc.strip()
    if isinstance(doc,dict):
        for k in ("description","url","uri"):
            if isinstance(doc.get(k),str): return doc[k].strip()
    return ""

def generate_documentation(data: Json, title: str|None=None, description: str|None=None) -> tuple[str, WarningCollector]:
    ctx=Ctx(data); warn_unknowns(data, ctx.warnings)
    b=io.StringIO(); w=b.write
    w(f"# {title or default_title(data)}\n\n")
    if description: w(description.strip()+"\n\n")
    w("## Table of Contents\n\n- [Registry](#registry)\n- [Endpoints](#endpoints)\n- [Messagegroups](#messagegroups)\n- [Schemagroups](#schemagroups)\n\n---\n\n")
    for section in (render_registry(data), render_endpoints(ctx), render_messagegroups(ctx), render_schemagroups(ctx)):
        for line in section: w(line+"\n")
    return b.getvalue().rstrip() + "\n", ctx.warnings

def render_registry(data: Json) -> list[str]:
    rows=[]
    for k,l in (("name","Name"),("version","Version"),("description","Description")):
        if data.get(k) is not None: rows.append((l, fmt(data[k])))
    if data.get("documentation"): rows.append(("Documentation", fmt_doc(data["documentation"])))
    rows += [("Endpoints", str(len(data.get("endpoints") or {}))),("Messagegroups", str(len(data.get("messagegroups") or {}))),("Schemagroups", str(len(data.get("schemagroups") or {})))]
    return ["## Registry", "", *table(["Field","Value"], rows), ""]

def render_endpoints(ctx: Ctx) -> list[str]:
    lines=["## Endpoints", ""]
    for eid,e in (ctx.data.get("endpoints") or {}).items():
        proto=str(e.get("protocol","unspecified"))
        rows=[("Usage", ", ".join(map(str,nlist(e.get("usage")))) or "-"),("Protocol", code(proto)),("Envelope",fmt(e.get("envelope"))),("Envelope options", cjson(e.get("envelopeoptions"))),("Messagegroups", ", ".join(group_link(r) for r in nlist(e.get("messagegroups") or e.get("messagegroup"))) or "-")]
        if e.get("description"): rows.insert(0,("Description",fmt(e.get("description"))))
        lines += [f"### Endpoint `{eid}`", "", *table(["Field","Value"], rows), "", *render_transport_options(proto,e,4)]
    if len(lines)==2: lines += ["No endpoints declared.", ""]
    return lines

def render_transport_options(proto: str, carrier: Json, level: int) -> list[str]:
    opts=carrier.get("protocoloptions") if isinstance(carrier.get("protocoloptions"),dict) else {}
    meta=carrier.get("protocolmetadata") if isinstance(carrier.get("protocolmetadata"),dict) else {}
    options=opts.get("options") if isinstance(opts.get("options"),dict) else {}; props=opts.get("properties") if isinstance(opts.get("properties"),dict) else {}
    up=proto.upper(); rows=[]
    if "KAFKA" in up: rows += [("Kafka topic", code(options.get("topic") or opts.get("topic"))),("Kafka key", code(options.get("key") or opts.get("key")))]
    if "MQTT" in up: rows += [("MQTT topic", code(opts.get("topic_name") or opts.get("topic") or props.get("topic"))),("QoS", fmt(opts.get("qos") or props.get("qos"))),("Retain", fmt(opts.get("retain") if "retain" in opts else props.get("retain"))),("Topic alias", fmt(opts.get("topic_alias") or opts.get("alias") or props.get("topic_alias"))),("Clean start", fmt(opts.get("clean_start") or opts.get("cleanstart") or props.get("clean_start")))]
    if "AMQP" in up: rows += [("AMQP address", code(opts.get("address") or opts.get("address_name") or options.get("address") or props.get("address"))),("Durable", fmt(opts.get("durable") or props.get("durable"))),("Application properties", cjson(opts.get("application_properties") or meta.get("application_properties")))]
    if opts.get("deployed") is not None: rows.append(("Deployed",fmt(opts.get("deployed"))))
    if opts.get("endpoints"): rows.append(("Broker endpoints",cjson(opts.get("endpoints"))))
    if carrier.get("deployed") is not None: rows.append(("Deployed",fmt(carrier.get("deployed"))))
    if carrier.get("endpoints"): rows.append(("Broker endpoints",cjson(carrier.get("endpoints"))))
    known={"options","properties","topic","topic_name","qos","retain","topic_alias","alias","clean_start","cleanstart","address","address_name","durable","application_properties","deployed","endpoints","key"}
    extra={k:v for k,v in opts.items() if k not in known}; extra.update({"metadata."+k:v for k,v in meta.items() if k!="application_properties"})
    if extra: rows.append(("Additional protocol metadata", cjson(extra)))
    rows=[r for r in rows if r[1] not in ("-","`-`","")]
    return ["#"*level+" Transport options", "", *table(["Option","Value"], rows), ""] if rows else []

def render_messagegroups(ctx: Ctx) -> list[str]:
    lines=["## Messagegroups", ""]
    for gid,g in (ctx.data.get("messagegroups") or {}).items():
        rows=[("Name",fmt(g.get("name"))),("Description",fmt(g.get("description"))),("Transport bindings", ", ".join(f"`{eid}` ({e.get('protocol','-')})" for eid,e in ctx.endpoints_by_group.get(gid,[])) or "-"),("Messages",str(len(g.get("messages") or {})))]
        lines += [f"### Messagegroup `{gid}`", f'<a id="messagegroup-{anchor(gid)}"></a>', "", *table(["Field","Value"], [r for r in rows if r[1]!="-"]), ""]
        for mid,m in (g.get("messages") or {}).items(): lines += render_message(ctx,gid,mid,m)
    if len(lines)==2: lines += ["No messagegroups declared.", ""]
    return lines

def render_message(ctx: Ctx, gid: str, mid: str, msg: Json) -> list[str]:
    resolved,chain=resolve_message_chain(msg, ctx.data.get("messagegroups") or {})
    lines=[f"#### Message `{mid}`", f'<a id="message-{anchor(mid)}"></a>', ""]
    if resolved.get("description"): lines += [cell(resolved.get("description")), ""]
    rows=[("Name",fmt(resolved.get("name"))),("Envelope",fmt(resolved.get("envelope"))),("Schema format",fmt(resolved.get("dataschemaformat"))),("Data schema",schema_link(resolved.get("dataschemauri")))]
    if chain: rows.append(("Base message chain", " → ".join(f"`{c}`" for c in chain)))
    proto=msg.get("protocol") or resolved.get("protocol")
    if proto: rows.append(("Transport override",code(proto)))
    rows.append(("Event role", reference_hint(msg,resolved)))
    lines += table(["Field","Value"], [r for r in rows if r[1]!="-"]) + [""]
    md=resolved.get("envelopemetadata") or {}
    if md:
        mrows=[]
        for n,v in md.items():
            d=v if isinstance(v,dict) else {"value":v}
            mrows.append((f"`{n}`", cell(d.get("description","")), code(d.get("type","string")), code(d.get("required",False)), code(d.get("value",""))))
        lines += ["##### CloudEvents metadata", "", *table(["Attribute","Description","Type","Required","Value/template"], mrows), ""]
    lines += render_bindings(ctx,gid,msg,resolved)
    if msg.get("protocoloptions") or msg.get("protocolmetadata"): lines += render_transport_options(str(proto or ""), msg, 5)
    return lines

def render_bindings(ctx: Ctx, gid: str, msg: Json, resolved: Json) -> list[str]:
    rows=[]; subj=((resolved.get("envelopemetadata") or {}).get("subject") or {})
    subject=subj.get("value") if isinstance(subj,dict) else None
    for eid,e in ctx.endpoints_by_group.get(gid,[]):
        proto=str(e.get("protocol","")); opts=e.get("protocoloptions") if isinstance(e.get("protocoloptions"),dict) else {}; options=opts.get("options") if isinstance(opts.get("options"),dict) else {}; bits=[]
        if "KAFKA" in proto.upper(): bits += ["topic "+code(options.get("topic") or opts.get("topic")), "key "+code(options.get("key") or opts.get("key") or subject)]
        if "MQTT" in proto.upper(): bits.append("topic "+code((msg.get("protocoloptions") or {}).get("topic_name") or (msg.get("protocoloptions") or {}).get("topic")))
        if "AMQP" in proto.upper(): bits.append("address "+code((msg.get("protocoloptions") or {}).get("address") or (msg.get("protocoloptions") or {}).get("address_name") or opts.get("address")))
        rows.append((f"`{eid}`", code(proto), "; ".join(bits) or "-"))
    return ["##### Bound transports", "", *table(["Endpoint","Protocol","Binding"], rows), ""] if rows else []

def render_schemagroups(ctx: Ctx) -> list[str]:
    lines=["## Schemagroups", ""]
    for gid,g in (ctx.data.get("schemagroups") or {}).items():
        lines += [f"### Schemagroup `{gid}`", f'<a id="schemagroup-{anchor(gid)}"></a>', ""]
        for sid,s in (g.get("schemas") or {}).items(): lines += render_schema_container(sid,s)
    if len(lines)==2: lines += ["No schemagroups declared.", ""]
    return lines

def render_schema_container(sid: str, c: Json) -> list[str]:
    lines=[f"#### Schema `{sid}`", f'<a id="schema-{anchor(sid)}"></a>', ""]
    rows=[("Name",fmt(c.get("name"))),("Format",fmt(c.get("format"))),("Default version",fmt(c.get("defaultversionid"))),("Description",fmt(c.get("description")))]
    lines += table(["Field","Value"], [r for r in rows if r[1]!="-"]) + [""]
    for vid,v in sorted((c.get("versions") or {}).items(), key=lambda kv: version_key(kv[0])):
        sch=v.get("schema"); lines += [f"##### Version `{vid}`", ""]
        if v.get("format"): lines += table(["Field","Value"], [("Format",fmt(v.get("format")))]) + [""]
        if isinstance(sch,dict): lines += render_avro(sch) if is_avro(sch,v.get("format") or c.get("format")) else render_jstruct(sch)
        else: lines += ["Schema payload is not an object.", ""]
    return lines

def render_jstruct(schema: Json) -> list[str]:
    root=resolve_root(schema); lines=["###### JsonStructure", ""]
    rows=[("$id",code(schema.get("$id") or root.get("$id"))),("$schema",code(schema.get("$schema"))),("$root",code(schema.get("$root"))),("Type",code(type_label(root))),("Additional properties",code(root.get("additionalProperties") if "additionalProperties" in root else schema.get("additionalProperties")))]
    lines += table(["Field","Value"], [r for r in rows if r[1]!="`-`"])+[""]
    seen=set(); q=[(str(root.get("name") or schema.get("name") or "Root"), root)]
    while q:
        name,node=q.pop(0)
        if id(node) in seen: continue
        seen.add(id(node)); lines += render_node(name,node,schema,q)
    return lines

def render_node(name: str, node: Json, doc: Json, q: list[tuple[str,Json]]) -> list[str]:
    lines=[f"###### {type_label(node).title()} `{name}`", f'<a id="schema-node-{anchor(name)}"></a>', ""]
    if node.get("description"): lines += [cell(node.get("description")), ""]
    meta=[]
    if node.get("$id"): meta.append(("$id",code(node.get("$id"))))
    if "additionalProperties" in node: meta.append(("Additional properties",code(node.get("additionalProperties"))))
    if meta: lines += table(["Field","Value"], meta)+[""]
    if is_obj(node):
        req=set(node.get("required") or []); rows=[]
        for fn,fs in (node.get("properties") or {}).items():
            fs=fs if isinstance(fs,dict) else {"type":fs}
            rows.append((f"`{fn}`", type_str(fs,doc,q,f"{name}.{fn}"), code(fn in req), cell(fs.get("description","")), ext_str(fs), val_str(fs), def_str(fs)))
        if rows: lines += table(["Field","Type","Required","Description","Extensions","Validation","Default/const"], rows)+[""]
    elif is_enum(node): lines += render_enum(node)
    else:
        rows=[]
        if "items" in node: rows.append(("Items", type_str(node["items"],doc,q,name+".items")))
        if "choices" in node:
            ch=node["choices"].items() if isinstance(node["choices"],dict) else enumerate(nlist(node["choices"]))
            for cn,cs in ch: rows.append((f"Choice `{cn}`", type_str(cs,doc,q,f"{name}.{cn}")))
        if rows: lines += table(["Part","Type"], rows)+[""]
    return lines

def render_enum(node: Json) -> list[str]:
    vals=node.get("enum") or node.get("symbols") or []; desc=node.get("descriptions") if isinstance(node.get("descriptions"),dict) else {}; alt=node.get("altenums") if isinstance(node.get("altenums"),dict) else {}; ords=node.get("ordinals") if isinstance(node.get("ordinals"),dict) else {}
    return [*table(["Value","Description","Ordinal","Alternative enum labels"], [(code(v), cell(desc.get(v,"")), fmt(ords.get(v)), cjson(alt.get(v)) if v in alt else "-") for v in vals]), ""] if vals else []

def render_avro(schema: Json) -> list[str]:
    lines=["###### Avro", "", *table(["Field","Value"], [("Name",fmt(schema.get("name"))),("Namespace",fmt(schema.get("namespace"))),("Type",code(schema.get("type"))),("Doc",cell(schema.get("doc","")))]), ""]
    if schema.get("type")=="record" and isinstance(schema.get("fields"),list):
        lines += table(["Field","Type","Description","Default"], [(f"`{f.get('name')}`", avro_type(f.get("type")), cell(f.get("doc","")), code(f.get("default") if "default" in f else "")) for f in schema["fields"]])+[""]
    elif schema.get("type")=="enum": lines += render_enum(schema)
    else: lines += ["```json", json.dumps(schema,indent=2,ensure_ascii=False), "```", ""]
    return lines

def resolve_message_chain(msg: Json, groups: Json) -> tuple[Json,list[str]]:
    merged=dict(msg); chain=[]
    ref=msg.get("basemessageurl")
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

def resolve_root(schema: Json) -> Json:
    r=schema.get("$root")
    target=ptr(schema,r) if isinstance(r,str) else None
    return target if isinstance(target,dict) else schema

def ptr(doc: Json, pointer: str|None) -> Any:
    if not pointer or not pointer.startswith("#/"): return None
    node: Any=doc
    for raw in pointer[2:].split('/'):
        if not isinstance(node,dict): return None
        node=node.get(raw.replace("~1","/").replace("~0","~"))
    return node

def type_str(s: Any, doc: Json, q: list[tuple[str,Json]], fb: str) -> str:
    if isinstance(s,str): return code(s)
    if isinstance(s,list): return " | ".join(type_str(x,doc,q,fb) for x in s)
    if not isinstance(s,dict): return code(s)
    if isinstance(s.get("$ref"),str):
        t=ptr(doc,s["$ref"]); name=str((t or {}).get("name") or s["$ref"].split('/')[-1]) if isinstance(t,dict) else s["$ref"]
        if isinstance(t,dict): q.append((name,t))
        return f"[`{cell(name)}`](#schema-node-{anchor(name)})"
    if is_obj(s):
        name=str(s.get("name") or fb); q.append((name,s)); return f"[object `{cell(name)}`](#schema-node-{anchor(name)})"
    if s.get("type")=="array": return "array of "+type_str(s.get("items",{}),doc,q,fb+".items")
    if is_enum(s): return "enum "+code(s.get("enum") or s.get("symbols"))
    return code(type_label(s))

def is_avro(s: Json, fmt: Any=None) -> bool: return (isinstance(fmt,str) and "avro" in fmt.lower()) or (s.get("type")=="record" and "fields" in s)
def is_obj(s: Json) -> bool: return s.get("type")=="object" or (isinstance(s.get("type"),list) and "object" in s.get("type")) or "properties" in s
def is_enum(s: Json) -> bool: return s.get("type")=="enum" or "enum" in s or (s.get("type")=="enum" and "symbols" in s)
def type_label(s: Json) -> str:
    if "choices" in s: return "choice"
    t=s.get("type")
    if isinstance(t,list): return "union"
    if isinstance(t,str): return t
    if "enum" in s or "symbols" in s: return "enum"
    if "properties" in s: return "object"
    return "schema"

def ext_str(s: Json) -> str:
    parts=[]
    if s.get("unit") or s.get("symbol"): parts.append(("unit="+code(s.get("unit","")) if not s.get("symbol") else "unit="+code(s.get("unit",""))+" symbol="+code(s.get("symbol"))))
    for k in ("altnames","altenums","alternates","descriptions","values"):
        if k in s: parts.append(f"{k}={cjson(s[k])}")
    return "<br>".join(parts) or "-"
def val_str(s: Json) -> str: return "<br>".join(f"{k}={code(s[k])}" for k in sorted(VALIDATION_KEYS) if k in s) or "-"
def def_str(s: Json) -> str: return "<br>".join(f"{k}={code(s[k])}" for k in ("const","default") if k in s) or "-"
def reference_hint(msg: Json, resolved: Json) -> str:
    opts=msg.get("protocoloptions") if isinstance(msg.get("protocoloptions"),dict) else {}
    if opts.get("retain") is True: return "Reference data (retained transport message)"
    text=(str(resolved.get("name",""))+" "+str(resolved.get("description",""))).lower()
    return "Reference/status data" if any(w in text for w in ("station","configuration","catalog","region","metadata","status")) else "Telemetry/event data"
def schema_link(ref: Any) -> str:
    if not isinstance(ref,str) or not ref: return "-"
    sid=ref.split('/')[-1]
    return f"[`{cell(ref)}`](#schema-{anchor(sid)})" if "/schemas/" in ref else code(ref)
def group_link(ref: Any) -> str:
    gid=ref_id(str(ref)); return f"[`{cell(gid)}`](#messagegroup-{anchor(gid)})"
def ref_id(ref: str) -> str: return ref.rstrip('/').split('/')[-1] if '/' in ref else ref

def warn_unknowns(data: Json, w: WarningCollector) -> None:
    warn_keys(data,KNOWN_TOP_KEYS,"registry",w)
    for eid,e in (data.get("endpoints") or {}).items():
        if isinstance(e,dict): warn_keys(e,KNOWN_ENDPOINT_KEYS,f"endpoints.{eid}",w)
    for gid,g in (data.get("messagegroups") or {}).items():
        if not isinstance(g,dict): continue
        warn_keys(g,KNOWN_MESSAGEGROUP_KEYS,f"messagegroups.{gid}",w)
        for mid,m in (g.get("messages") or {}).items():
            if isinstance(m,dict): warn_keys(m,KNOWN_MESSAGE_KEYS,f"messagegroups.{gid}.messages.{mid}",w)
    for gid,g in (data.get("schemagroups") or {}).items():
        for sid,c in ((g or {}).get("schemas") or {}).items():
            if isinstance(c,dict):
                warn_keys(c,KNOWN_SCHEMA_CONTAINER_KEYS,f"schemagroups.{gid}.schemas.{sid}",w)
                for vid,v in (c.get("versions") or {}).items():
                    if isinstance(v,dict):
                        warn_keys(v,KNOWN_SCHEMA_VERSION_KEYS,f"schemagroups.{gid}.schemas.{sid}.versions.{vid}",w)
                        if isinstance(v.get("schema"),dict): warn_schema(v["schema"],f"schemagroups.{gid}.schemas.{sid}.versions.{vid}.schema",w)
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

def table(headers: list[str], rows: list[tuple[Any,...]]) -> list[str]:
    if not rows: return []
    return ["| "+" | ".join(headers)+" |", "| "+" | ".join("---" for _ in headers)+" |"] + ["| "+" | ".join(cell(c) for c in r)+" |" for r in rows]
def cell(v: Any) -> str: return "-" if v is None else str(v).replace('|','\\|').replace('\r',' ').replace('\n',' ')
def fmt(v: Any) -> str: return "-" if v is None or v=="" else (cjson(v) if isinstance(v,(dict,list)) else cell(v))
def code(v: Any) -> str: return "`-`" if v is None or v=="" else "`"+cell(v)+"`"
def cjson(v: Any) -> str: return "-" if v is None or v=="" else "`"+cell(json.dumps(v,ensure_ascii=False,sort_keys=True))+"`"
def fmt_doc(v: Any) -> str:
    if isinstance(v,str): return f"<{cell(v)}>" if v.startswith(("http://","https://")) else cell(v)
    if isinstance(v,list): return ", ".join(fmt_doc(x) for x in v)
    if isinstance(v,dict): return "<br>".join(f"{cell(k)}: {fmt(val)}" for k,val in v.items())
    return fmt(v)
def avro_type(v: Any) -> str:
    if isinstance(v,str): return code(v)
    if isinstance(v,list): return " | ".join(avro_type(x) for x in v)
    if isinstance(v,dict):
        if v.get("type")=="array": return "array of "+avro_type(v.get("items"))
        if v.get("type") in ("record","enum"): return f"{v.get('type')} `{cell(v.get('name','anonymous'))}`"
        return code(v.get("type") or v)
    return code(v)
def nlist(v: Any) -> list[Any]: return [] if v is None else (v if isinstance(v,list) else [v])
def version_key(v: str) -> tuple[int,str]: return (0,f"{int(v):010d}") if str(v).isdigit() else (1,str(v))
def human(s: str) -> str: return " ".join(p.capitalize() for p in re.split(r"[-_\s]+",s) if p)
def anchor(s: str) -> str: return re.sub(r"[\s-]+","-",re.sub(r"[^a-z0-9\s-]","",s.lower())).strip('-')

def process_message(msg: Json, schemagroups: Json, messagegroups: Json|None=None) -> list[str]: return render_message(Ctx({"messagegroups":messagegroups or {},"schemagroups":schemagroups}),"default",str(msg.get("name","message")),msg)
def resolve_schema(uri: str|None, schemagroups: Json) -> Json|None:
    if not uri or not uri.startswith("#/"): return None
    node: Any={"schemagroups":schemagroups}
    for p in uri[2:].split('/'):
        node=node.get(p) if isinstance(node,dict) else None
    if not isinstance(node,dict): return None
    versions=node.get("versions") or {}
    return versions[sorted(versions.keys(),key=version_key)[-1]].get("schema") if versions else node.get("schema")
def print_schema(schema: Json) -> list[str]: return render_avro(schema) if is_avro(schema) else render_jstruct(schema)
def generate_anchor(name: str) -> str: return anchor(name)

if __name__ == "__main__": main()
