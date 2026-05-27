import requests, json, re

# 1. BW HVZ - the JS loads data from somewhere. Look at hvz_site_base.js for the data URL
print("=== BW HVZ hvz_site_base.js ===")
r = requests.get('https://hvz.lubw.baden-wuerttemberg.de/js/hvz_site_base.js', timeout=10)
if r.status_code == 200:
    # Find path/URL patterns
    paths = re.findall(r'Path[^=]*=\s*["\']([^"\']+)["\']', r.text)
    urls = re.findall(r'["\']([^"\']+(?:\.csv|\.json|\.xml|\.txt|\.dat|\.js|\.php)[^"\']*)["\']', r.text)
    data_refs = re.findall(r'["\']data/([^"\']+)["\']', r.text)
    print(f"Paths: {paths[:20]}")
    print(f"Data files: {urls[:20]}")
    print(f"Data refs: {data_refs[:10]}")
    # Look for DAT. patterns that indicate data loading
    dat_patterns = re.findall(r'(DAT\.[A-Z_]+)', r.text)
    print(f"DAT patterns: {list(set(dat_patterns))[:15]}")
print()

# 2. Sachsen WFS - extract actual feature type from WFS capabilities
print("=== Sachsen WFS FeatureType ===")
r2 = requests.get('https://luis.sachsen.de/arcgis/services/wasser/pegelnetz/MapServer/WFSServer',
                   params={'request': 'GetCapabilities', 'service': 'WFS'}, timeout=15)
# Find FeatureType names between <Name> tags within <FeatureType> blocks
feature_blocks = re.findall(r'<FeatureType>(.*?)</FeatureType>', r2.text, re.DOTALL)
for block in feature_blocks:
    name = re.search(r'<Name>(.*?)</Name>', block)
    title = re.search(r'<Title>(.*?)</Title>', block)
    if name:
        n = name.group(1)
        t = title.group(1) if title else ''
        print(f"  FeatureType: {n} ({t})")
print()

# If we found types, fetch one
print("=== Sachsen WFS GetFeature ===")
for block in feature_blocks:
    name = re.search(r'<Name>(.*?)</Name>', block)
    if name:
        tn = name.group(1)
        r3 = requests.get('https://luis.sachsen.de/arcgis/services/wasser/pegelnetz/MapServer/WFSServer',
                          params={'request': 'GetFeature', 'service': 'WFS', 'version': '2.0.0',
                                  'typeNames': tn, 'count': '3', 'outputFormat': 'GEOJSON'},
                          timeout=15)
        ct = r3.headers.get('Content-Type', '')
        print(f"  {tn}: status={r3.status_code} CT={ct[:40]}")
        if 'json' in ct.lower() and r3.status_code == 200:
            print(json.dumps(r3.json(), indent=2, ensure_ascii=False)[:1000])
        elif r3.status_code == 200:
            print(r3.text[:500])
        break
print()

# 3. Try BW HVZ data directory probe
print("=== BW HVZ data probes ===")
for test_url in [
    'https://hvz.lubw.baden-wuerttemberg.de/data/',
    'https://hvz.lubw.baden-wuerttemberg.de/data/pegel.js',
    'https://hvz.lubw.baden-wuerttemberg.de/data/pegel.json',
    'https://hvz.lubw.baden-wuerttemberg.de/data/PEG/',
    'https://hvz.lubw.baden-wuerttemberg.de/data/peg_tab.json',
    'https://hvz.lubw.baden-wuerttemberg.de/data/PEG/tab/',
    'https://hvz.lubw.baden-wuerttemberg.de/daten/PEG/',
]:
    try:
        r4 = requests.get(test_url, timeout=5)
        ct = r4.headers.get('Content-Type','')[:40]
        is_json = r4.text.strip()[:1] in ('{','[')
        size = len(r4.text)
        print(f"  {test_url[-40:]}: {r4.status_code} [{ct}] json={is_json} size={size}")
        if (is_json or 'javascript' in ct.lower() or 'json' in ct.lower()) and r4.status_code == 200 and size > 100:
            print(f"    >>> DATA FOUND!")
            print(f"    {r4.text[:300]}")
    except Exception as e:
        print(f"  {test_url}: FAIL")
