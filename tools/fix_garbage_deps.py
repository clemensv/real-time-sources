"""Fix notebooks where _pypi_deps contains garbage pip command fragments."""
import json, glob, re

STANDARD = [
    'avro>=1.11.3',
    'dataclasses_json>=0.6.7',
    'confluent_kafka>=2.5.3',
    'cloudevents>=1.11.0,<2.0.0',
]
STANDARD_NAMES = {re.split(r'[>=<]', x)[0].lower().replace('-', '_') for x in STANDARD}
GARBAGE = {'pip', 'install'}
GARBAGE_PREFIXES = ('-',)

fixed = 0
for path in sorted(glob.glob('feeders/*/notebook/*.ipynb')):
    nb = json.load(open(path, encoding='utf-8'))
    changed = False
    for cell in nb['cells']:
        if cell.get('cell_type') != 'code':
            continue
        # Reconstruct source as single string
        src = ''.join(cell.get('source', []))
        m = re.search(r'(_pypi_deps\s*=\s*)\[([^\]]+)\]', src, re.DOTALL)
        if not m:
            continue
        items_str = m.group(2)
        items = re.findall(r"'([^']+)'", items_str)
        # Keep only real package specs
        extra = []
        for item in items:
            name = re.split(r'[>=<]', item)[0].lower().replace('-', '_')
            if any(item.startswith(p) for p in GARBAGE_PREFIXES):
                continue
            if name in GARBAGE:
                continue
            if name in STANDARD_NAMES:
                continue  # will be added from STANDARD
            extra.append(item)
        final = STANDARD + extra
        new_deps_str = ', '.join(f"'{x}'" for x in final)
        new_block = f'{m.group(1)}[{new_deps_str}]'
        new_src = src[:m.start()] + new_block + src[m.end():]
        if new_src != src:
            # Re-encode as list of lines (each line as a string element)
            cell['source'] = [new_src]
            changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        fixed += 1

print(f'Fixed {fixed} notebooks')
