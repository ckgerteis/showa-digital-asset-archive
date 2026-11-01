#!/usr/bin/env python3
"""Draft schema-v2 catalog entries from Sketchfab model URLs.

Reads one Sketchfab model URL per line from catalog/sketchfab_urls.txt, looks each model up
through the public Sketchfab API, and writes draft entries to outputs/new_entries.yml (git-ignored).
Title, creator, licence, thumbnail and polygon counts come from the listing itself. Period tags,
object tags and notes are left for the curator; showa_fit starts as 'unassessed'.

Review the drafts, give each a free id, complete the curatorial fields, paste into catalog/fab.yml,
then run scripts/validate_catalog.py.

Usage: python scripts/scrape_sketchfab.py
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
URL_FILE = ROOT / "catalog" / "sketchfab_urls.txt"
OUT = ROOT / "outputs" / "new_entries.yml"
UA = {"User-Agent": "Mozilla/5.0 (ShowaArchive)"}
LICENCE = {
    "CC Attribution": "CC BY 4.0", "CC Attribution-NonCommercial": "CC BY-NC 4.0",
    "CC Attribution-ShareAlike": "CC BY-SA 4.0", "CC Attribution-NoDerivs": "CC BY-ND 4.0",
    "CC Attribution-NonCommercial-ShareAlike": "CC BY-NC-SA 4.0",
    "CC Attribution-NonCommercial-NoDerivs": "CC BY-NC-ND 4.0", "CC0 Public Domain": "CC0 1.0",
    "Standard": "Sketchfab Standard (paid)", "Editorial": "Sketchfab Editorial (editorial use only)",
}


def model(uid):
    req = urllib.request.Request(f"https://api.sketchfab.com/v3/models/{uid}", headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": e.code}


def main():
    if not URL_FILE.exists():
        sys.exit("Create catalog/sketchfab_urls.txt with one Sketchfab model URL per line.")
    urls = [u.strip() for u in URL_FILE.read_text(encoding="utf-8-sig").splitlines() if u.strip()]
    drafts, failures = [], []
    for url in urls:
        m = re.search(r"([0-9a-f]{32})/?$", url)
        if not m:
            failures.append((url, "no 32-character model UID in URL"))
            continue
        j = model(m.group(1))
        time.sleep(0.3)
        if "_error" in j:
            failures.append((url, f"Sketchfab API {j['_error']}"))
            continue
        lic = (j.get("license") or {}).get("label") if isinstance(j.get("license"), dict) else None
        imgs = j.get("thumbnails", {}).get("images", [])
        drafts.append({
            "id": "skf-XXXX",
            "title": j["name"],
            "source": "sketchfab",
            "source_url": j["viewerUrl"],
            "creator": j["user"]["displayName"],
            "creator_url": j["user"]["profileUrl"],
            "licence": LICENCE.get(lic, lic) if lic else "View only (not downloadable)",
            "period_tags": ["unassigned"],
            "object_tags": [],
            "historical_notes": "",
            "showa_fit": "unassessed",
            "image": sorted(imgs, key=lambda i: abs(i["width"] - 640))[0]["url"] if imgs else None,
            "technical": {"faces": j.get("faceCount"), "vertices": j.get("vertexCount"),
                          "downloadable": j.get("isDownloadable")},
            "verification": {"status": "verified", "method": "sketchfab-api", "checked": date.today().isoformat()},
            "_listing_description": (j.get("description") or "")[:400],
        })
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(yaml.safe_dump(drafts, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"{len(drafts)} draft entries written to {OUT.relative_to(ROOT)}")
    for url, why in failures:
        print(f"NOT DRAFTED: {url} ({why})")


if __name__ == "__main__":
    main()
