"""
This script generates documentation from an xRegistry JSON manifest file containing message groups and schema groups.

Usage:
    python printdoc.py <manifest_file> [--title <title>] [--description <description>]
Arguments:
    manifest_file: Path to the JSON manifest file.
    --title: Title of the documentation (replaces "Table of Contents"). Default is "Table of Contents".
    --description: Description added under the title. Default is an empty string.
Functions:
    main(): Parses command line arguments, reads the JSON manifest file, and generates documentation.
    generate_documentation(data, title, description): Generates the documentation content based on the provided data.
    process_message(msg, schemagroups): Processes individual messages and their metadata, generating documentation for attributes and schemas.
    resolve_schema(dataschemauri, schemagroups): Resolves the schema URL to retrieve the corresponding schema from the schema groups.
    generate_anchor(name): Generates a markdown-compatible anchor from a given name.
    print_schema(schema): Prints the schema documentation, including nested records and enums.
    print_record(schema, records_to_document, enums_to_document, documented_records): Prints the documentation for a record schema.
    get_field_type_str(field_type, records_to_document, enums_to_document): Returns a string representation of a field type, handling records and enums.
    print_enum(enum_schema, documented_enums): Prints the documentation for an enum schema.
"""

import json
import argparse
import io


def sanitize_cell(value):
    if value is None:
        return ''
    return str(value).replace('|', '\\|').replace('\n', ' ')

def main():
    parser = argparse.ArgumentParser(description='Generate documentation from a JSON manifest.')
    parser.add_argument('manifest_file', help='Path to the JSON manifest file.')
    parser.add_argument('--title', help='Title of the documentation (replaces "Table of Contents").', default='Table of Contents')
    parser.add_argument('--description', help='Description added under the title.', default='')
    parser.add_argument('--output', help='Optional output file path. Writes UTF-8 when provided.')
    args = parser.parse_args()

    with open(args.manifest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    document = generate_documentation(data, args.title, args.description)
    if args.output:
        with open(args.output, 'w', encoding='utf-8', newline='\n') as output_file:
            output_file.write(document)
    else:
        print(document, end='')

def generate_documentation(data, title, description):
    messagegroups = data.get('messagegroups', {})
    schemagroups = data.get('schemagroups', {})
    toc = []
    output_lines = []

    # Collect headings and content
    for mg_name, mg in messagegroups.items():
        mg_anchor = generate_anchor(f"Message Group: {mg_name}")
        mg_heading = f"## Message Group: {mg_name}\n"
        toc.append(f"- [{mg_name}](#{mg_anchor})")
        output_lines.append(mg_heading)

        messages = mg.get('messages', {})
        for msg_name, msg in messages.items():
            msg_anchor = generate_anchor(f"Message: {msg_name}")
            msg_heading = f"### Message: {msg_name}\n"
            toc.append(f"  - [{msg_name}](#{msg_anchor})")
            output_lines.append("---\n")
            output_lines.append(msg_heading)
            output_lines.extend(process_message(msg, schemagroups))

    buffer = io.StringIO()
    buffer.write(f"# {title}\n\n")
    if description:
        buffer.write(f"{description}\n\n")
    for line in toc:
        buffer.write(f"{line}\n")
    buffer.write("\n---\n\n")

    for line in output_lines:
        buffer.write(line)
        if not line.endswith('\n'):
            buffer.write('\n')

    return buffer.getvalue()

def process_message(msg, schemagroups):
    lines = []

    if msg.get('description'):
        lines.append(f"*{msg.get('description')}*\n")

    # CloudEvents Attributes Table (formerly Event Properties)
    lines.append("#### CloudEvents Attributes:\n")
    lines.append("| **Name**    | **Description** | **Type**     | **Required** | **Value** |")
    lines.append("|-------------|-----------------|--------------|--------------|-----------|")
    metadata = msg.get('envelopemetadata', {})
    for md_name, md in metadata.items():
        description = md.get('description', '')
        md_type = md.get('type', '')
        required = md.get('required', False)
        value = md.get('value', '')
        lines.append(f"| `{md_name}` | {description} | `{md_type}` | `{required}` | `{value}` |")
    lines.append("")

    # Resolve the schema
    dataschemauri = msg.get('dataschemauri')
    schema = resolve_schema(dataschemauri, schemagroups)
    if schema:
        lines.append("#### Schema:\n")
        lines.extend(print_schema(schema))
    else:
        lines.append("Schema not found.\n")
    return lines

def resolve_schema(dataschemauri, schemagroups):
    # dataschemauri is of the form "#/schemagroups/group_name/schemas/schema_name"
    if not dataschemauri.startswith("#/"):
        return None
    path = dataschemauri[2:].split('/')
    node = schemagroups
    for p in path[1:]:  # skip 'schemagroups' since node starts from schemagroups
        node = node.get(p)
        if node is None:
            return None
    # Node should now be the schema object
    # Get the latest version (assuming versions are numbered)
    versions = node.get('versions', {})
    if versions:
        latest_version_key = sorted(versions.keys(), key=int)[-1]
        latest_version = versions[latest_version_key]
        schema = latest_version.get('schema')
        return schema
    return None

def generate_anchor(name):
    # Generate anchors compatible with GitHub Flavored Markdown
    anchor = name.lower()
    anchor = ''.join(c for c in anchor if c.isalnum() or c in '- ')
    anchor = anchor.replace(' ', '-')
    return anchor

def print_schema(schema):
    if is_json_structure_schema(schema):
        return print_json_structure_schema(schema)

    lines = []
    records_to_document = []
    enums_to_document = []
    documented_records = set()
    documented_enums = set()
    lines.extend(print_record(schema, records_to_document, enums_to_document, documented_records))
    # Now document the nested records and enums
    while records_to_document or enums_to_document:
        if records_to_document:
            record_schema = records_to_document.pop(0)
            if record_schema.get('name') not in documented_records:
                lines.append("\n---\n")
                lines.extend(print_record(record_schema, records_to_document, enums_to_document, documented_records))
        elif enums_to_document:
            enum_schema = enums_to_document.pop(0)
            if enum_schema.get('name') not in documented_enums:
                lines.append("\n---\n")
                lines.extend(print_enum(enum_schema, documented_enums))
    return lines


def is_json_structure_schema(schema):
    return isinstance(schema, dict) and 'fields' not in schema and (
        'properties' in schema or '$root' in schema or 'definitions' in schema
    )


def resolve_json_pointer(document, pointer):
    if not pointer or not pointer.startswith('#/'):
        return None
    node = document
    for part in pointer[2:].split('/'):
        if not isinstance(node, dict):
            return None
        node = node.get(part)
        if node is None:
            return None
    return node


def resolve_json_structure_root(schema):
    root_pointer = schema.get('$root')
    if root_pointer:
        root = resolve_json_pointer(schema, root_pointer)
        if root is not None:
            return root
    return schema


def is_json_object_type(schema):
    type_value = schema.get('type')
    if type_value == 'object':
        return True
    if isinstance(type_value, list) and 'object' in type_value:
        return True
    return False


def primitive_type_name(type_name):
    return f"*{type_name}*"


def print_json_structure_schema(schema):
    lines = []
    objects_to_document = []
    documented_objects = set()

    root_schema = resolve_json_structure_root(schema)
    root_name = root_schema.get('name') or schema.get('name') or 'Root'
    objects_to_document.append((root_name, root_schema))

    while objects_to_document:
        object_name, object_schema = objects_to_document.pop(0)
        anchor_name = f"object-{generate_anchor(object_name)}"
        if anchor_name in documented_objects:
            continue
        documented_objects.add(anchor_name)
        if lines:
            lines.append("\n---\n")
        lines.extend(print_json_object(object_name, object_schema, objects_to_document))

    return lines


def print_json_object(object_name, schema, objects_to_document):
    lines = [f"##### Object: {object_name}\n"]
    description = schema.get('description', '')
    if description:
        lines.append(f"*{sanitize_cell(description)}*\n")

    properties = schema.get('properties', {})
    required = set(schema.get('required', []))

    lines.append("| **Field Name** | **Type** | **Unit** | **Required** | **Description** |")
    lines.append("|----------------|----------|----------|--------------|-----------------|")
    for field_name, field_schema in properties.items():
        field_type = get_json_structure_type_str(field_schema, objects_to_document, f"{object_name}.{field_name}")
        unit = get_json_structure_unit(field_schema)
        is_required = '`True`' if field_name in required else '`False`'
        description = sanitize_cell(field_schema.get('description', ''))
        lines.append(
            f"| `{field_name}` | {field_type} | {unit} | {is_required} | {description} |"
        )
    return lines


def get_json_structure_unit(schema):
    unit = schema.get('unit')
    symbol = schema.get('symbol')
    if unit and symbol and unit != symbol:
        return sanitize_cell(f"{unit} ({symbol})")
    if symbol:
        return sanitize_cell(symbol)
    if unit:
        return sanitize_cell(unit)
    return '-'


def get_json_structure_type_str(schema, objects_to_document, fallback_name):
    type_value = schema.get('type')

    if type_value == 'array':
        items = schema.get('items', {})
        item_type = get_json_structure_type_str(items, objects_to_document, f"{fallback_name}Item")
        return f"array of {item_type}"

    if is_json_object_type(schema):
        object_name = schema.get('name') or fallback_name
        objects_to_document.append((object_name, schema))
        return f"[Object {object_name}](#object-{generate_anchor(object_name)})"

    if isinstance(type_value, list):
        nullable = 'null' in type_value
        rendered_types = []
        for member_type in type_value:
            if member_type == 'null':
                continue
            if member_type == 'object' and is_json_object_type(schema):
                object_name = schema.get('name') or fallback_name
                objects_to_document.append((object_name, schema))
                rendered_types.append(f"[Object {object_name}](#object-{generate_anchor(object_name)})")
            else:
                rendered_types.append(primitive_type_name(member_type))
        suffix = ' (optional)' if nullable else ''
        return ', '.join(rendered_types) + suffix

    if isinstance(type_value, str):
        return primitive_type_name(type_value)

    return '*unknown*'

def print_record(schema, records_to_document, enums_to_document, documented_records):
    lines = []
    record_name = schema.get('name')
    record_anchor = generate_anchor(f"Record: {record_name}")

    if record_name in documented_records:
        return lines  # Already documented
    documented_records.add(record_name)

    lines.append(f"##### Record: {record_name}\n")
    doc = schema.get('doc', '')
    if doc:
        lines.append(f"*{doc}*\n")
    fields = schema.get('fields', [])
    lines.append("| **Field Name** | **Type** | **Description** |")
    lines.append("|----------------|----------|-----------------|")
    for field in fields:
        field_name = field.get('name')
        field_type = field.get('type')
        field_doc = field.get('doc', '')
        field_type_str = get_field_type_str(field_type, records_to_document, enums_to_document)
        lines.append(f"| `{field_name}` | {field_type_str} | {sanitize_cell(field_doc)} |")
    return lines

def get_field_type_str(field_type, records_to_document, enums_to_document):
    if isinstance(field_type, dict):
        type_name = field_type.get('type')
        if type_name == 'enum':
            enum_name = field_type.get('name')
            enums_to_document.append(field_type)
            return f"[Enum {enum_name}](#enum-{generate_anchor(enum_name)})"
        elif type_name == 'record':
            record_name = field_type.get('name')
            records_to_document.append(field_type)
            return f"[Record {record_name}](#record-{generate_anchor(record_name)})"
        else:
            return f"*{type_name}*"
    elif isinstance(field_type, list):
        # Union type
        types = [t for t in field_type if t != 'null']
        optional = ' (optional)' if 'null' in field_type else ''
        type_names = []
        for t in types:
            if isinstance(t, str):
                type_names.append(f"*{t}*")
            elif isinstance(t, dict):
                type_name = t.get('type')
                if type_name == 'record':
                    record_name = t.get('name')
                    records_to_document.append(t)
                    type_names.append(f"[Record {record_name}](#record-{generate_anchor(record_name)})")
                elif type_name == 'enum':
                    enum_name = t.get('name')
                    enums_to_document.append(t)
                    type_names.append(f"[Enum {enum_name}](#enum-{generate_anchor(enum_name)})")
                else:
                    type_names.append(f"*{type_name}*")
        return ', '.join(type_names) + optional
    else:
        return f"*{field_type}*"

def print_enum(enum_schema, documented_enums):
    lines = []
    enum_name = enum_schema.get('name')
    enum_anchor = generate_anchor(f"Enum: {enum_name}")

    if enum_name in documented_enums:
        return lines  # Already documented
    documented_enums.add(enum_name)

    lines.append(f"##### Enum: {enum_name}\n")
    doc = enum_schema.get('doc', '')
    if doc:
        lines.append(f"*{doc}*\n")

    symbols = enum_schema.get('symbols', [])
    ordinals_from_schema = enum_schema.get('ordinals', {})
    # Generate ordinals: use provided ordinals or default to position index
    ordinals = {}
    for idx, symbol in enumerate(symbols):
        if ordinals_from_schema:
            ordinal = ordinals_from_schema.get(symbol, idx)
        else:
            ordinal = idx
        ordinals[symbol] = ordinal

    lines.append("| **Symbol** | **Ordinal** | **Description** |")
    lines.append("|------------|-------------|-----------------|")
    for symbol in symbols:
        ordinal = ordinals.get(symbol, '')
        lines.append(f"| `{symbol}` | {ordinal} |  |")
    return lines

if __name__ == '__main__':
    main()
