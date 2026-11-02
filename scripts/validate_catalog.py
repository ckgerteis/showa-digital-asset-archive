#!/usr/bin/env python3
"""Validate catalog/fab.yml against catalog/schema.json plus cross-entry rules.

Usage: python scripts/validate_catalog.py
Exit status 1 if any entry fails. Run by .github/workflows/catalog.yml on every push and pull request.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = yaml.safe_load((ROOT / "catalog/fab.yml").read_text(encoding="utf-8-sig"))
    schema = json.loads((ROOT / "catalog/schema.json").read_text(encoding="utf-8"))
    errors = []

    for err in Draft202012Validator(schema).iter_errors(data):
        loc = "/".join(str(p) for p in err.absolute_path)
        entry = data[err.absolute_path[0]]["id"] if err.absolute_path else "catalog"
        errors.append(f"{entry}: {loc}: {err.message}")

    for field in ("id", "source_url"):
        for value, n in Counter(e.get(field) for e in data).items():
            if n > 1:
                errors.append(f"duplicate {field}: {value} ({n} entries)")

    prefix = {"sketchfab": "skf", "fab": "fab", "cgtrader": "cgt", "unity_asset_store": "unity",
              "booth": "booth", "niconi_3d": "nico", "open_data": "od"}
    for e in data:
        if e.get("source") in prefix and not e.get("id", "").startswith(prefix[e["source"]] + "-"):
            errors.append(f"{e.get('id')}: id prefix does not match source {e.get('source')}")
        if e.get("source") == "sketchfab" and not re.search(r"[-/][0-9a-f]{32}$", e.get("source_url", "")):
            errors.append(f"{e.get('id')}: Sketchfab URL must end in a 32-character model UID")
        if "unassigned" in e.get("period_tags", []) and len(e["period_tags"]) > 1:
            errors.append(f"{e.get('id')}: 'unassigned' cannot be combined with other period tags")

    quarantined = {q["id"] for q in yaml.safe_load((ROOT / "catalog/quarantine.yml").read_text(encoding="utf-8")) or []}
    for e in data:
        if e.get("id") in quarantined:
            errors.append(f"{e['id']}: appears in both fab.yml and quarantine.yml")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) in catalog/fab.yml")
        sys.exit(1)
    print(f"catalog/fab.yml: {len(data)} entries valid")


if __name__ == "__main__":
    main()
