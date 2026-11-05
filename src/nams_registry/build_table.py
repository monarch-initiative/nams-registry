"""Build the resource table page from resources/*.yaml.

The page lists one row per resource. Clicking a row shows the rest of the
resource's details below it. The data is embedded in the page, so it needs
no server. `just gen-doc` runs this and MkDocs publishes the page as part
of the documentation site.

To change the columns in each row, edit COLUMNS below.
"""

import argparse
import glob
import json
import os

import yaml

REPOSITORY = "https://github.com/monarch-initiative/nams-registry"

# The columns shown in each row, as (field, column heading, display).
# Display is one of:
#   text      the value, or tags for a field holding a list
#   clamp     text cut to two lines; the full text is in the details
#   check     a check mark when the value is true
#   discuss   a link to the resource's GitHub issues
# Everything else stays in the details that open below the row.
COLUMNS = [
    ("name", "Name", "text"),
    ("nams_relevance", "NAMs relevance", "text"),
    ("dismech_integration", "DisMech integration", "clamp"),
    ("is_tox", "is_tox", "check"),
    ("id", "Discussion", "discuss"),
]


def derived_fields(resource):
    """Fields computed for the table, not stored in the resource files."""
    return {"is_tox": "toxicology" in (resource.get("domain_areas") or [])}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NAMs Registry</title>
<style>
  :root {
    --bg: #ffffff; --fg: #1d2430; --muted: #5b6575; --line: #e3e7ee;
    --row-hover: #f6f8fb; --detail-bg: #f9fafc; --accent: #2f5fb3;
    --chip-bg: #eef2f8;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14171c; --fg: #e6e9ef; --muted: #9aa3b2; --line: #2a303a;
      --row-hover: #1b2028; --detail-bg: #181c23; --accent: #8fb3ff;
      --chip-bg: #232a35;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px 16px 48px; background: var(--bg); color: var(--fg);
    font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }
  main { max-width: 1100px; margin: 0 auto; }
  h1 { font-size: 22px; margin: 0 0 4px; }
  .subtitle { color: var(--muted); margin: 0 0 20px; }
  .controls { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; }
  .controls input, .controls select {
    font: inherit; color: inherit; background: var(--bg);
    border: 1px solid var(--line); border-radius: 6px; padding: 7px 10px;
  }
  .controls input { flex: 1 1 260px; }
  .count { color: var(--muted); font-size: 13px; margin: 0 0 8px; }
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; }
  th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-size: 13px; color: var(--muted); font-weight: 600; white-space: nowrap; }
  tr.summary { cursor: pointer; }
  tr.summary:hover { background: var(--row-hover); }
  .toggle {
    font: inherit; background: none; border: 0; color: var(--muted); cursor: pointer;
    width: 24px; padding: 0; line-height: 1;
  }
  .toggle[aria-expanded="true"] .chev { transform: rotate(90deg); }
  .chev { display: inline-block; transition: transform .12s; }
  .name { font-weight: 600; }
  .col-check { text-align: center; }
  .check { font-weight: 700; }
  .clamp {
    display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2;
    overflow: hidden; max-width: 34ch;
  }
  .rid { color: var(--muted); font-size: 13px; }
  tr.detail td { background: var(--detail-bg); padding: 14px 16px 18px 44px; }
  dl { display: grid; grid-template-columns: max-content 1fr; gap: 6px 18px; margin: 0; }
  dt { color: var(--muted); font-size: 13px; }
  dd { margin: 0; }
  .chip {
    display: inline-block; background: var(--chip-bg); border-radius: 4px;
    padding: 1px 7px; margin: 0 4px 4px 0; font-size: 13px;
  }
  a { color: var(--accent); }
  ul.pubs { margin: 0; padding-left: 18px; }
  .none { color: var(--muted); }
  @media (max-width: 600px) {
    tr.detail td { padding-left: 16px; }
    dl { grid-template-columns: 1fr; }
    dt { margin-top: 6px; }
  }
</style>
</head>
<body>
<main>
  <h1>NAMs Registry</h1>
  <p class="subtitle">NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.</p>
  <div class="controls">
    <input id="q" type="search" placeholder="Search names, ids, and descriptions" aria-label="Search">
    <select id="relevance" aria-label="NAMs relevance"><option value="">All NAMs relevance</option></select>
    <select id="type" aria-label="Resource type"><option value="">All resource types</option></select>
  </div>
  <p class="count" id="count"></p>
  <div class="table-wrap">
  <table>
    <thead><tr><th></th>__HEADERS__</tr></thead>
    <tbody id="rows"></tbody>
  </table>
  </div>
</main>
<script>
const DATA = __DATA__;
const COLUMNS = __COLUMNS__;
const REPOSITORY = __REPOSITORY__;

const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const link = u => u ? `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(u)}</a>` : `<span class="none">Not recorded</span>`;
const chips = a => a && a.length ? a.map(x => `<span class="chip">${esc(x)}</span>`).join("") : `<span class="none">Not recorded</span>`;
const text = v => v ? esc(v) : `<span class="none">Not recorded</span>`;

function cell(r, [f, heading, display]) {
  const v = r[f];
  if (f === "name") return `<span class="name">${esc(v)}</span>`;
  if (display === "check") return v ? `<span class="check" role="img" aria-label="Yes">&#10003;</span>` : "";
  if (display === "clamp") return v ? `<span class="clamp">${esc(v)}</span>` : text(v);
  if (display === "discuss") {
    const q = encodeURIComponent(`is:issue "${v}"`);
    return `<a href="${REPOSITORY}/issues?q=${q}" target="_blank" rel="noopener">Discuss</a>`;
  }
  return Array.isArray(v) ? chips(v) : text(v);
}

function pubUrl(id) {
  if (id.startsWith("doi:")) return "https://doi.org/" + id.slice(4);
  if (id.startsWith("PMID:")) return "https://pubmed.ncbi.nlm.nih.gov/" + id.slice(5);
  return id;
}

function detail(r) {
  const pubs = (r.publications || []).map(p =>
    `<li><a href="${esc(pubUrl(p.id))}" target="_blank" rel="noopener">${esc(p.title || p.id)}</a>${p.year ? " (" + esc(p.year) + ")" : ""}</li>`).join("");
  const imp = (r.imported_from || []).map(i =>
    `${esc(i.source)} <a href="${esc(i.source_url)}" target="_blank" rel="noopener">${esc(i.source_id)}</a>, commit ${esc(i.source_version || "?")}, ${esc(i.imported_on)}`).join("<br>");
  return `<dl>
    <dt>Id</dt><dd>${esc(r.id)}</dd>
    <dt>Description</dt><dd>${text(r.description)}</dd>
    <dt>Resource type</dt><dd>${text(r.resource_type)}</dd>
    <dt>Activity status</dt><dd>${text(r.activity_status)}</dd>
    <dt>Domain areas</dt><dd>${chips(r.domain_areas)}</dd>
    <dt>Homepage</dt><dd>${link(r.homepage_url)}</dd>
    ${r.repository ? `<dt>Repository</dt><dd>${link(r.repository)}</dd>` : ""}
    <dt>License</dt><dd>${r.license ? (r.license.id ? `<a href="${esc(r.license.id)}" target="_blank" rel="noopener">${esc(r.license.label)}</a>` : esc(r.license.label)) : text("")}</dd>
    <dt>Curation model</dt><dd>${chips(r.curation_model)}</dd>
    ${r.relevance_note ? `<dt>Relevance note</dt><dd>${esc(r.relevance_note)}</dd>` : ""}
    ${r.dismech_integration ? `<dt>DisMech integration</dt><dd>${esc(r.dismech_integration)}</dd>` : ""}
    <dt>Publications</dt><dd>${pubs ? `<ul class="pubs">${pubs}</ul>` : text("")}</dd>
    <dt>Imported from</dt><dd>${imp || text("")}</dd>
  </dl>`;
}

function fillSelect(el, key) {
  [...new Set(DATA.map(r => r[key]).filter(Boolean))].sort().forEach(v => {
    const n = DATA.filter(r => r[key] === v).length;
    el.insertAdjacentHTML("beforeend", `<option value="${esc(v)}">${esc(v)} (${n})</option>`);
  });
}

const q = document.getElementById("q"), rel = document.getElementById("relevance"), typ = document.getElementById("type");
fillSelect(rel, "nams_relevance");
fillSelect(typ, "resource_type");

function render() {
  const term = q.value.trim().toLowerCase();
  const shown = DATA.filter(r =>
    (!rel.value || r.nams_relevance === rel.value) &&
    (!typ.value || r.resource_type === typ.value) &&
    (!term || [r.id, r.name, r.description].some(v => (v || "").toLowerCase().includes(term))));
  document.getElementById("count").textContent = `${shown.length} of ${DATA.length} resources`;
  document.getElementById("rows").innerHTML = shown.map((r, i) => `
    <tr class="summary" data-i="${i}">
      <td><button class="toggle" aria-expanded="false" aria-controls="d${i}" aria-label="Show details for ${esc(r.name)}"><span class="chev">&#9656;</span></button></td>
      ${COLUMNS.map(c => `<td class="col-${c[2]}">${cell(r, c)}</td>`).join("")}
    </tr>
    <tr class="detail" id="d${i}" hidden><td colspan="${COLUMNS.length + 1}">${detail(r)}</td></tr>`).join("");
}

document.getElementById("rows").addEventListener("click", e => {
  if (e.target.closest("a")) return;
  const row = e.target.closest("tr.summary");
  if (!row) return;
  const btn = row.querySelector(".toggle");
  const d = document.getElementById(btn.getAttribute("aria-controls"));
  const open = btn.getAttribute("aria-expanded") === "true";
  btn.setAttribute("aria-expanded", String(!open));
  d.hidden = open;
});
[q, rel, typ].forEach(el => el.addEventListener("input", render));
render();
</script>
</body>
</html>
"""


def to_json(value):
    """Serialize for embedding in a <script> element."""
    return json.dumps(value, default=str, ensure_ascii=False).replace("</", "<\\/")


def main(argv=None):
    """Build the page."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resources", default="resources", help="Directory of resource files (default: resources)")
    parser.add_argument(
        "--output", default="docs/resources/index.html",
        help="Page to write (default: docs/resources/index.html)",
    )
    args = parser.parse_args(argv)

    rows = []
    for f in sorted(glob.glob(os.path.join(args.resources, "*.yaml"))):
        with open(f) as fh:
            resource = yaml.safe_load(fh)
        rows.append({**resource, **derived_fields(resource)})
    rows.sort(key=lambda r: r["name"].lower())

    headers = "".join(
        f'<th class="col-{display}">{heading}</th>' for _, heading, display in COLUMNS
    )
    page = (
        PAGE.replace("__HEADERS__", headers)
        .replace("__COLUMNS__", to_json(COLUMNS))
        .replace("__REPOSITORY__", to_json(REPOSITORY))
        .replace("__DATA__", to_json(rows))
    )
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as fh:
        fh.write(page)
    print(f"Wrote {len(rows)} resources to {args.output}")


if __name__ == "__main__":
    main()
