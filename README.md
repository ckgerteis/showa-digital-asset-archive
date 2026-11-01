# Shōwa Digital Asset Archive

**A curated index of externally hosted 3D models of material culture in Shōwa Japan (1926–1989), with provenance, licence and technical metadata for each listing.**
昭和時代（1926–1989）の物質文化を表す3Dモデルの掲載ページを、出所・ライセンス・技術情報とともに整理したインデックス。

Site: <https://ckgerteis.github.io/showa-digital-asset-archive/> · Directed by Dr Christopher Gerteis, SOAS University of London.

The archive links to listings on Sketchfab, Fab, CGTrader and the Unity Asset Store. It never copies or redistributes model files.

## How the site works

The site is static HTML served by GitHub Pages, with Bootstrap 5 for layout. There is no build step.

| Path | What it is |
|---|---|
| `catalog/fab.yml` | **The catalog.** One entry per listing, schema v2. |
| `catalog/schema.json` | JSON Schema for an entry; the controlled vocabularies live here. |
| `catalog/quarantine.yml` | Entries withheld from the catalog, each with the reason and its original record. |
| `assets/catalog.js` | Renders the catalog for both `catalog.html` and `ja/catalog.html`. |
| `scripts/validate_catalog.py` | Validates the catalog against the schema and cross-entry rules. |
| `scripts/check_links.py` | Confirms every listing still exists (Sketchfab via its API). |
| `scripts/scrape_sketchfab.py` | Drafts new entries from Sketchfab URLs, built from the listing itself. |
| `ethics.html` | AI & Ethics statement. |
| `ja/` | Japanese pages, mirroring the English ones. |

## Adding an entry

Entries enter `fab.yml` only after the listing has been checked. For Sketchfab:

1. Put the model URLs in `catalog/sketchfab_urls.txt`, one per line.
2. Run `python scripts/scrape_sketchfab.py`. Drafts appear in `outputs/new_entries.yml` (git-ignored), with title, creator, licence, thumbnail and polygon count taken from the Sketchfab API.
3. Give each draft a free id, complete `period_tags`, `object_tags`, `space_tags` and `historical_notes`, delete the `_listing_description` helper field, and paste the entry into `catalog/fab.yml`.
4. Run `python scripts/validate_catalog.py`.

For Fab, CGTrader and Unity listings, copy the fields from the listing page by hand and set `verification.method: manual`.

A minimal entry:

```yaml
- id: skf-0059
  title: Black Wall Telephone            # as on the listing
  source: sketchfab                      # sketchfab | fab | cgtrader | unity_asset_store
  source_url: "https://sketchfab.com/3d-models/black-wall-telephone-32ca0931052e40e192f59df81779fcef"
  creator: GiyoP                         # as on the listing
  licence: CC BY 4.0                     # as on the listing
  period_tags: [high_growth_1952_1973]
  object_tags: [technology, communication]
  historical_notes: "..."
  showa_fit: unassessed                  # set by the curator only
  verification:
    status: verified
    method: sketchfab-api
    checked: "2026-11-01"
```

Period tags: `interwar_wartime_1926_1945`, `occupation_reconstruction_1945_1952`, `high_growth_1952_1973`, `late_showa_1973_1989`, `unassigned`. New values go through the project director.

## Checks

`.github/workflows/catalog.yml` validates the catalog on every push and pull request, and runs the link check every Monday. A failed link check opens or updates an issue titled "Catalog link check: listings gone or changed". Fab and CGTrader answer automated requests with a bot challenge, so those listings are reported as unconfirmed and need an occasional check by hand.

## Testing locally

```bash
python3 -m http.server 8000
# open http://localhost:8000/catalog.html
```

The catalog page fetches `catalog/fab.yml`, so it needs a local server; opening the file directly will not load the data.

## Licences

Code: MIT (`LICENSE`). Text and project-authored metadata: CC BY 4.0 (`LICENSE-CONTENT.md`). Listed models remain their creators' and carry the licence each listing states.

## History

See `CHANGELOG.md`. The audit of 1 November 2026 rebuilt the catalog from its listings; the AI & Ethics page explains why.
