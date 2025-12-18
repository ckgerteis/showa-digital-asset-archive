#!/usr/bin/env python3
"""
scripts/scrape_sketchfab.py

Simple scraper and Sketchfab-API caller to produce CSV/JSON outputs.

Usage:
  - set SKETCHFAB_TOKEN environment variable to a Sketchfab API token for best results
  - run: python scripts/scrape_sketchfab.py
"""
import os
import re
import csv
import json
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
URL_FILE = ROOT / "catalog" / "sketchfab_urls.txt"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True, parents=True)

SKETCHFAB_API = "https://api.sketchfab.com/v3/models"
TOKEN = os.environ.get("SKETCHFAB_TOKEN")
HEADERS = {"User-Agent":"ShowaArchiveBot/1.0"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def extract_uid_from_url(url):
    m = re.search(r'([0-9a-f]{32})$', url)
    if m:
        return m.group(1)
    parts = url.rstrip('/').split('/')
    if parts:
        return parts[-1]
    return None

def fetch_api(uid_or_slug):
    url = f"{SKETCHFAB_API}/{uid_or_slug}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        return r.json()
    return None

def html_fallback(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    meta = {}
    og = {}
    for tag in soup.find_all("meta"):
        if tag.get("property", "").startswith("og:"):
            og[tag["property"]] = tag.get("content", "")
        if tag.get("name", "").startswith("twitter:"):
            meta[tag["name"]] = tag.get("content", "")
    author = None
    a = soup.find("a", {"rel": "author"})
    if a:
        author = {"name": a.text.strip(), "url": a.get("href")}
    title = og.get("og:title") or (soup.title.string if soup.title else None)
    desc = og.get("og:description") or meta.get("twitter:description")
    return {"title": title, "description": desc, "og": og, "meta": meta, "author": author, "html_snippet": soup.text[:800]}

def collect_one(url):
    out = {"original_url": url, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sketchfab_api_used": False, "errors": []}
    uid = extract_uid_from_url(url)
    if not uid:
        out["errors"].append("no_uid")
        try:
            hf = html_fallback(url)
            out.update(hf)
        except Exception as e:
            out["errors"].append(str(e))
        return out
    api_data = None
    if TOKEN:
        try:
            api_data = fetch_api(uid)
            time.sleep(0.25)
        except Exception as e:
            out["errors"].append(f"api_error:{e}")
    if api_data:
        out["sketchfab_api_used"] = True
        out["id"] = api_data.get("uid") or api_data.get("id")
        out["name"] = api_data.get("name")
        out["description"] = api_data.get("description")
        out["published_at"] = api_data.get("publishedAt")
        out["updated_at"] = api_data.get("updatedAt")
        out["is_downloadable"] = api_data.get("isDownloadable", api_data.get("downloadable"))
        user = api_data.get("user", {})
        out["author_name"] = user.get("displayName")
        out["author_username"] = user.get("username")
        out["author_url"] = user.get("profileUrl") or ("https://sketchfab.com/" + user.get("username",""))
        lic = None
        if api_data.get("license"):
            lic = api_data.get("license")
        elif api_data.get("license_info") and isinstance(api_data.get("license_info"), dict):
            lic = api_data['license_info'].get('type')
        out["license"] = lic
        arches = api_data.get("archives") or []
        fmts = []
        for a in arches:
            fmt = a.get("format")
            if fmt:
                fmts.append(fmt)
        out["formats"] = ",".join(fmts)
        out["faces"] = api_data.get("faces")
        out["vertices"] = api_data.get("vertices")
    else:
        try:
            hf = html_fallback(url)
            out.update(hf)
        except Exception as e:
            out["errors"].append(str(e))
    return out

def main():
    if not URL_FILE.exists():
        print("Create catalog/sketchfab_urls.txt with one URL per line.")
        return
    urls = [ln.strip() for ln in URL_FILE.read_text(encoding='utf8').splitlines() if ln.strip()]
    results = []
    for i,url in enumerate(urls,1):
        print(f"[{i}/{len(urls)}] {url}")
        try:
            r = collect_one(url)
            results.append(r)
        except Exception as e:
            results.append({"original_url": url, "error": str(e)})
        time.sleep(0.3)
    OUT_DIR.mkdir(exist_ok=True)
    jsonp = OUT_DIR / "sketchfab_metadata.json"
    csvp = OUT_DIR / "sketchfab_metadata.csv"
    with jsonp.open("w", encoding="utf8") as jf:
        json.dump(results, jf, ensure_ascii=False, indent=2)
    fields = ["original_url","id","name","description","author_name","author_username","author_url","license","is_downloadable","faces","vertices","formats","published_at","updated_at","sketchfab_api_used","fetched_at","errors"]
    with csvp.open("w", newline="", encoding="utf8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k,"") for k in fields})
    print("Wrote outputs to", OUT_DIR)
if __name__ == "__main__":
    main()