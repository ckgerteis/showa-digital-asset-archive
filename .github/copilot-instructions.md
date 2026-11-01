# Shōwa Digital Asset Archive: instructions for AI coding agents

Read `ethics.html` first. It is binding on agents as well as people.

## The one rule that matters

**Never write a catalog field from your own knowledge.** Every descriptive field in `catalog/fab.yml` (`title`, `creator`, `creator_url`, `licence`, `source_url`, `image`, `technical`) must be copied from the listing itself, through the Sketchfab API (`scripts/scrape_sketchfab.py`) or from a listing page you have actually fetched. Do not construct, complete or guess a URL or a Sketchfab UID. If you cannot fetch the listing, do not add the entry; put it in `catalog/quarantine.yml` with the reason. The v1 catalog contained 31 Sketchfab links that resolved to no model, which is why this rule exists.

Do not set `showa_fit` to anything except `unassessed`, and do not invent period tags. Curatorial fields are the curator's.

## Architecture

- Static GitHub Pages site, no build step. Bootstrap 5.3 and js-yaml from CDNs with SRI hashes.
- `catalog/fab.yml` is the single source of truth, validated against `catalog/schema.json`.
- `assets/catalog.js` renders both `catalog.html` and `ja/catalog.html` (it sets labels by `window.CATALOG_CONFIG.lang`). Change catalog behaviour there, once.
- English pages at the root; Japanese mirrors in `ja/`. A navigation change must be made in all twelve pages (six English, six Japanese).
- All catalog text is escaped in `assets/catalog.js` before it reaches the DOM; keep it that way.

## Workflow for a change to the catalog

1. Draft entries with `python scripts/scrape_sketchfab.py` (Sketchfab) or from the fetched listing page (other platforms).
2. Run `python scripts/validate_catalog.py`. It must pass.
3. Optionally run `python scripts/check_links.py`.
4. Write a commit message that says what changed in the data (for example, "Add 3 Sketchfab listings (skf-0059 to skf-0061)"). Never commit with a placeholder message.

## Conventions

- Romanisation: Modified Hepburn with macrons in running text (Shōwa, Omotesandō, 4-chōme). Tokyo, Kyoto, Osaka and Kobe take no macron. The repository slug stays `showa-digital-asset-archive`.
- Citations on the site: Chicago 18 author–date.
- British spelling of "licence" (noun) in prose; the UI word "Catalog" is kept as is.
- Do not add model files, textures or binaries to the repository.
- Do not add a backend, a database or a build tool.

## Testing locally

```bash
python3 -m http.server 8000
# http://localhost:8000/catalog.html
```

The catalog fetches the YAML over HTTP, so opening the file directly will not work.
