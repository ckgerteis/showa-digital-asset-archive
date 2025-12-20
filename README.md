# Showa Digital Asset Archive

**Preserving the Material Heritage of Modern Japan (1926-1989)**

This repository hosts the source code and data for the [Showa Digital Asset Archive](https://ckgerteis.github.io/showa-digital-asset-archive/). The site is a static generated site hosted on GitHub Pages, utilizing Bootstrap 5 for layout and Client-Side JavaScript to render the catalog.

## 📂 Project Structure

- **`index.html`**: The landing page with mission statement and navigation.
- **`catalog.html`**: The dynamic gallery. It reads data from `catalog/fab.yml`.
- **`submit.html`**: Embeds the Google Form for community submissions.
- **`educators.html`**: Resources, pedagogy, and citation guidelines.
- **`catalog/fab.yml`**: **THE DATABASE.** This YAML file contains all asset metadata.

---

## 🛠 How to Add New Assets

You do not need to edit HTML code to add items. Simply update the YAML database.

1. Open `catalog/fab.yml`.
2. Add a new entry following this exact format:

```yaml
- id: skf-0026
  title: "Your Asset Title"
  source: "sketchfab"
  source_url: "[https://sketchfab.com/](https://sketchfab.com/)..."
  creator: "Creator Name"
  period_tags: ["high_growth_1952_1973"]
  object_tags: ["category_name"]
  historical_notes: "Description of why this matters..."
  image: "[https://link-to-thumbnail.jpg](https://link-to-thumbnail.jpg)"  # Optional but recommended
