#!/usr/bin/env python3
"""Extract candidate upstream URLs from each source's README + CONTAINER.

For every source dir (one with both README.md and CONTAINER.md), scan the
markdown for external http(s) links. Heuristically classify them into:
  - homepage  : root path of the upstream provider site (no /api/ or /docs/)
  - api_docs  : any URL containing /docs, /api, /openapi, /swagger, /redoc,
                /developer, /reference, or a .yaml/.json OpenAPI spec link.

Emit a JSON map { source_id : { homepage, api_docs, candidates: [...] } }.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]

URL_RE = re.compile(r"https?://[^\s\)\]<>\"]+")

EXCLUDE_HOSTS = {
    "github.com", "raw.githubusercontent.com", "ghcr.io",
    "azure.microsoft.com", "portal.azure.com",
    "learn.microsoft.com", "docs.microsoft.com",
    "shields.io", "img.shields.io",
    "clemensv.github.io", "vasters.com",
    "creativecommons.org", "opensource.org",
    "python.org", "docker.com", "hub.docker.com",
    "wikipedia.org", "en.wikipedia.org", "de.wikipedia.org", "fr.wikipedia.org",
    "json-structure.github.io", "json-schema.org",
    "cloudevents.io", "www.iso.org",
    # Azure marketing / template / runtime hosts that appear in deploy buttons.
    "aka.ms", "servicebus.azure.net", "windows.net", "core.windows.net",
    "eventgrid.azure.net", "windows.net", "azurewebsites.net",
    "microsoft.com", "www.microsoft.com",
    # Generic infra
    "letsencrypt.org", "tools.ietf.org", "www.rfc-editor.org",
    "datatracker.ietf.org", "stackoverflow.com",
    "apache.org", "www.apache.org",
    "xregistry.io", "spec.openapis.org",
}

API_HINTS = (
    "/docs", "/api", "/openapi", "/swagger", "/redoc",
    "/developer", "/reference", ".yaml", ".json",
    "/help/api", "/data-services", "/sdk",
)


def classify(urls):
    seen = []
    seen_set = set()
    for u in urls:
        u = u.rstrip(".,);:'\"")
        if u in seen_set:
            continue
        try:
            p = urlparse(u)
        except Exception:
            continue
        host = (p.hostname or "").lower()
        if not host or host in EXCLUDE_HOSTS:
            continue
        seen.append(u)
        seen_set.add(u)
    api = None
    for u in seen:
        if any(h in u.lower() for h in API_HINTS):
            api = u
            break
    # Prefer the FIRST non-excluded URL in the README as the homepage
    # (per convention, READMEs introduce the upstream with a markdown
    # link in the opening paragraph). Fall back to most-mentioned host.
    homepage = None
    if seen:
        first_url = seen[0]
        p = urlparse(first_url)
        # If the first URL is a deep link, root it.
        if p.path and p.path != "/":
            homepage = f"{p.scheme}://{p.hostname}{p.path.rsplit('/', 1)[0] or '/'}"
            # Prefer the cleaner root if available
            root = f"{p.scheme}://{p.hostname}/"
            # Heuristic: if any other seen URL is exactly the root, use it.
            if root in seen:
                homepage = root
            else:
                homepage = first_url if len(p.path) < 40 else root
        else:
            homepage = first_url
    if api and homepage and api == homepage:
        api = None
    return homepage, api, seen[:25]


def main():
    out = {}
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        readme = d / "README.md"
        container = d / "CONTAINER.md"
        if not readme.exists() or not container.exists():
            continue
        text = readme.read_text(encoding="utf-8", errors="ignore") + "\n" + \
               container.read_text(encoding="utf-8", errors="ignore")
        urls = URL_RE.findall(text)
        homepage, api, cands = classify(urls)
        out[d.name] = {
            "homepage": homepage,
            "api_docs": api,
            "candidates": cands,
        }
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
