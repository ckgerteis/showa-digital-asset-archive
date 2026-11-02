# Changelog

## 2026-11-02: Japanese marketplaces, institutional open data and 273 new entries

- The catalog now accepts three further sources: BOOTH (`booth`, ids `booth-`), ニコニ立体 / Niconi 3D (`niconi_3d`, `nico-`) and institutional open-data portals (`open_data`, `od-`). Schema, validator, link checker, the platform filter and both Submit pages are updated.
- 273 entries added (catalog now 452), all found through Japanese-language searches and admitted where the model can be downloaded and its stated terms allow use in world or game building, or restrict it, as recorded: 243 BOOTH items (10 with restricted terms, mostly non-commercial), one ニコニ立体 work, 28 Sketchfab models from municipal, museum and individual accounts, and Nakano Sunplaza's 3D data on Tokyo's open-data catalogue. About 500 further BOOTH items whose pages state no terms are held back until their terms can be read.
- One entry per listing: a pack sold as one item is one entry, with the number of objects in `technical.items`. Seller's terms are recorded in `licence` in the listing's own words.
- New field `ai_statement` quotes what a listing says about AI use in making the model, as the AI & Ethics statement requires; the card shows it and a new filter selects it. Twenty listings carry one.
- Historical fit applied under the adopted rule: the marketplace items are proxies, with the listing's period wording quoted in the grounds; 15 institutional and individual scans are documented. Six BOOTH items give only a decade, not 昭和, and are admitted as proxies at the director's ruling.

## 2026-11-01: historical fit for every entry

- The director adopted a rule for `showa_fit` (now in the README) and assessed skf-0059 to skf-0170 under it: 89 documented, 22 proxy, 1 anachronistic. A new field, `fit_grounds`, records the reasons for each, and the catalog card shows them beside the fit.
- Proxies are mainly spaces still in use (the Asakusa underground arcade, Suehirochō passage, Jinbōchō station, Omoide Yokochō, a Hotel New Akao room), air-raid exhibits whose listings name no holder, reconstructions (Gunkanjima, the Kenmeri Skyline), and objects dated only approximately or by type. The Hijimayama landslide memorial is anachronistic: its inscription says it was rebuilt some thirty years after the 1972 disaster.
- The nine pieces of military hardware stay in the catalog at the director's ruling.
- The 67 earlier entries are assessed under the same rule: 66 proxy and 1 anachronistic. All are modelled assets rather than records of surviving originals. Twenty-four have no tie to Japan in their listings: seven place the object elsewhere (a Zenith console, G-Plan tables, a French coal wagon and mine gallery, a German rock drill, a Goldfinger-set ashtray, a shelf tagged Chinese and Korean) and seventeen are generic. They stay in the catalog as proxies at the director's ruling, and their grounds say so. Nimikko's Conveyor Belt Sushi Restaurant is anachronistic: its listing describes a present-day restaurant with tablet ordering. The seven review notes on these entries, from the audit, are resolved by the grounds and removed.
- The historical notes on those 24 entries now give both texts: the original catalog note, labelled as such, followed by what the listing describes. Four original notes that the audit had replaced (skf-0011, 0013, 0015, 0039) are restored in this form.
- Every entry now carries a historical fit: 89 documented, 88 proxy, 2 anachronistic. Two review notes remain open.
- Review notes: 17 of 19 resolved and removed. Three Iizuka licence notes were wrong (the catalog already recorded CC BY-NC 4.0); the two horse-Kannon listings give different dimensions and the two Asakusa arcade scans are separate listings, so both pairs stay. Jinbōchō's historical note now gives the Mita Line station's opening as 30 June 1972, not the listing's 1969. Two notes stay open: Gunkanjima (comparison with the Hashima XR Project record) and the surrender rescript (original or facsimile).

## 2026-11-01: an image for every entry

- Every one of the 179 entries now carries an image from its own listing, hotlinked from the platform's image server. The 37 Fab, CGTrader and Unity entries that had none now show the listing's preview image: Fab's from its listing data (640 px), CGTrader's and Unity's from the page's `og:image`. Fab and CGTrader refuse automated requests, so those listings were read in a browser; the Unity listings were read directly. All 179 image addresses answered 200 on 1 Nov 2026.
- The same reading filled in what the listings show. Fab: seller links for all 22, and the licence (Fab Standard License, Personal and Professional tiers) where the catalog had "Not displayed on listing". CGTrader: the designer for the six entries that had "Not confirmed", the licence (Royalty Free, no AI training) for all nine, and the current titles of cgt-0006 and cgt-0007, which their sellers have renamed. Verification dates and methods are updated for all 37.
- The seven probable entries stay probable: their doubt is whether each listing is the product the v1 catalog meant, which reading the listing does not settle.

## 2026-11-01: 112 new Sketchfab entries

- `catalog/fab.yml` grows from 67 to 179 entries (skf-0059 to skf-0170), drawn from a search of Sketchfab and of the full model lists of 24 accounts. Each entry's listing dates the object to 1926–1989: the Osaka Museum of History's Time Capsule EXPO'70 objects, Edo-Tokyo Museum home-front objects, Tōbunken's scans of the Chiran and Aoto airfields, the Sakata clinic in Kumagaya (1931), traces of the Tokyo air raids, steam locomotives, culverts and rail remains, and postwar shopping arcades.
- Title, creator, licence, thumbnail and polygon counts come from the Sketchfab API; each card shows the listing's own thumbnail. Historical notes state only what the listing says. `showa_fit` is `unassessed` throughout.
- Review notes mark 19 entries for the director: nine pieces of military hardware admitted for a ruling (seven Ki-84 Hayate components, the Shiden-kai propeller, the destroyer Sawakaze turbine); three Iizuka listings whose descriptions state CC BY-NC while the platform's licence field differs; two pairs that look like second scans of one object (Asakusa arcade, the coal-mine horse Kannon); and single questions on the Hashima, Jinbōchō, box-pillow, Kenmeri and surrender-rescript listings.
- `scripts/validate_catalog.py` now accepts Sketchfab URLs of the form `/3d-models/<uid>`, which Sketchfab uses for models with non-Latin titles.

## 2026-11-01: menu and citation

- Acknowledgments (謝辞) added to the top menu of every page, after About the Creator. Menu links are set a little tighter at 1200 px and above so all items fit on one line.
- Every page footer (EN/JA) now carries the suggested citation: Gerteis, Christopher. 2025–. *Shōwa Digital Asset Archive*. SOAS University of London. https://showa-digital-archive.org/.

## 2026-11-01: About the Creator

- New page `creator.html` / `ja/creator.html` on Dr Christopher Gerteis's work in critical heritage, digital heritage and computational humanities, with links to the Hashima XR Project, Simulating Silence, his articles in the *Bulletin of the Institute of Oriental Culture* (2024) and *History* (2026), *Past Meets Pixel* and bibliograph-mcp. Added to the top menu of every page.
- The top menu now collapses to the menu button below 1200 px, since the extra item made labels wrap at laptop widths.

## 2026-11-01: Shōwa artefacts in video games

- Home page (EN/JA): new subsection on Shōwa artefacts in video games (*Shenmue*, *Yakuza 0*, *Boku no Natsuyasumi*, *Paranormasight*), placed after the opening paragraph of About the Archive; the nostalgia paragraphs follow under their own heading, and the duplicate game sentence in the closing paragraph is cut. The project credit line is removed at the director's instruction.

## 2026-11-01: About the Archive rewritten

- Home page (EN/JA): the About section now describes the archive as a collaborative hub and sets it in the Shōwa retro boom in Japan and the global city pop revival, and explains why the period draws world builders and game designers and how the archive supports teaching history alongside game and virtual-world design. Sources: SHIBUYA109 lab. (SoftBank News, 21 Feb 2024); Travel Watch (13 Apr 2021) and TV Tokyo (28 May 2021) on Seibuen Yūenchi; Tokyo Weekender (21 Jul 2026) on Spotify streams.

## 2026-11-01: provenance of the catalog stated

- AI & Ethics statement (EN/JA) corrected at the project director's instruction: the December 2025 catalog was adapted from the work of Katherine Strachan and Adam Kay (linked to their public profiles), and has been maintained with Anthropic's Claude tools since then. It replaces the earlier sentence that the first version was compiled with AI tools.

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
