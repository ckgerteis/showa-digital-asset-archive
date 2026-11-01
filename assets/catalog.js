/* Shōwa Digital Asset Archive: catalog renderer shared by catalog.html and ja/catalog.html.
 * Reads catalog/fab.yml (schema v2) and renders filterable cards. All catalog text is escaped
 * before it reaches the DOM, so a submitted entry cannot inject markup.
 * The page sets window.CATALOG_CONFIG = { yamlPath, lang } before loading this file.
 */
(function () {
  "use strict";
  const cfg = window.CATALOG_CONFIG || { yamlPath: "catalog/fab.yml", lang: "en" };
  const JA = cfg.lang === "ja";

  const T = JA ? {
    periods: {
      interwar_wartime_1926_1945: "戦間期・戦時期（1926–45）",
      occupation_reconstruction_1945_1952: "占領・復興期（1945–52）",
      high_growth_1952_1973: "高度成長期（1952–73）",
      late_showa_1973_1989: "昭和後期（1973–89）",
      unassigned: "時期未定"
    },
    sources: { sketchfab: "Sketchfab", fab: "Fab", cgtrader: "CGTrader", unity_asset_store: "Unity Asset Store" },
    view: "掲載ページを開く", details: "詳細", noAssets: "条件に該当するアセットはありません。",
    error: "カタログを読み込めませんでした", of: "件中", shown: "件を表示",
    licence: "ライセンス（掲載ページ記載）", creator: "制作者", checked: "確認日", probable: "照合：推定",
    probableHelp: "掲載ページのタイトルが移行時に変更されているため、同一性は推定です。",
    review: "要検討", fitLabel: "時代適合性", technical: "技術情報", faces: "ポリゴン数", downloadable: "ダウンロード可",
    yes: "可", no: "不可", formats: "形式", price: "価格", notesLang: "（解説は英語）",
    fit: { unassessed: "未評価", documented: "確認済み", proxy: "代替資料", anachronistic: "時代不適合" },
    licenceClass: { open: "オープン（CC）", commercial: "商用ライセンス", viewonly: "閲覧のみ", unknown: "記載なし" }
  } : {
    periods: {
      interwar_wartime_1926_1945: "Interwar and wartime (1926–45)",
      occupation_reconstruction_1945_1952: "Occupation and reconstruction (1945–52)",
      high_growth_1952_1973: "High growth (1952–73)",
      late_showa_1973_1989: "Late Shōwa (1973–89)",
      unassigned: "Period unassigned"
    },
    sources: { sketchfab: "Sketchfab", fab: "Fab", cgtrader: "CGTrader", unity_asset_store: "Unity Asset Store" },
    view: "Open listing", details: "Details", noAssets: "No assets match these filters.",
    error: "The catalog could not be loaded", of: "of", shown: "shown",
    licence: "Licence (as listed)", creator: "Creator", checked: "Listing checked", probable: "Match probable",
    probableHelp: "The listing was retitled when it moved platforms; the match rests on seller and description.",
    review: "Under review", fitLabel: "Historical fit", technical: "Technical", faces: "Faces", downloadable: "Downloadable",
    yes: "yes", no: "no", formats: "Formats", price: "Price", notesLang: "",
    fit: { unassessed: "not yet assessed", documented: "documented", proxy: "proxy object", anachronistic: "anachronistic" },
    licenceClass: { open: "Open (Creative Commons)", commercial: "Commercial licence", viewonly: "View only", unknown: "Not stated" }
  };

  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = (u) => (/^https:\/\//.test(u || "") ? u : "#");

  function licenceClass(l) {
    if (!l) return "unknown";
    if (/^CC/.test(l)) return "open";
    if (/view only/i.test(l)) return "viewonly";
    if (/not displayed|unconfirmed/i.test(l)) return "unknown";
    return "commercial";
  }

  let data = [];
  const $ = (id) => document.getElementById(id);

  function fillSelect(id, values, labelFn) {
    const sel = $(id);
    values.forEach((v) => {
      const o = document.createElement("option");
      o.value = v; o.textContent = labelFn ? labelFn(v) : v;
      sel.appendChild(o);
    });
  }

  function card(e, idx) {
    const periods = (e.period_tags || []).map((p) =>
      `<span class="badge text-bg-light border me-1 mb-1">${esc(T.periods[p] || p)}</span>`).join("");
    const lc = licenceClass(e.licence);
    const img = e.image
      ? `<img src="${esc(safeUrl(e.image))}" alt="${esc(e.title)}" loading="lazy">`
      : `<div class="no-image">${esc(T.sources[e.source] || e.source)}</div>`;
    const flags = [];
    if (e.verification && e.verification.status === "probable")
      flags.push(`<span class="badge text-bg-warning" title="${esc(T.probableHelp)}">${esc(T.probable)}</span>`);
    if (e.review_note) flags.push(`<span class="badge text-bg-danger">${esc(T.review)}</span>`);
    const tech = e.technical || {};
    const techRows = [
      tech.faces != null ? `${esc(T.faces)}: ${Number(tech.faces).toLocaleString()}` : "",
      tech.downloadable != null ? `${esc(T.downloadable)}: ${tech.downloadable ? T.yes : T.no}` : "",
      tech.formats ? `${esc(T.formats)}: ${esc(tech.formats)}` : "",
      tech.price ? `${esc(T.price)}: ${esc(tech.price)}` : ""
    ].filter(Boolean).join(" · ");
    const v = e.verification || {};
    return `
      <div class="col-md-6 col-lg-4 mb-4">
        <article class="card h-100 shadow-sm asset-card">
          <div class="img-container">${img}
            <span class="badge bg-dark badge-source">${esc(T.sources[e.source] || e.source)}</span>
          </div>
          <div class="card-body">
            <div class="mb-2">${flags.join(" ")}</div>
            <h3 class="h6 card-title mb-1">${esc(e.title)}</h3>
            ${e.title_ja ? `<p class="small mb-1" lang="ja">${esc(e.title_ja)}</p>` : ""}
            <p class="creator-text mb-2"><i class="bi bi-person-circle" aria-hidden="true"></i>
              ${e.creator_url ? `<a href="${esc(safeUrl(e.creator_url))}" target="_blank" rel="noopener">${esc(e.creator)}</a>` : esc(e.creator)}</p>
            <div class="mb-2">${periods}</div>
            <p class="small mb-2"><span class="licence-dot lic-${lc}"></span>${esc(e.licence)}</p>
            <details class="small">
              <summary>${esc(T.details)}</summary>
              ${e.historical_notes ? `<p class="mt-2 mb-1" lang="en">${esc(e.historical_notes)} ${esc(T.notesLang)}</p>` : ""}
              ${e.review_note ? `<p class="mb-1 text-danger" lang="en"><strong>${esc(T.review)}:</strong> ${esc(e.review_note)}</p>` : ""}
              <p class="mb-1">${esc(T.fitLabel)}: ${esc(T.fit[e.showa_fit] || e.showa_fit)}${e.fit_grounds ? ` <span class="text-muted" lang="en">(${esc(e.fit_grounds)})</span>` : ""}</p>
              ${techRows ? `<p class="mb-1">${esc(T.technical)}: ${techRows}</p>` : ""}
              <p class="mb-0 text-muted">${esc(T.checked)}: ${esc(v.checked)} (${esc(v.method)}) · ${esc(e.id)}</p>
            </details>
          </div>
          <div class="card-footer bg-white border-top-0 pt-0 pb-3">
            <a href="${esc(safeUrl(e.source_url))}" target="_blank" rel="noopener" class="btn btn-outline-dark btn-sm w-100">
              ${esc(T.view)} <i class="bi bi-box-arrow-up-right" aria-hidden="true"></i></a>
          </div>
        </article>
      </div>`;
  }

  function apply() {
    const term = $("searchInput").value.trim().toLowerCase();
    const period = $("periodFilter").value, obj = $("objectFilter").value, space = $("spaceFilter").value;
    const src = $("sourceFilter").value, lic = $("licenceFilter").value;
    const rows = data.filter((e) => {
      if (period && !(e.period_tags || []).includes(period)) return false;
      if (obj && !(e.object_tags || []).includes(obj)) return false;
      if (space && !(e.space_tags || []).includes(space)) return false;
      if (src && e.source !== src) return false;
      if (lic && licenceClass(e.licence) !== lic) return false;
      if (!term) return true;
      return [e.title, e.title_ja, e.creator, e.historical_notes, (e.object_tags || []).join(" "), (e.space_tags || []).join(" ")]
        .join(" ").toLowerCase().includes(term);
    });
    $("count").textContent = JA ? `${data.length}${T.of}${rows.length}${T.shown}` : `${rows.length} ${T.of} ${data.length} ${T.shown}`;
    $("catalogGrid").innerHTML = rows.length ? rows.map(card).join("")
      : `<div class="col-12 text-center p-5">${esc(T.noAssets)}</div>`;
  }

  document.addEventListener("DOMContentLoaded", () => {
    fetch(cfg.yamlPath)
      .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.text(); })
      .then((text) => {
        data = jsyaml.load(text.replace(/^\uFEFF/, "")) || [];
        const uniq = (f) => [...new Set(data.flatMap(f))].sort();
        fillSelect("periodFilter", Object.keys(T.periods).filter((p) => data.some((e) => (e.period_tags || []).includes(p))), (p) => T.periods[p]);
        fillSelect("objectFilter", uniq((e) => e.object_tags || []), (t) => t.replace(/_/g, " "));
        fillSelect("spaceFilter", uniq((e) => e.space_tags || []), (t) => t.replace(/_/g, " "));
        fillSelect("sourceFilter", Object.keys(T.sources).filter((s) => data.some((e) => e.source === s)), (s) => T.sources[s]);
        fillSelect("licenceFilter", Object.keys(T.licenceClass), (c) => T.licenceClass[c]);
        ["searchInput", "periodFilter", "objectFilter", "spaceFilter", "sourceFilter", "licenceFilter"].forEach((id) =>
          $(id).addEventListener(id === "searchInput" ? "input" : "change", apply));
        apply();
      })
      .catch((err) => {
        $("catalogGrid").innerHTML = `<div class="alert alert-danger">${esc(T.error)}: ${esc(err.message)}</div>`;
      });
  });
})();
