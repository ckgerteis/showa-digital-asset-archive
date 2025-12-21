# Showa Digital Asset Archive - AI Agent Instructions

## Project Overview
This is a **static GitHub Pages site** serving as a curated link archive for 3D digital assets of Japanese Showa Era (1926-1989) material culture. It does NOT host binaries—only metadata and links to external platforms (Sketchfab, Fab, CGTrader, Unity Asset Store).

## Architecture

### Critical: YAML-Driven Static Site
- **Single Source of Truth**: [catalog/fab.yml](catalog/fab.yml) is the entire database
- HTML files are **static templates** that read `catalog/fab.yml` client-side via `js-yaml`
- No backend, no build process—direct HTML/CSS/JS served by GitHub Pages
- Deployment: Push to `main` branch automatically deploys to `https://ckgerteis.github.io/showa-digital-asset-archive/`

### Bilingual Structure
- **English**: Root HTML files (`index.html`, `catalog.html`, etc.)
- **Japanese**: Mirrored in `ja/` directory (`ja/index.html`, `ja/catalog.html`, etc.)
- Both versions **read the same YAML file** (`catalog/fab.yml`) but render UI text differently
- Use `hreflang` tags for SEO (see existing HTML `<head>` sections)

### Data Schema ([catalog/fab.yml](catalog/fab.yml))
```yaml
- id: skf-0001                      # Unique ID (prefix: skf=Sketchfab, fab=Fab, cgt=CGTrader, uas=Unity)
  title: "Asset Name"
  source: "sketchfab"               # One of: sketchfab, unreal_marketplace, cgtrader, unity_asset_store
  source_url: "https://..."
  creator: "Creator Name"
  period_tags:                      # Must use exact values below (at least one required)
    - "high_growth_1952_1973"       # Options: interwar_wartime_1926_1945, occupation_reconstruction_1945_1952, 
                                    #          high_growth_1952_1973, bubble_era_1973_1989
  object_tags: ["technology", "camera"]  # Freeform, but be consistent with existing tags
  space_tags: ["home", "studio"]         # Optional. Common values: home, public, commercial, education
                                         # Specific rooms: kitchen, living_room, bedroom, studio, bath, interior
  historical_notes: "Why this asset matters historically"
  image: "https://..."              # Optional thumbnail URL
```

## Key Workflows

### Adding New Assets (PRIMARY TASK)
1. **Never edit HTML directly** for content changes
2. Open [catalog/fab.yml](catalog/fab.yml) and append new entry using exact schema above
3. Use [templates/new-entry.md](templates/new-entry.md) as a checklist for metadata collection
4. **ID naming**: Increment from last entry with same prefix (e.g., `skf-0058` → `skf-0059`)
5. **Period tags**: Must exactly match one of the four historical periods
6. Test locally by opening `catalog.html` in browser (uses CORS-free local file:// protocol)

### Scraping Sketchfab Metadata
Script: [scripts/scrape_sketchfab.py](scripts/scrape_sketchfab.py) - automated metadata collection from Sketchfab URLs

**Usage:**
```bash
# 1. Add Sketchfab URLs to the input file (one per line)
echo "https://sketchfab.com/3d-models/..." >> catalog/sketchfab_urls.txt

# 2. (Optional but recommended) Set API token for better data quality
export SKETCHFAB_TOKEN="your_token_here"

# 3. Run the scraper
python3 scripts/scrape_sketchfab.py
```

**Output:**
- `outputs/sketchfab_metadata.json` - Full API response with all fields
- `outputs/sketchfab_metadata.csv` - Tabular format for spreadsheet review
- Fields extracted: title, creator, license, download status, poly count, formats, thumbnails

**Workflow:**
1. Scraper hits Sketchfab API (if `SKETCHFAB_TOKEN` set) or falls back to HTML scraping
2. Review output files to verify metadata quality
3. Manually add curated entries to [catalog/fab.yml](catalog/fab.yml) with proper period/object tags
4. `outputs/` directory is git-ignored (scratch space only)

### Common Edits
- **Styling changes**: Inline `<style>` blocks in each HTML file (no separate CSS file except [style.css](style.css) for shared rules)
- **Navigation updates**: Must update in **all 10 HTML files** (5 English + 5 Japanese)
- **Catalog filtering logic**: JavaScript at bottom of [catalog.html](catalog.html) and [ja/catalog.html](ja/catalog.html)

## Conventions & Patterns

### Bootstrap + Vanilla JS
- Bootstrap 5.3 for layout (via CDN)
- No jQuery, React, or build tools
- Client-side YAML parsing via `js-yaml` CDN library
- Catalog cards rendered dynamically with `renderGrid()` function

### Image Loading Pattern
```javascript
// Lazy loading with blur-to-sharp transition
<img class="img-loading" onload="this.classList.remove('img-loading'); this.classList.add('img-loaded')">
```

### Source-Specific UI Logic
Each `source` value triggers different button styles and badges (see [catalog.html:150-180](catalog.html#L150-L180)):
- `sketchfab` → Blue "View on Sketchfab" button
- `unreal_marketplace` → Dark "View on Fab.com" button
- `cgtrader` → Green "View on CGTrader" button
- `unity_asset_store` → Gray "View on Unity Store" button

### Historical Period Display Names
Map YAML tags to UI labels (all four periods are valid, though "bubble_era_1973_1989" is rarely used currently):
```javascript
"interwar_wartime_1926_1945" → "Interwar (1926-45)"
"occupation_reconstruction_1945_1952" → "Occupation (1945-52)"
"high_growth_1952_1973" → "High Growth (1952-73)"
"bubble_era_1973_1989" → "Bubble Era (1973-89)"
```

**Note**: Most assets in the current catalog use `high_growth_1952_1973` as this was the peak of Japanese industrial design innovation.

## Critical Don'ts
- ❌ Don't add binary files (3D models, textures) to repo
- ❌ Don't create a database/backend—this is intentionally static
- ❌ Don't use Node.js build tools or preprocessors
- ❌ Don't edit English HTML without updating Japanese mirror
- ❌ Don't create new period_tag values without coordinating with project lead

## Testing Locally
```bash
# Serve locally (Python 3)
python3 -m http.server 8000
# Open http://localhost:8000/catalog.html
```

Or just open HTML files directly—no server needed for basic functionality.
