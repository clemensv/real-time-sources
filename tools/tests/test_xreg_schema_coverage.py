import copy
import json
import pathlib
import sys
import unittest

import avro.schema
import avro.io
from avro.compatibility import ReaderWriterCompatibilityChecker, SchemaCompatibilityType

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import xreg_schema_coverage as coverage


def manifest():
    return {
        "messagegroups": {
            "example": {"messages": {"example.Observation": {
                "envelope": "CloudEvents/1.0",
                "envelopemetadata": {
                    "type": {"value": "example.Observation"},
                    "subject": {"type": "uritemplate", "value": "{id}"},
                    "source": {"type": "uritemplate", "value": "{feedurl}"},
                },
                "dataschemaformat": "JsonStructure/draft-02",
                "dataschemauri": "#/schemagroups/example.jstruct/schemas/example.Observation",
            }}},
            "example.mqtt": {"messages": {"example.mqtt.Observation": {
                "basemessageuri": "/messagegroups/example/messages/example.Observation",
                "protocol": "MQTT/5.0",
                "protocoloptions": {"topic_name": "example/{id}", "retain": True, "qos": 1},
            }}},
        },
        "endpoints": {"example.Mqtt": {
            "protocol": "MQTT/5.0",
            "messagegroups": ["#/messagegroups/example.mqtt"],
        }},
        "schemagroups": {"example.jstruct": {"schemas": {"example.Observation": {
            "format": "JsonStructure/draft-02",
            "defaultversionid": "1",
            "versions": {"1": {
                "format": "JsonStructure/draft-02",
                "schema": {
                    "$id": "https://example.test/Observation", "name": "Observation",
                    "type": "object", "required": ["id", "timestamp"],
                    "properties": {
                        "id": {"type": "string", "description": "Stable identifier."},
                        "timestamp": {"type": "datetime", "description": "Observation time with offset."},
                        "value": {"type": ["double", "null"], "description": "Measured level.", "unit": "m"},
                    },
                },
            }},
        }}}},
    }


class CoverageTests(unittest.TestCase):
    def test_completion_preserves_transport_and_json_schema(self):
        source = manifest()
        result = coverage.complete(source)
        self.assertEqual(source, manifest())
        self.assertEqual(source["schemagroups"]["example.jstruct"], result["schemagroups"]["example.jstruct"])
        self.assertEqual([], coverage.audit(result))
        for suffix, content_type in ((".avro", coverage.JSON_TYPE), (".avro.binary", coverage.AVRO_TYPE)):
            ref = "#/messagegroups/example.mqtt" + suffix
            self.assertIn(ref, result["endpoints"]["example.Mqtt"]["messagegroups"])
            message = result["messagegroups"]["example.mqtt" + suffix]["messages"]["example.mqtt.Observation"]
            effective = coverage.materialize(result, message)
            self.assertEqual(source["messagegroups"]["example.mqtt"]["messages"]["example.mqtt.Observation"]["protocoloptions"], effective["protocoloptions"])
            self.assertEqual(content_type, effective["envelopemetadata"]["datacontenttype"]["value"])
            self.assertEqual("{id}", effective["envelopemetadata"]["subject"]["value"])
        self.assertNotIn("#/messagegroups/example.avro", result["endpoints"]["example.Mqtt"]["messagegroups"])
        self.assertEqual(result, coverage.complete(result))

    def test_validator_detects_missing_variant_schema_and_routing(self):
        good = coverage.complete(manifest())
        mutations = [
            lambda doc: doc["endpoints"]["example.Mqtt"]["messagegroups"].pop(),
            lambda doc: doc["messagegroups"]["example.avro"]["messages"].clear(),
            lambda doc: doc["schemagroups"]["example.avro"]["schemas"].clear(),
            lambda doc: doc["schemagroups"]["example.avro"]["schemas"]["example.Observation"]["versions"]["1"]["schema"]["fields"].pop(),
            lambda doc: doc["messagegroups"]["example.mqtt.avro"]["messages"]["example.mqtt.Observation"].update(protocoloptions={"retain": False}),
            lambda doc: doc["endpoints"]["example.Mqtt"].update(messagegroups=[]),
            lambda doc: doc["endpoints"]["example.Mqtt"]["messagegroups"].pop(0),
            lambda doc: doc["messagegroups"]["example.mqtt.avro"]["messages"]["example.mqtt.Observation"].update(protocol="AMQP/1.0"),
            lambda doc: doc["messagegroups"]["example.mqtt.avro"]["messages"]["example.mqtt.Observation"].update(envelope="Example/1.0"),
            lambda doc: doc["messagegroups"]["example.mqtt.avro"]["messages"]["example.mqtt.Observation"].pop("basemessage"),
            lambda doc: doc["messagegroups"].pop("example.mqtt"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                document = copy.deepcopy(good)
                mutate(document)
                self.assertTrue(coverage.audit(document))

    def test_validator_rejects_crosswired_schema_relationships(self):
        source = manifest()
        second = copy.deepcopy(source["messagegroups"]["example"]["messages"]["example.Observation"])
        second["dataschemauri"] = "#/schemagroups/example.jstruct/schemas/example.Other"
        source["messagegroups"]["example"]["messages"]["example.Other"] = second
        resource = copy.deepcopy(source["schemagroups"]["example.jstruct"]["schemas"]["example.Observation"])
        resource["versions"]["1"]["schema"]["properties"]["other"] = {"type": "boolean"}
        source["schemagroups"]["example.jstruct"]["schemas"]["example.Other"] = resource
        good = coverage.complete(source)
        self.assertEqual([], coverage.audit(good))
        for suffix in (".avro", ".avro.binary"):
            good["messagegroups"]["example" + suffix]["messages"]["example.Other"]["dataschemauri"] = "#/schemagroups/example.avro/schemas/example.Observation"
        self.assertTrue(coverage.audit(good))

    def test_default_only_repairs_are_versioned_and_invalid_defaults_fail_audit(self):
        source = manifest()
        source["schemagroups"]["example.jstruct"]["schemas"]["example.Observation"]["versions"]["1"]["schema"]["properties"]["cancelled"] = {
            "type": "boolean", "default": False,
        }
        good = coverage.complete(source)
        resource = good["schemagroups"]["example.avro"]["schemas"]["example.Observation"]
        cancelled = next(field for field in resource["versions"]["1"]["schema"]["fields"] if field["name"] == "cancelled")
        self.assertEqual(False, cancelled.pop("default"))
        repaired = coverage.complete(good)
        repaired_resource = repaired["schemagroups"]["example.avro"]["schemas"]["example.Observation"]
        self.assertEqual("2", repaired_resource["defaultversionid"])
        self.assertNotIn("default", next(field for field in repaired_resource["versions"]["1"]["schema"]["fields"] if field["name"] == "cancelled"))
        self.assertEqual([], coverage.audit(repaired))
        repaired_resource["versions"]["2"]["schema"]["fields"][-2]["default"] = 123
        self.assertTrue(any("default" in error for error in coverage.audit(repaired)))

    def test_inheritance_cycles_and_dangling_references_fail(self):
        doc = manifest()
        with self.assertRaises(KeyError):
            coverage.materialize(doc, {"basemessage": "/messagegroups/missing/messages/missing"})
        msg = doc["messagegroups"]["example"]["messages"]["example.Observation"]
        msg["basemessage"] = "/messagegroups/example/messages/example.Observation"
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            coverage.materialize(doc, msg)

    def test_schema_shape_repairs_are_versioned_and_keep_wide_integers(self):
        doc = manifest()
        doc["schemagroups"]["example.jstruct"]["schemas"]["example.Observation"]["versions"]["1"]["schema"]["properties"]["seq"] = {"type": "integer"}
        old = {"type": "record", "name": "Old", "fields": [
            {"name": "id", "type": "string"},
            {"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-micros"}},
            {"name": "seq", "type": ["null", "long"], "default": None},
        ]}
        doc["schemagroups"]["example.avro"] = {"schemas": {"example.Observation": {
            "format": coverage.AVRO_FORMAT, "defaultversionid": "1",
            "versions": {"1": {"format": coverage.AVRO_FORMAT, "schema": copy.deepcopy(old)}},
        }}}
        result = coverage.complete(doc)
        resource = result["schemagroups"]["example.avro"]["schemas"]["example.Observation"]
        self.assertEqual("2", resource["defaultversionid"])
        self.assertEqual(old, resource["versions"]["1"]["schema"])
        fields = {field["name"]: field for field in resource["versions"]["2"]["schema"]["fields"]}
        self.assertEqual(["null", "long"], fields["seq"]["type"])
        self.assertEqual("timestamp-micros", fields["timestamp"]["type"]["logicalType"])
        self.assertIn("value", fields)
        self.assertEqual(result, coverage.complete(result))

    def test_invalid_string_timestamp_annotation_is_removed_not_retyped(self):
        old = {"type": "record", "name": "Observation", "fields": [
            {"name": "time", "type": {"type": "string", "logicalType": "timestamp-millis"}},
        ]}
        coverage._repair_string_timestamps(old)
        self.assertEqual({"type": "string"}, old["fields"][0]["type"])
        data = {"type": "record", "name": "Metadata", "fields": [{
            "name": "metadata", "type": {"type": "map", "values": "string"},
            "default": {"type": "string", "logicalType": "timestamp-millis"},
        }]}
        before = copy.deepcopy(data)
        coverage._repair_string_timestamps(data)
        self.assertEqual(before, data)

    def test_preserving_named_type_identities_keeps_reader_writer_compatibility(self):
        old = {"type": "record", "name": "old.Observation", "fields": [
            {"name": "quality", "type": {"type": "enum", "name": "old.QualityLevel", "symbols": ["OK", "BAD"]}},
            {"name": "other", "type": "old.QualityLevel"},
        ]}
        new = {"type": "record", "name": "new.Observation", "fields": [
            {"name": "quality", "type": {"type": "enum", "name": "new.quality", "symbols": ["OK", "BAD"]}},
            {"name": "other", "type": "new.quality"},
        ]}
        writer = avro.schema.parse(json.dumps(old))
        projected = coverage._preserve_encodings(new, writer)
        reader = avro.schema.parse(json.dumps(projected))
        result = ReaderWriterCompatibilityChecker().get_compatibility(reader, writer)
        self.assertEqual(SchemaCompatibilityType.compatible, result.compatibility)

    def test_existing_documented_enum_symbol_mappings_are_preserved(self):
        writer = avro.schema.parse(json.dumps({
            "type": "enum", "name": "example.State", "symbols": ["normal", "out_dated"],
            "doc": "The symbol out_dated represents the JSON value out-dated.",
        }))
        projected = coverage.StandardAvro({"type": "string", "enum": ["normal", "out-dated"]}, "example.State").convert()
        reader = coverage._preserve_encodings(projected, writer)
        self.assertEqual("example.State", avro.schema.parse(json.dumps(reader)).fullname)
        self.assertEqual(writer.symbols, reader["symbols"])

    def test_native_logical_type_survives_matching_primitive_projection(self):
        source = manifest()
        source["schemagroups"]["example.jstruct"]["schemas"]["example.Observation"]["versions"]["1"]["schema"]["properties"]["timestamp"]["type"] = "int64"
        previous = {"type": "record", "name": "example.Observation", "fields": [
            {"name": "id", "type": "string"},
            {"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}},
        ]}
        source["schemagroups"]["example.avro"] = {"schemas": {"example.Observation": {
            "format": coverage.AVRO_FORMAT, "defaultversionid": "1",
            "versions": {"1": {"format": coverage.AVRO_FORMAT, "schema": previous}},
        }}}
        completed = coverage.complete(source)
        schema = coverage.versioned_schema(completed["schemagroups"]["example.avro"]["schemas"]["example.Observation"])["schema"]
        self.assertEqual(previous["fields"][1]["type"], schema["fields"][1]["type"])
        self.assertEqual([], coverage.audit(completed))
        self.assertEqual(completed, coverage.complete(completed))
        schema["fields"][1]["type"] = "long"
        self.assertTrue(any("loses native timestamp-millis" in error for error in coverage.audit(completed)))


class StandardAvroTests(unittest.TestCase):
    def test_nullable_enums_enforce_symbols_with_independent_avro_validation(self):
        schema = {"type": "object", "properties": {"country": {"type": ["string", "null"], "enum": ["DNK", "GRL", "FRO"]}}}
        result = avro.schema.parse(json.dumps(coverage.StandardAvro(schema, "example.Observation").convert()))
        for value in (None, "DNK", "GRL", "FRO"):
            self.assertTrue(avro.io.validate(result, {"country": value}))
        self.assertFalse(avro.io.validate(result, {"country": "USA"}))

    def test_repeated_invalid_symbol_enum_references_remain_parseable(self):
        schema = {"type": "object", "properties": {
            "first": {"type": {"$ref": "#/definitions/State"}},
            "second": {"type": {"$ref": "#/definitions/State"}},
        }, "definitions": {"State": {"type": "string", "enum": ["Very High", "Low"]}}}
        result = avro.schema.parse(json.dumps(coverage.StandardAvro(schema, "example.Observation").convert()))
        self.assertTrue(avro.io.validate(result, {"first": "Very High", "second": "Low"}))

    def test_nonnull_defaults_are_first_in_unions(self):
        schema = {"type": "object", "properties": {"cancelled": {"type": "boolean", "default": False}}}
        result = coverage.StandardAvro(schema, "example.Observation").convert()
        self.assertEqual(["boolean", "null"], result["fields"][0]["type"])
        self.assertEqual([], coverage._default_errors(avro.schema.parse(json.dumps(result)), "example"))

    def test_nested_refs_aliases_enums_and_nulls_parse_independently(self):
        schema = {
            "name": "Observation", "$root": "#/definitions/example/Observation",
            "definitions": {"example": {
                "Observation": {"type": "object", "required": ["samples"], "properties": {
                    "samples": {"type": {"$ref": "#/definitions/example/Samples"}},
                    "state": {"type": ["null", {"$ref": "#/definitions/example/State"}]},
                    "count": {"type": "integer"},
                }},
                "Samples": {"type": "array", "items": {"type": "double"}},
                "State": {"type": "string", "enum": ["OK", "BAD"]},
            }},
        }
        result = coverage.StandardAvro(schema, "example.Observation").convert()
        parsed = avro.schema.parse(json.dumps(result))
        self.assertEqual("record", parsed.type)
        fields = {field["name"]: field for field in result["fields"]}
        self.assertEqual("array", fields["samples"]["type"]["type"])
        self.assertEqual(["null", "int"], fields["count"]["type"])
        self.assertEqual([], coverage.logical_type_errors(result, coverage.AVRO_FORMAT))

    def test_offset_timestamp_and_date_remain_strings(self):
        schema = {"type": "object", "required": ["timestamp", "date"], "properties": {
            "timestamp": {"type": "datetime"}, "date": {"type": "date"},
        }}
        result = coverage.StandardAvro(schema, "example.Observation").convert()
        self.assertEqual(["string", "string"], [field["type"] for field in result["fields"]])

    def test_tagged_choices_retain_selector_and_value(self):
        schema = {"type": "choice", "choices": {
            "Text": {"type": "string"}, "Number": {"type": "int32"},
        }}
        result = coverage.StandardAvro(schema, "example.Choice").convert()
        parsed = avro.schema.parse(json.dumps(result))
        self.assertEqual(["Text", "Number"], [branch.fields[0].name for branch in parsed.schemas])

    def test_unsupported_type_is_not_silently_widened(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            coverage.StandardAvro({"type": "unrecognized"}, "example.Bad").convert()


class LogicalTypeTests(unittest.TestCase):
    def test_nested_custom_and_wrong_backing_types_are_rejected(self):
        schema = {"type": "record", "name": "Record", "fields": [
            {"name": "a", "type": ["null", {"type": "array", "items": {"type": "long", "logicalType": "uint64"}}]},
            {"name": "b", "type": {"type": "map", "values": {"type": "string", "logicalType": "timestamp-millis"}}},
            {"name": "c", "type": "string", "logicalType": "uuid"},
        ]}
        errors = coverage.logical_type_errors(schema, coverage.AVRO_FORMAT)
        self.assertEqual(3, len(errors))
        self.assertTrue(any("nonstandard" in error for error in errors))
        self.assertTrue(any("requires" in error for error in errors))
        self.assertTrue(any("not the field" in error for error in errors))

    def test_decimal_bounds_and_fixed_sizes(self):
        invalid = [
            {"type": "bytes", "logicalType": "decimal", "precision": True},
            {"type": "bytes", "logicalType": "decimal", "precision": 3, "scale": 4},
            {"type": "fixed", "name": "Small", "size": 1, "logicalType": "decimal", "precision": 3},
            {"type": "fixed", "name": "Duration", "size": 16, "logicalType": "duration"},
        ]
        for schema in invalid:
            with self.subTest(schema=schema):
                self.assertTrue(coverage.logical_type_errors(schema, coverage.AVRO_FORMAT))
        self.assertEqual([], coverage.logical_type_errors({"type": "fixed", "name": "Small", "size": 1, "logicalType": "decimal", "precision": 2}, coverage.AVRO_FORMAT))

    def test_version_specific_logical_types(self):
        cases = [
            ({"type": "long", "logicalType": "timestamp-nanos"}, "Avro/1.11.3", False),
            ({"type": "long", "logicalType": "timestamp-nanos"}, "Avro/1.12.0", True),
            ({"type": "fixed", "name": "Uuid", "size": 16, "logicalType": "uuid"}, "Avro/1.11.3", False),
            ({"type": "fixed", "name": "Uuid", "size": 16, "logicalType": "uuid"}, "Avro/1.12.0", True),
            ({"type": "bytes", "logicalType": "big-decimal"}, "Avro/1.12.0", True),
            ({"type": "long", "logicalType": "local-timestamp-micros"}, "Avro/1.9.2", False),
        ]
        for schema, fmt, valid in cases:
            with self.subTest(schema=schema, format=fmt):
                self.assertEqual(valid, not coverage.logical_type_errors(schema, fmt))

    def test_default_data_is_not_treated_as_schema(self):
        schema = {"type": "record", "name": "Record", "fields": [{
            "name": "metadata", "type": {"type": "map", "values": "string"},
            "default": {"logicalType": "custom"},
        }]}
        self.assertEqual([], coverage.logical_type_errors(schema, coverage.AVRO_FORMAT))


if __name__ == "__main__":
    unittest.main()
