# Changelog

## 2026-11-01: AI & Ethics statement adopted

- The AI & Ethics statement (`ethics.html`, `ja/ethics.html`) is adopted by the project director as published; the draft label is removed.

## 2026-11-01: custom domain

- The archive moves to https://showa-digital-archive.org/, registered through Netlify with DNS on Netlify (apex A and AAAA records to GitHub Pages, `www` as a CNAME to ckgerteis.github.io). GitHub Pages still serves the site; the old ckgerteis.github.io address redirects to the new one.
- `CNAME` added; every absolute link, the citation on the Research & Education page, the README and `LICENSE-CONTENT.md` now give the new address.

## 2026-11-01: audit and schema v2

An audit of the catalog on 1 November 2026 checked every listing. Of 54 Sketchfab entries, 23 resolved through the Sketchfab API and 31 did not (30 returned 404; one carried a malformed 28-character UID). The 49 Fab, CGTrader and Unity entries were resolved by web search, since those platforms refuse automated requests.

### Catalog data

- `catalog/fab.yml` rebuilt to schema v2 (`catalog/schema.json`): 67 entries, 60 verified and 7 probable. Title, creator, licence, thumbnail and polygon counts now come from each listing; every entry records the date and method of its check.
- Seven Sketchfab entries whose URLs carried corrupted UIDs were restored to the model with the same title and creator found by API search (skf-0014, 0019, 0020, 0028, 0033, 0044, 0046).
- 36 entries moved to `catalog/quarantine.yml` with their original records and the reason: 23 Sketchfab models not found, one duplicate (skf-0049 of skf-0033), seven Fab or CGTrader listings not found, and five where a similar listing exists but the title or seller differs.
- 22 Unreal Marketplace entries moved to their current Fab listing URLs; CGTrader category paths and Unity hosts normalised.
- Creator "Generic" replaced by the creator named on the listing in every entry.
- Seven entries carry review notes: six where the listing contradicts the v1 framing (skf-0010, 0011, 0013, 0015, 0018, 0039), and skf-0038, whose v1 period tag lay outside the vocabulary. Four historical notes the listings contradicted were replaced with what the listing states.
- Period vocabulary fixed: `bubble_era_1973_1989` renamed `late_showa_1973_1989`; `unassigned` added; the stray values `industrial_era` and `edo_1603_1868` replaced by `unassigned`.
- `historical_notes`, `showa_fit` (all `unassessed`), `review_note`, `technical` and `verification` fields added.

### Checks

- `scripts/validate_catalog.py` and `.github/workflows/catalog.yml`: schema validation on every push and pull request; a weekly link check that opens an issue when a listing is gone or changed.
- `scripts/check_links.py`: Sketchfab checked through the API for existence, title and creator.
- `scripts/scrape_sketchfab.py` rewritten to draft schema-v2 entries from the API.

### Site

- Catalog page rebuilt on a shared renderer (`assets/catalog.js`) for English and Japanese: filters for period, object type, space, platform and licence; licence, period badges, review notes and verification date on each card; all text escaped; thumbnails from the catalog instead of a third-party CORS proxy; mobile navigation toggle added.
- Lesson-plan asset links rebuilt from the catalog. Four dead references were replaced by verified listings of the same object type (skf-0035 by fab-0029, skf-0058 by cgt-0004, skf-0052 by fab-0027, skf-0055 by fab-0028); three were marked withdrawn (skf-0003, 0004, 0005).
- "Digital Shōwa Landscape" section verified claim by claim against sources and corrected, with sources added (Hiroshima VR producer and format, 1964 TOKYO VR dates and sponsors, Virtual Kyoto aerial photographs, Matsudo production method, Virtual Market details, Showa American Story status). RealityScan corrected to Epic Games; 1925 corrected to 1926.
- Reading lists converted to Chicago 18 author–date and corrected: Yoshimi 1992 is *Hakurankai no seijigaku* (Chūō Kōronsha); Gordon 2003 was published in New York.
- New AI & Ethics page (`ethics.html`, `ja/ethics.html`), draft for the director's review.
- Submission guidance aligned with the catalog: listings under any licence, licence recorded as stated.
- Shōwa with macron in running text; "Dr" without a full stop; SRI hashes on CDN assets; absolute hreflang links on Japanese pages; footer contact link fixed.
- Unused `style.css` removed.

### Repository

- `LICENSE` completed (the MIT text was truncated) and given a copyright holder; `LICENSE-CONTENT.md` added for CC BY 4.0 text and metadata.
- README, CONTRIBUTING, the entry template and the Copilot instructions rewritten for schema v2.
- Line endings normalised to LF (`.gitattributes`); byte-order marks removed.
