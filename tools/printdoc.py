import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate documentation from a JSON manifest.')
    parser.add_argument('manifest_file', help='Path to the JSON manifest file.')
    parser.add_argument('--title', help='Title of the documentation (replaces "Table of Contents").', default='Table of Contents')
    parser.add_argument('--description', help='Description added under the title.', default='')
    args = parser.parse_args()

    with open(args.manifest_file, 'r') as f:
        data = json.load(f)

    # Generate documentation with updated features
    generate_documentation(data, args.title, args.description)

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
            output_lines.append(msg_heading)
            output_lines.extend(process_message(msg, schemagroups))

    # Print Title and Description
    print(f"# {title}\n")
    if description:
        print(f"{description}\n")
    for line in toc:
        print(line)
    print("\n---\n")

    # Print documentation
    for line in output_lines:
        print(line)

def process_message(msg, schemagroups):
    lines = []

    if msg.get('description'):
        lines.append(f"*{msg.get('description')}*\n")

    # CloudEvents Attributes Table (formerly Event Properties)
    lines.append("#### CloudEvents Attributes:\n")
    lines.append("| **Name**    | **Description** | **Type**     | **Required** | **Value** |")
    lines.append("|-------------|-----------------|--------------|--------------|-----------|")
    metadata = msg.get('metadata', {})
    for md_name, md in metadata.items():
        description = md.get('description', '')
        md_type = md.get('type', '')
        required = md.get('required', False)
        value = md.get('value', '')
        lines.append(f"| `{md_name}` | {description} | `{md_type}` | `{required}` | `{value}` |")
    lines.append("")

    # Resolve the schema
    schemaurl = msg.get('schemaurl')
    schema = resolve_schema(schemaurl, schemagroups)
    if schema:
        lines.append("#### Schema:\n")
        lines.extend(print_schema(schema))
    else:
        lines.append("Schema not found.\n")
    return lines

def resolve_schema(schemaurl, schemagroups):
    # schemaurl is of the form "#/schemagroups/group_name/schemas/schema_name"
    if not schemaurl.startswith("#/"):
        return None
    path = schemaurl[2:].split('/')
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
        lines.append(f"| `{field_name}` | {field_type_str} | {field_doc} |")
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
