import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import printdoc


def manifest():
    schema = {
        "$schema": "https://json-structure.org/meta/extended/v0/#",
        "$id": "https://example.test/schema/Created",
        "name": "Created",
        "type": "object",
        "additionalProperties": False,
        "required": ["id", "state"],
        "properties": {
            "id": {"type": "string", "description": "Identifier", "altnames": ["upstream_id"], "pattern": "^[A-Z]+$", "minLength": 1},
            "level": {"type": ["null", "double"], "description": "Level", "unit": "metre", "symbol": "m", "minimum": 0, "maximum": 10, "default": None},
            "state": {"type": "string", "description": "State", "enum": ["ok", "bad"], "descriptions": {"ok": "OK"}, "altenums": {"ok": ["0"]}},
            "nested": {"type": "object", "name": "Nested", "description": "Nested record", "properties": {"value": {"type": "integer", "const": 1}}},
        },
    }
    base_msg = {
        "name": "Created",
        "description": "A telemetry message.",
        "envelope": "CloudEvents/1.0",
        "envelopemetadata": {
            "type": {"value": "example.Created", "type": "string", "required": True},
            "source": {"value": "https://example.test", "type": "uri"},
            "subject": {"value": "{id}", "type": "uritemplate"},
            "partitionkey": {"value": "{id}", "type": "uritemplate"},
        },
        "dataschemaformat": "JsonStructure/draft-02",
        "dataschemauri": "#/schemagroups/example.jstruct/schemas/example.Created",
    }
    return {
        "name": "Synthetic Registry",
        "version": "1.0.0",
        "description": "Registry description.",
        "documentation": {"url": "https://example.test/docs"},
        "endpoints": {
            "example.Kafka": {"usage": ["producer"], "protocol": "KAFKA", "envelope": "CloudEvents/1.0", "envelopeoptions": {"mode": "structured"}, "protocoloptions": {"options": {"topic": "example", "key": "{id}"}}, "messagegroups": ["#/messagegroups/example"]},
            "example.Mqtt": {"usage": ["producer"], "protocol": "MQTT/5.0", "protocoloptions": {"endpoints": [{"uri": "mqtt://localhost:1883"}]}, "messagegroups": ["#/messagegroups/example.mqtt"]},
            "example.Amqp": {"usage": ["producer"], "protocol": "AMQP/1.0", "protocoloptions": {"address": "events/{id}", "durable": True, "application_properties": {"ce_type": "example.Created"}}, "messagegroups": ["#/messagegroups/example.amqp"]},
        },
        "messagegroups": {
            "example": {"description": "Base messages.", "messages": {"example.Created": base_msg}},
            "example.mqtt": {"description": "MQTT bindings.", "messages": {"example.mqtt.Created": {"name": "Created", "basemessageurl": "/messagegroups/example/messages/example.Created", "protocol": "MQTT/5.0", "protocoloptions": {"topic_name": "factory/{id}/created", "qos": 1, "retain": True}}}},
            "example.amqp": {"messages": {"example.amqp.Created": {"name": "Created", "basemessageurl": "/messagegroups/example/messages/example.Created", "protocol": "AMQP/1.0", "protocoloptions": {"address": "events/{id}", "durable": False}}}},
        },
        "schemagroups": {"example.jstruct": {"schemas": {"example.Created": {"name": "Created", "format": "JsonStructure/draft-02", "defaultversionid": "1", "versions": {"1": {"format": "JsonStructure/draft-02", "schema": schema}}}}}},
    }

class PrintDocTests(unittest.TestCase):
    def test_renders_full_surface(self):
        md, warnings = printdoc.generate_documentation(manifest())
        self.assertEqual([], sorted(warnings.paths))
        for text in ["## Registry", "### Endpoint `example.Kafka`", "Kafka key", "MQTT topic", "AMQP address", "#### Message `example.mqtt.Created`", "Base message chain", "`partitionkey`", "Reference data (retained transport message)", "#### Schema `example.Created`", "$id", "altnames=", "unit=`metre` symbol=`m`", "pattern=`^[A-Z]+$`", "minimum=`0`", "const=`1`", "Additional properties"]:
            self.assertIn(text, md)
    def test_unknown_fields_are_warned(self):
        m=manifest(); m["mystery"]=True
        _, warnings = printdoc.generate_documentation(m)
        self.assertIn("registry.mystery", warnings.paths)
    def test_cli_writes_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as td:
            p=pathlib.Path(td); mf=p/"sample.xreg.json"; out=p/"EVENTS.md"
            mf.write_text(json.dumps(manifest()), encoding="utf-8")
            old=sys.argv
            try:
                sys.argv=["printdoc.py", str(mf), "--output", str(out)]
                printdoc.main()
            finally:
                sys.argv=old
            self.assertIn("# Synthetic Registry Events", out.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
