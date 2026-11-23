"""Reproduce the native contract from the checked-in upstream evidence and reviewed mapping."""

import copy
import json
from pathlib import Path

from avrotize.jstructtoavro import JsonStructureToAvro


def rooted_avro(schema, root_name):
    """Inline first-use Avro declarations into the selected payload record."""
    records = {f"{item.get('namespace', '')}.{item['name']}": item for item in schema}
    declared = set()

    def expand(node, namespace):
        if isinstance(node, str):
            qualified = node if "." in node else f"{namespace}.{node}"
            if qualified in records and qualified not in declared:
                declared.add(qualified)
                return expand(copy.deepcopy(records[qualified]), namespace)
            return node
        elif isinstance(node, list):
            if "null" in node:
                node.remove("null")
                node.insert(0, "null")
            return [expand(value, namespace) for value in node]
        elif isinstance(node, dict):
            for key in ("type", "items", "values", "fields"):
                if key in node:
                    node[key] = expand(node[key], node.get("namespace", namespace))
        return node

    return expand(root_name, root_name.rsplit(".", 1)[0])

ROOT = Path(__file__).parent
NS = "USGS.WaterData"
BASE = "https://api.waterdata.usgs.gov/ogcapi/v1"
EVIDENCE = json.loads((ROOT / "tests/fixtures/contract-evidence.json").read_text(encoding="utf-8"))


def field(kind, description, **annotations):
    return {"type": kind, "description": description, **annotations}


def obj(description, properties, required=()):
    return {"type": "object", "description": description, "properties": properties, "required": list(required)}


def document(name, record, definitions=None):
    record["name"] = name
    return {
        "$schema": "https://json-structure.org/meta/extended/v0/#",
        "$id": f"https://schemas.real-time-sources.dev/usgs/waterdata/{name}/v1",
        "$uses": ["JSONStructureUnits", "JSONStructureAlternateNames", "JSONStructureValidation"],
        "name": name, "description": record["description"], "$root": f"#/definitions/USGS/WaterData/{name}",
        "definitions": {"USGS": {"WaterData": {name: record, **(definitions or {})}}},
    }


def upstream(collection):
    schema = EVIDENCE["collections"][collection]["schema"]
    props = {}
    for key, raw in schema["properties"].items():
        if key == "geometry":
            continue
        description = raw.get("description", "").strip().replace("\ufffd", "'")
        kind = "double" if raw["type"] == "number" else "string"
        if key in {"time", "revision_created", "revision_modified", "begin", "end"}:
            kind = "datetime"
        if key == "data_gap_interval":
            kind = "duration"
        description += f" Source: {BASE}/collections/{collection}/schema."
        props[key] = field([kind, "null"], description)
    return props


def main():
    geometry = obj(
        "OGC GeoJSON Point in EPSG:4326; coordinates are longitude then latitude in decimal degrees. "
        "The original survey datum remains on the monitoring-location reference.",
        {"type": field("string", "GeoJSON geometry discriminator; monitoring locations use Point.", const="Point"),
         "coordinates": field("array", "Longitude and latitude in decimal degrees, in that order.",
                              items=field("double", "WGS84 coordinate ordinate in degrees.", unit="deg", symbol="°"),
                              minItems=2, maxItems=2)}, ("type", "coordinates"))
    period = obj(
        "One effective interval of an AQUARIUS threshold, as returned in the live "
        "time-series-metadata thresholds[].Periods array. Values use the containing series units.",
        {
            "start_time": field(["datetime", "null"], "Inclusive RFC3339 threshold interval boundary from StartTime. "
                                "The JSON publisher preserves the original fractional precision and offset, including "
                                "year-0001 sentinel boundaries.", altnames={"upstream": "StartTime"}),
            "end_time": field(["datetime", "null"], "RFC3339 threshold interval end boundary from EndTime. "
                              "Year 9999 is used as an open-ended sentinel; the JSON publisher preserves all seven fractional digits.",
                              altnames={"upstream": "EndTime"}),
            "applied_time": field(["datetime", "null"], "RFC3339 AQUARIUS AppliedTime timestamp for this threshold interval. "
                                  "The JSON publisher preserves the original offset and seven-digit fractional precision; "
                                  "year-0001 sentinel dates can occur.", altnames={"upstream": "AppliedTime"}),
            "comments": field(["string", "null"], "Optional operator Comments attached to this effective threshold period; "
                              "preserved without HTML decoding.", altnames={"upstream": "Comments"}),
            "suppress_data": field(["boolean", "null"], "AQUARIUS SuppressData flag indicating whether the threshold "
                                   "period suppresses values from publication.", altnames={"upstream": "SuppressData"}),
            "reference_value": field(["double", "null"], "Primary numeric ReferenceValue of the threshold. Units are "
                                     "the containing time-series unit_of_measure, not a fixed schema-wide unit.",
                                     altnames={"upstream": "ReferenceValue"}),
            "secondary_reference_value": field(["double", "null"], "Optional second numeric bound SecondaryReferenceValue. "
                                               "Uses the same units as the containing time series.",
                                               altnames={"upstream": "SecondaryReferenceValue"}),
        })
    threshold = obj(
        "A named numeric limit in the live USGS time-series-metadata thresholds array. "
        "The published schema incorrectly calls this a string. Field names and meanings are grounded "
        "in the captured live AQUARIUS object; open string labels avoid claiming an undocumented closed enumeration.",
        {
            "name": field(["string", "null"], "AQUARIUS Name identifying the threshold for operators and displays.",
                          altnames={"upstream": "Name"}),
            "type": field(["string", "null"], "AQUARIUS Type label; observed None, ThresholdAbove and ThresholdBelow. "
                          "The upstream schema publishes no exhaustive vocabulary.", altnames={"upstream": "Type"}),
            "periods": field("array", "Effective periods supplied in the upstream Periods array.",
                             items={"type": {"$ref": "#/definitions/USGS/WaterData/ThresholdPeriod"}},
                             altnames={"upstream": "Periods"}),
            "severity": field(["int32", "null"], "Upstream AQUARIUS Severity integer; zero occurs in the evidence. "
                              "No severity scale is documented by the selected USGS schema.", altnames={"upstream": "Severity"}),
            "description": field(["string", "null"], "AQUARIUS Description of the threshold purpose and display meaning.",
                                 altnames={"upstream": "Description"}),
            "display_color": field(["string", "null"], "DisplayColor string supplied by AQUARIUS, for example #990600.",
                                   altnames={"upstream": "DisplayColor"}),
            "reference_code": field(["string", "null"], "ReferenceCode label categorizing the threshold publication or "
                                    "operational use, preserved without reinterpretation.", altnames={"upstream": "ReferenceCode"}),
            "processing_order": field(["string", "null"], "AQUARIUS ProcessingOrder label; Suppression occurs in the "
                                      "captured responses. The upstream publishes no closed vocabulary.",
                                      altnames={"upstream": "ProcessingOrder"}),
        }, ("periods",))
    identity = field("string", "Native opaque USGS time-series identifier, equal to time-series-metadata.id and "
                     "continuous.time_series_id. Never a legacy numeric NWIS TS_ID.", minLength=1)
    geometry_field = field([{"$ref": "#/definitions/USGS/WaterData/Point"}, "null"],
                           "OGC feature geometry; null when the reference collection has no geometry.")
    observation = upstream("continuous")
    observation["time_series_id"] = copy.deepcopy(identity)
    observation["time"] = field("datetime", observation["time"]["description"])
    observation["last_modified"]["type"] = ["datetime", "null"]
    observation["geometry"] = copy.deepcopy(geometry_field)
    observation["feature_id"] = field(["string", "null"], "OGC continuous feature id from the outer Feature; "
                                      "a database record identifier, not the series identity or dedupe key.",
                                      altnames={"upstream": "Feature.id"})
    observation["parameter_code"]["pattern"] = "^[0-9]{5}$"
    records = {"ContinuousObservation": document("ContinuousObservation", obj(
        "Native USGS continuous observation, including approval, qualifier, method category and exact value text. "
        "Corrections are events for the same series and observation instant when scientific content changes.",
        observation, ("time_series_id", "time")), {"Point": geometry})}
    series = upstream("time-series-metadata")
    series.pop("id")
    series["time_series_id"] = copy.deepcopy(identity)
    series["time_series_id"]["altnames"] = {"upstream": "id"}
    series["geometry"] = copy.deepcopy(geometry_field)
    series["last_modified"]["description"] += " The live metadata API omits a timezone on some values; "
    series["last_modified"]["description"] += "the original text is retained without assigning an unreported offset."
    series["thresholds"] = field("array", upstream("time-series-metadata")["thresholds"]["description"] +
                                " Modeled from the live array, including effective periods; not the incorrect published string.",
                                items={"type": {"$ref": "#/definitions/USGS/WaterData/Threshold"}})
    records["TimeSeries"] = document("TimeSeries", obj(
        "Reference metadata for one native instantaneous Points time series. Only computation_identifier=Instantaneous "
        "and computation_period_identifier=Points are emitted; other OGC products are out of scope.",
        series, ("time_series_id", "thresholds")),
        {"Point": geometry, "Threshold": threshold, "ThresholdPeriod": period})
    for name, collection, member in (
        ("MonitoringLocation", "monitoring-locations", "location"),
        ("Parameter", "parameter-codes", "parameter"),
    ):
        props = upstream(collection)
        props["geometry"] = copy.deepcopy(geometry_field)
        if name == "MonitoringLocation":
            for key, unit, symbol in (
                ("altitude", "ft", "ft"), ("altitude_accuracy", "ft", "ft"),
                ("well_constructed_depth", "ft", "ft"), ("hole_constructed_depth", "ft", "ft"),
                ("drainage_area", "mi^2", "mi²"), ("contributing_drainage_area", "mi^2", "mi²"),
            ):
                props[key].update(unit=unit, symbol=symbol)
            props["construction_date"]["description"] += " Preserved as upstream text because partial dates can occur."
        else:
            props["id"]["pattern"] = "^[0-9]{5}$"
        detail = f"{name}Metadata"
        records[name] = document(name, obj(
            f"{name} reference attached to each native series that uses it. The time_series_id attachment is the "
            "existing relationship from time-series-metadata, not a new property claimed on the upstream resource.",
            {"time_series_id": copy.deepcopy(identity),
             member: field({"$ref": f"#/definitions/USGS/WaterData/{detail}"},
                           f"Complete {collection} properties plus its OGC geometry.")},
            ("time_series_id", member)),
            {detail: obj(f"Complete selected USGS {collection} resource properties and geometry.", props), "Point": geometry})
    manifest = {
        "name": "USGS Water Data",
        "description": "Native USGS continuous water observations and their monitoring-location, time-series and "
                       "parameter references. Consumers receive exact observation values, provisional status, "
                       "sensor qualifiers, threshold history and acknowledged corrections on Kafka, MQTT or AMQP.",
        "documentation": {"url": "README.md", "description": "Upstream scope, source interpretation and deployment options."},
        "endpoints": {}, "messagegroups": {}, "schemagroups": {
        f"{NS}.jstruct": {"schemas": {}}, f"{NS}.avro": {"schemas": {}}}}
    messages = {}
    for name, schema in records.items():
        type_id = f"{NS}.{name}"
        description = schema["definitions"]["USGS"]["WaterData"][name]["description"]
        manifest["schemagroups"][f"{NS}.jstruct"]["schemas"][type_id] = {
            "name": name, "description": description, "format": "JsonStructure/draft-02", "defaultversionid": "1",
            "versions": {"1": {"description": description, "format": "JsonStructure/draft-02", "schema": schema}}}
        avro = rooted_avro(JsonStructureToAvro().convert(schema), type_id)
        avro["description"] = description
        manifest["schemagroups"][f"{NS}.avro"]["schemas"][type_id] = {
            "name": name, "description": description, "format": "Avro/1.11.3", "defaultversionid": "1",
            "versions": {"1": {"description": description, "format": "Avro/1.11.3", "schema": avro}}}
        messages[type_id] = {
            "name": name, "description": schema["definitions"]["USGS"]["WaterData"][name]["description"],
            "envelope": "CloudEvents/1.0", "envelopemetadata": {
                "type": {"value": type_id}, "source": {"value": f"{BASE}/collections/continuous"},
                "subject": {"type": "uritemplate", "value": "{time_series_id}"}},
            "dataschemaformat": "JsonStructure/draft-02",
            "dataschemauri": f"#/schemagroups/{NS}.jstruct/schemas/{type_id}",
        }
    manifest["messagegroups"][NS] = {"description": "Native USGS continuous observations and their selected reference resources.", "messages": messages}
    leaves = {"ContinuousObservation": "observation", "TimeSeries": "time-series", "MonitoringLocation": "monitoring-location", "Parameter": "parameter"}
    for transport, protocol in (("kafka", "KAFKA"), ("mqtt", "MQTT/5.0"), ("amqp", "AMQP/1.0")):
        group_id = f"{NS}.{transport}"
        derived = {}
        for name in records:
            options = {}
            if transport == "kafka":
                options = {"key": "{time_series_id}"}
            elif transport == "mqtt":
                options = {"topic_name": f"hydro/us/usgs/waterdata/{{time_series_id}}/{leaves[name]}",
                           "qos": 1, "retain": name != "ContinuousObservation"}
            else:
                options = {
                    "properties": {"subject": {"type": "uritemplate", "value": "{time_series_id}"}},
                    "message_annotations": {"x-opt-partition-key": {"type": "uritemplate", "value": "{time_series_id}",
                                            "description": "Native series partition identity, same as the CloudEvent subject."}}}
            derived[f"{group_id}.{name}"] = {
                "name": name, "basemessageuri": f"/messagegroups/{NS}/messages/{NS}.{name}",
                "protocol": protocol, "protocoloptions": options}
        manifest["messagegroups"][group_id] = {"description": f"{protocol} binding of native USGS Water Data events.", "messages": derived}
        manifest["endpoints"][f"{NS}.{transport.title()}"] = {
            "usage": ["producer"], "protocol": protocol, "envelope": "CloudEvents/1.0",
            "envelopeoptions": {"mode": "structured" if transport == "kafka" else "binary"},
            "messagegroups": [f"#/messagegroups/{group_id}"],
            "protocoloptions": {"deployed": False, "options": {"topic": "usgs-waterdata", "key": "{time_series_id}"}}
            if transport == "kafka" else {"deployed": False, "endpoints": [{"uri": "mqtt://localhost:1883" if transport == "mqtt"
                                                                       else "amqp://localhost:5672/usgs-waterdata"}]},
        }
    (ROOT / "xreg").mkdir(exist_ok=True)
    (ROOT / "xreg/usgs-waterdata.xreg.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Authored four native JSON Structure schemas and generated their parallel Avro contracts.")


if __name__ == "__main__":
    main()
