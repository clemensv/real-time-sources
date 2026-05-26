#!/usr/bin/env python3
"""Find upstream URLs per source by scanning all source files.

For each source dir, gather candidate upstream URLs from:
  - *.py files (the bridge — usually has the base URL as a constant)
  - xreg/*.xreg.json (description fields)
  - README.md / CONTAINER.md / EVENTS.md
  - Dockerfile labels

Output a JSON map { source_id : { all_candidates: [...] } } so a downstream
step (or human) can pick the right homepage + api_docs.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
URL_RE = re.compile(r"https?://[^\s\)\]<>\"'`,;]+")

EXCLUDE_HOSTS = {
    "github.com", "raw.githubusercontent.com", "ghcr.io",
    "azure.microsoft.com", "portal.azure.com",
    "learn.microsoft.com", "docs.microsoft.com",
    "shields.io", "img.shields.io",
    "clemensv.github.io", "vasters.com",
    "creativecommons.org", "opensource.org",
    "python.org", "docker.com", "hub.docker.com",
    "wikipedia.org", "en.wikipedia.org", "de.wikipedia.org", "fr.wikipedia.org",
    "json-structure.github.io", "json-schema.org", "json-structure.org",
    "cloudevents.io", "www.iso.org",
    "aka.ms", "servicebus.azure.net", "windows.net", "core.windows.net",
    "eventgrid.azure.net", "azurewebsites.net", "eventhubs.azure.net",
    "microsoft.com", "www.microsoft.com",
    "letsencrypt.org", "tools.ietf.org", "www.rfc-editor.org",
    "datatracker.ietf.org", "stackoverflow.com",
    "apache.org", "www.apache.org",
    "xregistry.io", "spec.openapis.org",
    "fastapi.tiangolo.com", "pydantic.dev", "pypi.org",
    "kafka.apache.org", "mosquitto.org", "rabbitmq.com",
    "qpid.apache.org",
    "example.com", "example.org", "example.test", "example.net",
    "schema.management.azure.com", "schemas.real-time-sources.dev",
    "real-time-sources.2030.io", "real-time-sources.dev",
}


def normalise(u: str) -> str | None:
    u = u.rstrip(".,);:'\"`,")
    # Strip trailing backticks/quotes/parens
    while u and u[-1] in ".,);:'\"`":
        u = u[:-1]
    try:
        p = urlparse(u)
    except Exception:
        return None
    if not p.hostname:
        return None
    if p.hostname.lower() in EXCLUDE_HOSTS:
        return None
    return u


def collect(d: Path) -> list[str]:
    urls = []
    for sub in d.rglob("*"):
        if not sub.is_file():
            continue
        if any(part in {"__pycache__", "node_modules", ".pytest_cache",
                        ".venv", "dist", "build"} for part in sub.parts):
            continue
        # Skip generated producer outputs
        if any(part.endswith("_producer") or part.endswith("_producer_data")
               or part.endswith("_kafka_producer") or part.endswith("_amqp_producer")
               or part.endswith("_mqtt_producer")
               for part in sub.parts):
            continue
        ext = sub.suffix.lower()
        if ext not in (".py", ".md", ".json", ".yaml", ".yml", ".dockerfile",
                       ".ps1", ".sh", ".txt"):
            continue
        try:
            text = sub.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in URL_RE.findall(text):
            u = normalise(m)
            if u:
                urls.append(u)
    return urls


API_HINTS = (
    "/api/", "/openapi", "/swagger", "/redoc",
    "/developer", "/reference", "/docs/api",
    "/data-services", "/sdk",
)
DOC_HINTS = ("/docs", "/help", "/documentation", "/wiki", "/manual")


def pick(urls):
    if not urls:
        return None, None
    cnt = Counter(urls)
    host_cnt = Counter(urlparse(u).hostname for u in urls)
    # Find the most-mentioned upstream host.
    top_host = host_cnt.most_common(1)[0][0]
    # Homepage: shortest URL on top host (root or near-root).
    same_host = [u for u in urls if urlparse(u).hostname == top_host]
    same_host_unique = sorted(set(same_host), key=lambda u: (len(urlparse(u).path), -cnt[u]))
    homepage = same_host_unique[0] if same_host_unique else None
    # Round homepage path to "/" if anything else under that host exists.
    if homepage:
        p = urlparse(homepage)
        if p.path and p.path != "/":
            homepage = f"{p.scheme}://{p.hostname}/"
    # API docs: first URL whose path matches an API/doc hint, preferring top host.
    api = None
    for u in [u for u in urls if urlparse(u).hostname == top_host] + urls:
        ul = u.lower()
        if any(h in ul for h in API_HINTS) or any(h in ul for h in DOC_HINTS):
            api = u
            break
    if api == homepage:
        api = None
    return homepage, api


def main():
    out = {}
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if not ((d / "README.md").exists() and (d / "CONTAINER.md").exists()):
            continue
        urls = collect(d)
        homepage, api_docs = pick(urls)
        host_cnt = Counter(urlparse(u).hostname for u in urls)
        top_hosts = [h for h, _ in host_cnt.most_common(5)]
        out[d.name] = {
            "homepage": homepage,
            "api_docs": api_docs,
            "top_hosts": top_hosts,
        }
    json.dump(out, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
