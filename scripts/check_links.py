#!/usr/bin/env python3
"""Check that every catalog listing still exists.

Sketchfab entries are checked through the public Sketchfab API (reliable, no token needed).
BOOTH items are checked through their public item data (/items/<id>.json), ニコニ立体 works through
/works/<id>.json, and open-data records through the portal page. Fab, CGTrader and Unity pages are fetched over HTTP; Fab and CGTrader often answer automated
requests with a bot challenge (403/202), which is reported as UNCONFIRMED rather than as a failure.

Usage: python scripts/check_links.py [--report outputs/link_report.md]
Exit status 1 if any listing is definitely gone (404/410) or a Sketchfab model no longer matches
its catalog title or creator.
"""
import argparse
import concurrent.futures as cf
import re
import sys
import urllib.error
import urllib.request
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (ShowaArchiveLinkCheck; +https://github.com/ckgerteis/showa-digital-asset-archive)"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # network error
        return None, str(e).encode()


def check(entry):
    url = entry["source_url"]
    if entry["source"] == "sketchfab":
        uid = re.search(r"([0-9a-f]{32})$", url).group(1)
        status, body = fetch(f"https://api.sketchfab.com/v3/models/{uid}")
        if status == 200:
            j = json.loads(body)
            drift = []
            if j.get("name") != entry["title"]:
                drift.append(f"title now '{j.get('name')}'")
            if j.get("user", {}).get("displayName") != entry["creator"]:
                drift.append(f"creator now '{j.get('user', {}).get('displayName')}'")
            return ("CHANGED", "; ".join(drift)) if drift else ("OK", "")
        if status in (404, 410):
            return "GONE", f"Sketchfab API {status}"
        return "UNCONFIRMED", f"Sketchfab API {status}"
    if entry["source"] == "booth":
        iid = re.search(r"/items/([0-9]+)", url).group(1)
        status, body = fetch(f"https://booth.pm/ja/items/{iid}.json")
        if status == 200:
            name = json.loads(body).get("name")
            return ("CHANGED", f"title now '{name}'") if name != entry["title"] else ("OK", "")
        if status in (404, 410):
            return "GONE", f"BOOTH {status}"
        return "UNCONFIRMED", f"BOOTH {status}"
    if entry["source"] == "niconi_3d":
        url = url + ".json"
    status, _ = fetch(url)
    if status and 200 <= status < 300 and status != 202:
        return "OK", ""
    if status in (404, 410):
        return "GONE", f"HTTP {status}"
    return "UNCONFIRMED", f"HTTP {status}" if status else "network error"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=None)
    args = ap.parse_args()
    data = yaml.safe_load((ROOT / "catalog/fab.yml").read_text(encoding="utf-8-sig"))
    with cf.ThreadPoolExecutor(6) as ex:
        results = list(ex.map(check, data))
    rows = [(e["id"], e["title"], s, d, e["source_url"]) for e, (s, d) in zip(data, results)]
    bad = [r for r in rows if r[2] in ("GONE", "CHANGED")]
    unconfirmed = [r for r in rows if r[2] == "UNCONFIRMED"]
    lines = [f"# Catalog link check", "",
             f"{len(rows)} listings checked: {len(rows) - len(bad) - len(unconfirmed)} OK, "
             f"{len(bad)} gone or changed, {len(unconfirmed)} unconfirmed (bot challenge or network).", ""]
    if bad:
        lines += ["## Gone or changed", "", "| id | title | status | detail |", "|---|---|---|---|"]
        lines += [f"| {i} | {t} | {s} | {d} |" for i, t, s, d, _ in bad] + [""]
    if unconfirmed:
        lines += ["## Unconfirmed", "", "| id | title | detail |", "|---|---|---|"]
        lines += [f"| {i} | {t} | {d} |" for i, t, s, d, _ in unconfirmed] + [""]
    report = "\n".join(lines)
    print(report)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(report, encoding="utf-8")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
