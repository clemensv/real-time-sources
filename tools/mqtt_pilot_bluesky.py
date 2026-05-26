"""One-shot script: extend bluesky.xreg.json for the MQTT firehose pilot.

Adds:
  - top-level required fields `collection` and `lang` to every JsonStructure
    schema (and matching Avro field) under BlueskyFirehose.jstruct/.avro;
  - a `BlueskyFirehose.Mqtt` endpoint (MQTT/5.0, binary CE);
  - a `BlueskyFirehose.mqtt` messagegroup with one message per record kind
    whose `topic_name` bakes the kebab `{event}` tail as a literal and
    declares `qos=0` / `retain=false`.

Idempotent — safe to re-run.
"""

from __future__ import annotations

import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XREG = ROOT / "bluesky" / "xreg" / "bluesky.xreg.json"

# (CE type, schema id stem, kebab event tail used in topic + did/lang/collection)
EVENTS = [
    ("Bluesky.Feed.Post",      "Bluesky.Feed.Post",      "post"),
    ("Bluesky.Feed.Like",      "Bluesky.Feed.Like",      "like"),
    ("Bluesky.Feed.Repost",    "Bluesky.Feed.Repost",    "repost"),
    ("Bluesky.Graph.Follow",   "Bluesky.Graph.Follow",   "follow"),
    ("Bluesky.Graph.Block",    "Bluesky.Graph.Block",    "block"),
    ("Bluesky.Actor.Profile",  "Bluesky.Actor.Profile",  "profile"),
]

COLLECTION_DESC = (
    "AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). "
    "Populated by the bridge from the upstream firehose commit and used "
    "as the second MQTT topic segment so subscribers can wildcard on a "
    "record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). "
    "Lowercase; never empty."
)
LANG_DESC = (
    "Primary BCP-47 language tag for the record. For posts this is the "
    "first entry of `record.langs[]`; for records without a language "
    "field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). "
    "Always lowercase, so subscribers can wildcard on `…/ja/+/+`."
)


def main() -> int:
    data = json.loads(XREG.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)

    # ---- 1. Schemas: add collection + lang ---------------------------------
    sg = data["schemagroups"]["BlueskyFirehose.jstruct"]["schemas"]
    for ce_type, schema_id, _ in EVENTS:
        if schema_id not in sg:
            print(f"WARN: jstruct schema {schema_id} missing")
            continue
        schema = sg[schema_id]["versions"]["1"]["schema"]
        # navigate to the inner object definition
        defs = schema.get("definitions", {})
        # Walk to find the inner object (Bluesky/Feed/Post etc.)
        node = defs
        for part in ce_type.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                node = None
                break
        if not isinstance(node, dict) or node.get("type") != "object":
            print(f"WARN: cannot locate object for {ce_type}")
            continue
        props = node.setdefault("properties", OrderedDict())
        if "collection" not in props:
            props["collection"] = OrderedDict([
                ("type", "string"),
                ("description", COLLECTION_DESC),
            ])
        if "lang" not in props:
            props["lang"] = OrderedDict([
                ("type", "string"),
                ("description", LANG_DESC),
            ])
        req = node.setdefault("required", [])
        for f in ("collection", "lang"):
            if f not in req:
                req.append(f)

    # Avro mirror -----------------------------------------------------------
    avro_grp = data["schemagroups"].get("BlueskyFirehose.avro", {}).get("schemas", {})
    for ce_type, schema_id, _ in EVENTS:
        if schema_id not in avro_grp:
            continue
        schema = avro_grp[schema_id]["versions"]["1"]["schema"]
        fields = schema.get("fields", [])
        names = {f.get("name") for f in fields}
        if "collection" not in names:
            fields.append(OrderedDict([
                ("name", "collection"),
                ("type", "string"),
                ("doc", COLLECTION_DESC),
            ]))
        if "lang" not in names:
            fields.append(OrderedDict([
                ("name", "lang"),
                ("type", "string"),
                ("doc", LANG_DESC),
                ("default", "und"),
            ]))

    # ---- 2. Endpoint -------------------------------------------------------
    endpoints = data["endpoints"]
    endpoints["BlueskyFirehose.Mqtt"] = OrderedDict([
        ("usage", ["producer"]),
        ("protocol", "MQTT/5.0"),
        ("envelope", "CloudEvents/1.0"),
        ("envelopeoptions", OrderedDict([("mode", "binary")])),
        ("protocoloptions", OrderedDict([
            ("deployed", False),
            ("endpoints", [OrderedDict([("uri", "mqtt://localhost:1883")])]),
        ])),
        ("messagegroups", ["#/messagegroups/BlueskyFirehose.mqtt"]),
    ])

    # ---- 3. MQTT messagegroup ---------------------------------------------
    mqtt_msgs = OrderedDict()
    for ce_type, _, event in EVENTS:
        msg_id = f"{ce_type}.mqtt"
        topic = f"social/intl/bluesky/bluesky/{{collection}}/{{lang}}/{{did}}/{event}"
        mqtt_msgs[msg_id] = OrderedDict([
            ("messageid", msg_id),
            ("name", ce_type.split(".")[-1]),
            ("basemessageuri", f"/messagegroups/BlueskyFirehose/messages/{ce_type}"),
            ("protocol", "MQTT/5.0"),
            ("protocoloptions", OrderedDict([
                ("topic_name", topic),
                ("qos", 0),
                ("retain", False),
            ])),
        ])
    data["messagegroups"]["BlueskyFirehose.mqtt"] = OrderedDict([
        ("messagegroupid", "BlueskyFirehose.mqtt"),
        ("description",
         "MQTT/5.0 non-retained firehose variants of the Bluesky CloudEvents. "
         "Each record family gets a dedicated topic with the kebab record name "
         "baked as the trailing segment so subscribers can wildcard per family. "
         "QoS 0, retain=false — there is no LKV slot for a firehose."),
        ("messages", mqtt_msgs),
    ])

    XREG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print(f"Updated {XREG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
