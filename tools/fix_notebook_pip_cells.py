"""Update all notebook pip cells to fix cloudevents.kafka import ordering bug."""
import json, re, glob, os, sys

NEW_TEMPLATE = '''import subprocess, sys, glob as _glob, importlib

_wheels = _glob.glob('/lakehouse/default/Files/wheels/{slug}/*.whl')
# Install local wheels first (force-reinstall to avoid stale cached versions in Fabric env)
if _wheels:
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', '-q', '--force-reinstall', '--no-deps'] + _wheels
    )
# Install all PyPI deps including cloudevents and confluent_kafka together
# (cloudevents.kafka requires confluent_kafka to be present when first imported;
#  installing them together prevents Python from caching a failed import of cloudevents.kafka)
_pypi_deps = {pypi_deps}
subprocess.check_call(
    [sys.executable, '-m', 'pip', 'install', '-q', '--upgrade', '--force-reinstall'] + _pypi_deps
)
# Clear any cached import failures for cloudevents (import system caches failures; stale cache causes ModuleNotFoundError)
for _key in list(sys.modules.keys()):
    if _key.startswith('cloudevents'):
        del sys.modules[_key]
importlib.invalidate_caches()
print(f'Installed {{len(_wheels)}} wheel(s) + {{len(_pypi_deps)}} PyPI deps')
'''

updated = 0
skipped = 0

for nb_path in sorted(glob.glob('feeders/*/notebook/*.ipynb')):
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"SKIP {nb_path}: {e}")
        skipped += 1
        continue
    
    pip_cell_idx = -1
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code':
            src = ''.join(cell.get('source', []))
            if 'force-reinstall' in src and 'cloudevents' in src:
                pip_cell_idx = i
                break
    
    if pip_cell_idx < 0:
        continue
    
    src = ''.join(nb['cells'][pip_cell_idx].get('source', []))
    
    # Skip if already updated to new pattern
    if 'Clear any cached import failures' in src:
        print(f"ALREADY_UPDATED {os.path.basename(nb_path)}")
        continue
    
    # Extract slug from wheels glob path
    m = re.search(r"glob\(['\"].*?/wheels/([^/]+)/\*\.whl['\"]", src)
    if not m:
        print(f"SKIP (no slug) {nb_path}")
        skipped += 1
        continue
    slug = m.group(1)
    
    # Extract extra pypi deps (beyond standard set)
    standard_names = {'avro', 'dataclasses_json', 'confluent_kafka', 'cloudevents', 'requests'}
    extra_deps = []
    seen = set()
    for dep_m in re.finditer(r"'([a-zA-Z0-9_\-]+(?:[><=][^',\]]+)?)'", src):
        dep = dep_m.group(1)
        name = re.split(r'[>=<]', dep)[0].lower().replace('-', '_')
        if name not in standard_names and name not in seen and len(name) > 2:
            extra_deps.append(dep)
            seen.add(name)
    
    # Build pypi_deps list
    base_deps = ['avro>=1.11.3', 'dataclasses_json>=0.6.7', 'confluent_kafka>=2.5.3', 'cloudevents>=1.11.0,<2.0.0']
    all_deps = base_deps + extra_deps
    
    new_src = NEW_TEMPLATE.format(
        slug=slug,
        pypi_deps=repr(all_deps)
    )
    
    # Convert to notebook cell source format (list of lines with \n)
    lines = new_src.lstrip('\n').split('\n')
    nb['cells'][pip_cell_idx]['source'] = [line + '\n' for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    
    try:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"OK {slug}")
        updated += 1
    except Exception as e:
        print(f"ERROR {nb_path}: {e}")

print(f"\nUpdated: {updated}, Skipped: {skipped}")
