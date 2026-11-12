"""Build the registry's browse page from resources/, nams/ and partial-nams/.

The page has four tabs: all records, resources (resources/*.yaml), NAM
records (nams/*.yaml) and partial NAM records
(partial-nams/<resource>/*.yaml). Each tab
lists one row per record; clicking a row shows the rest of the record's
details below it. The data is embedded in the page, so it needs no server.
`just build-table` runs this, as does `just gen-doc`, before MkDocs
publishes the page at /resources/.

To change a tab's columns, edit TABS below.
"""

import argparse
import glob
import json
import os

import yaml

REPOSITORY = "https://github.com/monarch-initiative/nams-registry"

# Each tab as (key, label, kinds, columns). The key is the tab's URL hash,
# e.g. #nams; kinds are the kinds of record it lists. Each column is
# (field, heading, display, filter). Display is one of:
#   text      the value, or tags for a field holding a list
#   clamp     text cut to two lines; the full text is in the details
#   check     a check mark when the value is true
#   badge     the value as a badge
#   issue     the number of the resource's review issue (discussion_issue),
#             linked, or a dash if it has none
# Filter, shown under the column heading, is one of:
#   None      no filter
#   values    choose one of the column's values (for a list, one it holds)
#   present   choose whether the column has a value
# Clicking a column heading sorts by that column, ascending then descending.
# Everything else stays in the details that open below the row.
TABS = [
    ("all", "All records", ["resource", "nam", "partial"], [
        ("name", "Name", "text", None),
        ("kind_label", "Kind", "badge", "values"),
        ("type", "Type or NAMO class", "text", "values"),
        ("sources", "Found in", "text", "values"),
    ]),
    ("resources", "Resources", ["resource"], [
        ("name", "Name", "text", None),
        ("holds_nams", "Holds NAMs", "text", "values"),
        ("priority", "Priority", "text", "values"),
        ("dismech_integration", "DisMech integration", "clamp", "present"),
        ("is_tox", "is_tox", "check", "present"),
        ("discussion_issue", "GH Issue", "issue", "present"),
    ]),
    ("nams", "NAMs", ["nam"], [
        ("name", "Name", "text", None),
        ("type", "NAMO class", "text", "values"),
        ("organ", "Organ", "text", "values"),
        ("species", "Species", "text", "values"),
        ("sources", "Found in", "text", "values"),
    ]),
    ("partial", "Partial NAM records", ["partial"], [
        ("name", "Name", "text", None),
        ("type", "Proposed NAMO class", "text", "values"),
        ("method_type", "Method type", "text", "values"),
        ("organs", "Organ", "text", "values"),
        ("development_status", "Development status", "text", "values"),
        ("sources", "Found in", "text", "values"),
    ]),
]

KIND_LABELS = {"resource": "Resource", "nam": "NAM", "partial": "Partial NAM record"}


def record_link(path):
    return {"record_path": path, "record_url": f"{REPOSITORY}/blob/main/{path}"}


def found_in(resource_ids, resource_names):
    """The resources a NAM was found in: their ids, to match on, and names, to show."""
    return {
        "source_resource_ids": resource_ids,
        "sources": [resource_names.get(i, i) for i in resource_ids],
    }


def resource_row(resource):
    """A resource, with the fields computed for the table."""
    return {
        **resource,
        "kind": "resource",
        "type": resource.get("resource_type"),
        **found_in([], {}),
        "is_tox": "toxicology" in (resource.get("domain_areas") or []),
        **record_link(f"resources/{resource['id']}.yaml"),
    }


def nam_row(record, resource_names):
    """A NAM record, flattened for the table; the full record is kept for its details."""
    model = record["model"]
    return {
        "kind": "nam",
        "id": model["id"],
        "name": model.get("name") or model["id"],
        "description": model.get("description"),
        "type": model.get("type"),
        "organ": (model.get("organ_modeled") or {}).get("name"),
        "species": [s.get("name") or s["id"] for s in record.get("species") or []],
        **found_in([s["resource"] for s in record.get("source_resources") or []], resource_names),
        "synonyms": record.get("synonyms") or [],
        "record": record,
        **record_link(f"nams/{model['id']}.yaml"),
    }


def partial_row(partial, resource_names):
    """A partial NAM record, with the fields computed for the table."""
    return {
        **partial,
        "kind": "partial",
        "type": partial.get("proposed_namo_class"),
        **found_in([partial["resource"]], resource_names),
        **record_link(f"partial-nams/{partial['resource']}/{partial['id']}.yaml"),
    }


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NAMs Registry</title>
<style>
  :root {
    --bg: #f6f7fa; --surface: #ffffff; --fg: #1d2430; --muted: #5b6575; --line: #e3e7ee;
    --row-hover: #f3f5f9; --detail-bg: #f9fafc; --accent: #2f5fb3;
    --chip-bg: #eef2f8; --banner-bg: #2f4a8f; --banner-fg: #ffffff; --banner-muted: #d6def0;
    --tab-on-bg: #2f4a8f; --tab-on-fg: #ffffff; --badge-bg: #e6e9ef; --badge-fg: #2b3240;
    --partial-bg: #fdf1dc; --partial-fg: #7a4b00;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #101318; --surface: #14171c; --fg: #e6e9ef; --muted: #9aa3b2; --line: #2a303a;
      --row-hover: #1b2028; --detail-bg: #181c23; --accent: #8fb3ff;
      --chip-bg: #232a35; --banner-bg: #1c2a4d; --banner-fg: #eef2fb; --banner-muted: #a9b6d3;
      --tab-on-bg: #8fb3ff; --tab-on-fg: #0f1420; --badge-bg: #2a303a; --badge-fg: #dde2ea;
      --partial-bg: #3a2c12; --partial-fg: #f3c77a;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--fg);
    font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }
  header.banner { background: var(--banner-bg); color: var(--banner-fg); padding: 22px 0 24px; }
  header.banner .inner, main, footer { max-width: 1132px; margin: 0 auto; padding-left: 16px; padding-right: 16px; }
  header.banner nav { font-size: 14px; margin-bottom: 6px; }
  header.banner nav a { color: var(--banner-fg); }
  h1 { font-size: 26px; margin: 0 0 4px; }
  .subtitle { color: var(--banner-muted); margin: 0; }
  main { padding-top: 20px; padding-bottom: 48px; }
  .tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 16px; }
  .tabs button {
    font: inherit; color: var(--accent); background: var(--surface); cursor: pointer;
    border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px;
  }
  .tabs button[aria-selected="true"] { background: var(--tab-on-bg); color: var(--tab-on-fg); border-color: var(--tab-on-bg); }
  .tabs .n {
    display: inline-block; margin-left: 6px; padding: 0 7px; border-radius: 999px;
    font-size: 12px; background: var(--chip-bg); color: var(--muted);
  }
  .tabs button[aria-selected="true"] .n { background: rgba(255,255,255,.22); color: inherit; }
  .controls { display: flex; margin-bottom: 12px; }
  .controls input {
    flex: 1 1 260px; font: inherit; color: inherit; background: var(--surface);
    border: 1px solid var(--line); border-radius: 8px; padding: 9px 12px;
  }
  .note { color: var(--muted); font-size: 14px; margin: 0 0 12px; }
  tr.filters th { padding-top: 0; font-weight: 400; }
  button.sort {
    font: inherit; color: inherit; background: none; border: 0; padding: 0;
    cursor: pointer; white-space: nowrap;
  }
  button.sort .arrow { display: inline-block; width: 1em; color: var(--muted); }
  tr.filters select {
    font: inherit; font-size: 13px; color: inherit; background: var(--surface);
    border: 1px solid var(--line); border-radius: 6px; padding: 3px 6px;
    width: 100%; max-width: 13em;
  }
  td:nth-child(2) { min-width: 16em; }
  .count { color: var(--muted); font-size: 13px; margin: 0 0 8px; }
  .table-wrap { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
  table { width: 100%; border-collapse: collapse; }
  th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-size: 13px; color: var(--muted); font-weight: 600; white-space: nowrap; }
  tbody tr:last-child td { border-bottom: 0; }
  tr.summary { cursor: pointer; }
  tr.summary:hover { background: var(--row-hover); }
  .toggle {
    font: inherit; background: none; border: 0; color: var(--muted); cursor: pointer;
    width: 24px; padding: 0; line-height: 1;
  }
  .toggle[aria-expanded="true"] .chev { transform: rotate(90deg); }
  .chev { display: inline-block; font-size: 1.35em; transition: transform .12s; }
  .name { font-weight: 600; }
  .col-check { text-align: center; }
  .check { font-weight: 700; }
  .clamp {
    display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2;
    overflow: hidden; max-width: 34ch;
  }
  tr.detail td { background: var(--detail-bg); padding: 14px 16px 18px 44px; }
  dl { display: grid; grid-template-columns: max-content 1fr; gap: 6px 18px; margin: 0; }
  dt { color: var(--muted); font-size: 13px; }
  dd { margin: 0; }
  .chip {
    display: inline-block; background: var(--chip-bg); border-radius: 4px;
    padding: 1px 7px; margin: 0 4px 4px 0; font-size: 13px;
  }
  .badge {
    display: inline-block; background: var(--badge-bg); color: var(--badge-fg); border-radius: 4px;
    padding: 1px 8px; font-size: 13px; font-weight: 600; white-space: nowrap;
  }
  .badge.partial { background: var(--partial-bg); color: var(--partial-fg); }
  .callout {
    background: var(--partial-bg); color: var(--partial-fg); border-radius: 6px;
    padding: 8px 12px; margin: 0 0 12px; font-size: 14px;
  }
  a { color: var(--accent); }
  ul.pubs { margin: 0; padding-left: 18px; }
  ul.pubs li { margin-bottom: 4px; }
  .none { color: var(--muted); }
  footer { padding-bottom: 32px; color: var(--muted); font-size: 13px; }
  @media (max-width: 600px) {
    tr.detail td { padding-left: 16px; }
    dl { grid-template-columns: 1fr; }
    dt { margin-top: 6px; }
  }
</style>
</head>
<body>
<header class="banner"><div class="inner">
  <nav><a href="../">Documentation</a> &middot; <a href="__REPOSITORY__">Repository</a></nav>
  <h1>NAMs Registry</h1>
  <p class="subtitle" id="summary"></p>
</div></header>
<main>
  <div class="tabs" role="tablist" id="tabs"></div>
  <p class="note" id="note"></p>
  <div class="controls">
    <input id="q" type="search" aria-label="Filter">
  </div>
  <p class="count" id="count"></p>
  <div class="table-wrap">
  <table>
    <thead><tr id="headers"></tr><tr class="filters" id="filters"></tr></thead>
    <tbody id="rows"></tbody>
  </table>
  </div>
</main>
<footer><p>NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis, and the NAMs found in them.</p></footer>
<script>
const DATA = __DATA__;
const TABS = __TABS__;

// What each tab says above its table.
const NOTES = {
  all: "Every record in the registry: the resources reviewed, the NAMs recorded from them, and partial records of NAMs whose full records can't yet be held here.",
  resources: "Sources of NAMs, and of data about them, each reviewed for what it holds.",
  nams: "NAMs recorded in full from the resources, each as a NAMO model. Species, applications and limitations are held beside the model until NAMO covers them.",
  partial: "NAMs recorded only in part. A partial record holds only what its resource gives publicly, in the resource's own terms, because the registry can't hold that resource's full records. It reflects what the resource allows, not how far the NAM has been curated.",
};
const NOUNS = {
  all: ["record", "records"], resources: ["resource", "resources"],
  nams: ["NAM", "NAMs"], partial: ["partial NAM record", "partial NAM records"],
};

const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
// Shown for an empty value, such as a field not yet evaluated or recorded.
const DASH = `<span class="none" aria-label="Not recorded">&ndash;</span>`;
const a = (u, label) => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(label ?? u)}</a>`;
const link = u => u ? a(u) : DASH;
const chips = v => v && v.length ? v.map(x => `<span class="chip">${esc(x)}</span>`).join("") : DASH;
const text = v => v ? esc(v) : DASH;
const has = v => Array.isArray(v) ? v.length > 0 : Boolean(v);
const row = (label, html) => `<dt>${esc(label)}</dt><dd>${html}</dd>`;
const rowIf = (label, v, fmt = text) => has(v) ? row(label, fmt(v)) : "";
const LABELS = { three_d_architecture: "3D architecture" };
const label = k => LABELS[k] || k.charAt(0).toUpperCase() + k.slice(1).replace(/_/g, " ");

// A link for a CURIE where one is known, else null.
function curieUrl(id) {
  const s = String(id);
  const obo = s.match(/^(CL|UBERON|NCBITaxon|GO|HP|MONDO|CHEBI):(.+)$/);
  if (obo) return `https://purl.obolibrary.org/obo/${obo[1]}_${obo[2]}`;
  if (s.startsWith("doi:")) return "https://doi.org/" + s.slice(4);
  if (s.startsWith("PMID:")) return "https://pubmed.ncbi.nlm.nih.gov/" + s.slice(5);
  if (s.startsWith("aop:")) return "https://aopwiki.org/aops/" + s.slice(4);
  if (s.startsWith("aop.events:")) return "https://aopwiki.org/events/" + s.slice(11);
  if (/^https?:/.test(s)) return s;
  return null;
}
const curie = id => { const u = curieUrl(id); return u ? a(u, id) : esc(id); };
const term = t => t ? (t.id ? `${esc(t.name || t.id)} (${curie(t.id)})` : esc(t.name)) : DASH;
const terms = ts => ts && ts.length ? ts.map(t => `<span class="chip">${term(t)}</span>`).join("") : DASH;
const curies = ids => ids && ids.length ? ids.map(id => `<span class="chip">${curie(id)}</span>`).join("") : DASH;

function cell(r, [f, heading, display]) {
  const v = r[f];
  if (f === "name") return `<span class="name">${esc(v)}</span>`;
  if (display === "check") return v ? `<span class="check" role="img" aria-label="Yes">&#10003;</span>` : "";
  if (display === "clamp") return v ? `<span class="clamp">${esc(v)}</span>` : text(v);
  if (display === "badge") return v ? `<span class="badge${r.kind === "partial" ? " partial" : ""}">${esc(v)}</span>` : DASH;
  if (display === "issue") return v ? a(v, "#" + String(v).split("/").pop()) : DASH;
  return Array.isArray(v) ? chips(v) : text(v);
}

const recordRow = r => row("Registry record", a(r.record_url, r.record_path));
const resourceName = id => DATA.find(x => x.kind === "resource" && x.id === id)?.name || id;

function detailResource(r) {
  const pubs = (r.publications || []).map(p =>
    `<li>${a(curieUrl(p.id) || p.id, p.title || p.id)}${p.year ? " (" + esc(p.year) + ")" : ""}</li>`).join("");
  const scripts = (r.supporting_scripts || []).map(s => {
    const repo = String(s.repository || "").replace(/\\/+$/, "");
    const url = s.path ? `${repo}/blob/HEAD/${String(s.path).replace(/^\\/+/, "")}` : repo;
    return `<li>${a(url, s.name)}` +
      ` in ${esc(repo.replace(/^https?:\\/\\/(www\\.)?github\\.com\\//, ""))}` +
      (s.command ? `<br><code>${esc(s.command)}</code>` : "") +
      (s.description ? `<br>${esc(s.description)}` : "") + `</li>`;
  }).join("");
  const imp = (r.imported_from || []).map(i =>
    `${esc(i.source)} ${a(i.source_url, i.source_id)}, commit ${esc(i.source_version || "?")}, ${esc(i.imported_on)}`).join("<br>");
  const found = DATA.filter(x => x.kind !== "resource" && x.source_resource_ids.includes(r.id));
  const nams = found.filter(x => x.kind === "nam").length, partials = found.length - nams;
  return `<dl>
    ${row("Id", esc(r.id))}
    ${row("Homepage", link(r.homepage_url))}
    ${row("Description", text(r.description))}
    ${recordRow(r)}
    ${row("Resource type", text(r.resource_type))}
    ${row("Activity status", text(r.activity_status))}
    ${row("Domain areas", chips(r.domain_areas))}
    ${found.length ? row("NAMs from it", `${nams} NAM record${nams === 1 ? "" : "s"}, ${partials} partial record${partials === 1 ? "" : "s"}`) : ""}
    ${r.repository ? row("Repository", link(r.repository)) : ""}
    ${row("License", r.license ? (r.license.id ? a(r.license.id, r.license.label) : esc(r.license.label)) : DASH)}
    ${row("Curation model", chips(r.curation_model))}
    ${rowIf("Relevance note", r.relevance_note)}
    ${rowIf("DisMech integration", r.dismech_integration)}
    ${scripts ? row("Supporting scripts", `<ul class="pubs">${scripts}</ul>`) : ""}
    ${row("Priority", text(r.priority))}
    ${rowIf("Priority rationale", r.priority_rationale)}
    ${row("Extraction effort", text(r.extraction_effort))}
    ${rowIf("Effort rationale", r.effort_rationale)}
    ${rowIf("Expectations", r.expectations)}
    ${row("Publications", pubs ? `<ul class="pubs">${pubs}</ul>` : DASH)}
    ${row("Imported from", imp || DASH)}
  </dl>`;
}

function statements(list) {
  if (!list || !list.length) return DASH;
  return `<ul class="pubs">${list.map(s => {
    const src = (s.source_urls || []).map((u, i) => a(u, `source ${i + 1}`)).join(", ");
    const refs = (s.supporting_references || []).map(curie).join(", ");
    return `<li>${esc(s.description)}${src || refs ? ` <span class="none">(${[src, refs].filter(Boolean).join("; ")})</span>` : ""}</li>`;
  }).join("")}</ul>`;
}

// Model fields shown in their own rows; any other model field is shown below them.
const MODEL_SHOWN = new Set(["id", "type", "name", "description", "cell_types", "organ_modeled", "models", "references"]);
const plain = x => typeof x === "object" && x !== null ? (x.name || x.id || JSON.stringify(x)) : x;

function detailNam(r) {
  const rec = r.record, m = rec.model;
  const refs = (m.references || []).map(p =>
    `<li>${a(curieUrl(p.id) || p.id, p.title || p.id)}${p.year ? " (" + esc(p.year) + ")" : ""}</li>`).join("");
  const modeled = (m.models || []).map(x => x.biological_system_modeled).filter(Boolean);
  const others = Object.entries(m).filter(([k, v]) => !MODEL_SHOWN.has(k) && has(v))
    .map(([k, v]) => row(label(k), Array.isArray(v) ? chips(v.map(plain)) : typeof v === "object" ? term(v) : esc(v))).join("");
  const sources = (rec.source_resources || []).map(s =>
    `<li>${esc(resourceName(s.resource))}` +
    (s.accessed_on ? `, accessed ${esc(s.accessed_on)}` : "") +
    ((s.source_urls || []).length ? `<br>${s.source_urls.map(u => a(u)).join("<br>")}` : "") +
    ((s.products || []).length ? `<br>Products: ${s.products.map(p => p.url ? a(p.url, p.name) : esc(p.name)).join(", ")}` : "") +
    `</li>`).join("");
  const compared = (rec.compared_with || []).map(c =>
    `<li>${esc(DATA.find(x => x.kind === "nam" && x.id === c.nam)?.name || c.nam)}` +
    ` <span class="none">(${a(curieUrl(c.reference) || c.reference, c.reference)})</span></li>`).join("");
  const dm = rec.dismech_status;
  const dismech = dm ? [
    dm.processed_through_dismech ? "Came through DisMech curation" : "Did not come through DisMech curation",
    dm.present_in_dismech ? "in the DisMech graph" : "not in the DisMech graph",
  ].join("; ") + ` (${a("https://github.com/monarch-initiative/dismech/commit/" + dm.dismech_commit, "commit " + dm.dismech_commit.slice(0, 7))}, checked ${esc(dm.assessed_on)})` : "";
  return `<dl>
    ${row("Id", esc(r.id))}
    ${recordRow(r)}
    ${row("NAMO class", text(m.type))}
    ${row("Description", text(m.description))}
    ${rowIf("Synonyms", rec.synonyms, chips)}
    ${row("Species", terms(rec.species))}
    ${row("Organ modeled", m.organ_modeled ? term(m.organ_modeled) : DASH)}
    ${modeled.length ? row("Models", curies(modeled)) : ""}
    ${row("Cell types", terms(m.cell_types))}
    ${others}
    ${row("References", refs ? `<ul class="pubs">${refs}</ul>` : DASH)}
    ${row("Applications", statements(rec.applications))}
    ${row("Limitations", statements(rec.limitations))}
    ${row("Found in", sources ? `<ul class="pubs">${sources}</ul>` : DASH)}
    ${compared ? row("Compared with", `<ul class="pubs">${compared}</ul>`) : ""}
    ${dismech ? row("DisMech", dismech) : ""}
    ${rowIf("Created", rec.creation_date)}
    ${rowIf("Last modified", rec.last_modified_date)}
  </dl>`;
}

function detailPartial(r) {
  const source = r.sources[0];
  const pages = (r.source_urls || []).map(u => `<li>${a(u)}</li>`).join("");
  return `<p class="callout">A partial record. It holds only what ${esc(source)} gives publicly: it has no description, species, references, applications or limitations.</p>
  <dl>
    ${row("Id", esc(r.id))}
    ${recordRow(r)}
    ${row(`Pages in ${source}`, pages ? `<ul class="pubs">${pages}</ul>` : DASH)}
    ${row("Method type", text(r.method_type))}
    ${row("Proposed NAMO class", text(r.proposed_namo_class))}
    ${row("Development status", text(r.development_status))}
    ${row("Endpoints", chips(r.endpoints))}
    ${row("Organs", chips(r.organs))}
    ${row("Cell lines", chips(r.cell_lines))}
    ${row("Guidelines", chips(r.guidelines))}
    ${rowIf("Regulations", r.regulations, chips)}
    ${rowIf("Substances", r.substances, chips)}
    ${rowIf("Methods and biomarkers", r.methods_biomarkers, chips)}
    ${rowIf("AOP-Wiki AOPs", r.aops, curies)}
    ${rowIf("AOP-Wiki Key Events", r.key_events, curies)}
    ${row("Accessed on", text(r.accessed_on))}
  </dl>`;
}

const DETAIL = { resource: detailResource, nam: detailNam, partial: detailPartial };

// Labels for a "present" filter, by column display.
const PRESENT_LABELS = {
  check: ["\\u2713", "No \\u2713"],
  issue: ["Has issue", "No issue"],
  clamp: ["Recorded", "Not recorded"],
  text: ["Recorded", "Not recorded"],
};
const MISSING = "__missing__";
// What the filters call an empty value, by field.
const MISSING_LABEL = { holds_nams: "Not yet evaluated", type: "None" };

// Sort order for fields whose values are not ordered alphabetically.
const RANK = {
  priority: ["high", "medium", "low"],
  holds_nams: ["primary", "secondary", "unclear", "none"],
  kind_label: ["Resource", "NAM", "Partial NAM record"],
};

let tab = null, sortField = "name", sortDir = 1;
// Each tab's search, filters and sort, kept while another tab is open.
const STATE = {};
const tabRows = t => DATA.filter(r => t[2].includes(r.kind));
const holds = (v, value) => Array.isArray(v) ? v.includes(value) : v === value;

function sortKey(r, f) {
  let v = r[f];
  if (!has(v)) return null;
  if (Array.isArray(v)) v = v[0];
  if (RANK[f]) { const i = RANK[f].indexOf(v); return i < 0 ? RANK[f].length : i; }
  if (typeof v === "boolean") return v ? 0 : 1;
  if (f === "discussion_issue") return Number(String(v).split("/").pop());
  return String(v).toLowerCase();
}

function compare(r1, r2) {
  const x = sortKey(r1, sortField), y = sortKey(r2, sortField);
  if (x === null || y === null) return (x === null) - (y === null) || r1.name.localeCompare(r2.name);  // empty values last
  return (x < y ? -1 : x > y ? 1 : 0) * sortDir || r1.name.localeCompare(r2.name);
}

function filterControl(rows, [f, heading, display, filter]) {
  if (!filter) return "";
  const count = pred => rows.filter(pred).length;
  let options = "";
  if (filter === "values") {
    // Ranked values in their rank, then any value the rank does not list.
    const rank = v => { const i = RANK[f].indexOf(v); return i < 0 ? RANK[f].length : i; };
    const order = (x, y) => (RANK[f] && rank(x) - rank(y)) || String(x).localeCompare(String(y));
    const values = [...new Set(rows.flatMap(r => [].concat(r[f] ?? [])).filter(has))].sort(order);
    options = values.map(v => `<option value="${esc(v)}">${esc(v)} (${count(r => holds(r[f], v))})</option>`).join("");
    const missing = count(r => !has(r[f]));
    if (missing) options += `<option value="${MISSING}">${MISSING_LABEL[f] || "Not recorded"} (${missing})</option>`;
  } else {
    const [yes, no] = PRESENT_LABELS[display] || PRESENT_LABELS.text;
    options = `<option value="yes">${yes} (${count(r => has(r[f]))})</option>` +
              `<option value="no">${no} (${count(r => !has(r[f]))})</option>`;
  }
  return `<select data-field="${f}" data-filter="${filter}" aria-label="Filter ${esc(heading)}"><option value="">All</option>${options}</select>`;
}

const q = document.getElementById("q");
let selects = [];

function matches(r) {
  return selects.every(s => {
    if (!s.value) return true;
    const v = r[s.dataset.field];
    if (s.dataset.filter === "present") return has(v) === (s.value === "yes");
    return s.value === MISSING ? !has(v) : holds(v, s.value);
  });
}

function searchText(r) {
  return [r.id, r.name, r.description, r.type, ...(r.sources || []), ...(r.synonyms || []), ...(r.cell_lines || [])]
    .filter(Boolean).join(" ").toLowerCase();
}

function render() {
  const all = tabRows(tab);
  const term = q.value.trim().toLowerCase();
  const shown = all.filter(r => matches(r) && (!term || searchText(r).includes(term))).sort(compare);
  document.querySelectorAll("button.sort").forEach(b => {
    const on = b.dataset.field === sortField;
    b.closest("th").setAttribute("aria-sort", on ? (sortDir > 0 ? "ascending" : "descending") : "none");
    b.querySelector(".arrow").textContent = on ? (sortDir > 0 ? "\\u25B2" : "\\u25BC") : "";
  });
  const [one, many] = NOUNS[tab[0]];
  document.getElementById("count").textContent = `${shown.length} of ${all.length} ${all.length === 1 ? one : many}`;
  const columns = tab[3];
  document.getElementById("rows").innerHTML = shown.map((r, i) => `
    <tr class="summary">
      <td><button class="toggle" aria-expanded="false" aria-controls="d${i}" aria-label="Show details for ${esc(r.name)}"><span class="chev">&#9656;</span></button></td>
      ${columns.map(c => `<td class="col-${c[2]}">${cell(r, c)}</td>`).join("")}
    </tr>
    <tr class="detail" id="d${i}" hidden><td colspan="${columns.length + 1}">${DETAIL[r.kind](r)}</td></tr>`).join("");
}

function showTab(key) {
  if (tab) STATE[tab[0]] = {
    q: q.value, sortField, sortDir,
    filters: Object.fromEntries(selects.map(s => [s.dataset.field, s.value])),
  };
  tab = TABS.find(t => t[0] === key) || TABS[0];
  // A tab opens as it was left; the first time, All records is grouped by
  // kind (resources, then NAMs, then partial records) and the others sorted by name.
  const state = STATE[tab[0]] || {
    q: "", sortField: tab[0] === "all" ? "kind_label" : "name", sortDir: 1, filters: {},
  };
  ({ sortField, sortDir } = state);
  q.value = state.q;
  document.querySelectorAll("#tabs button").forEach(b => b.setAttribute("aria-selected", String(b.dataset.tab === tab[0])));
  document.getElementById("note").textContent = NOTES[tab[0]];
  q.placeholder = `Filter ${tab[0] === "all" ? "all records" : tab[1]}`;
  const columns = tab[3], rows = tabRows(tab);
  document.getElementById("headers").innerHTML = "<th></th>" + columns.map(([f, heading, display]) =>
    `<th class="col-${display}" aria-sort="none"><button class="sort" data-field="${f}">${esc(heading)}<span class="arrow" aria-hidden="true"></span></button></th>`).join("");
  document.getElementById("filters").innerHTML = "<th></th>" + columns.map(c => `<th>${filterControl(rows, c)}</th>`).join("");
  selects = [...document.querySelectorAll("#filters select")];
  selects.forEach(el => {
    el.value = state.filters[el.dataset.field] || "";
    el.addEventListener("input", render);
  });
  document.querySelectorAll("button.sort").forEach(b => b.addEventListener("click", () => {
    sortDir = b.dataset.field === sortField ? -sortDir : 1;
    sortField = b.dataset.field;
    render();
  }));
  render();
}

document.getElementById("tabs").innerHTML = TABS.map(t =>
  `<button role="tab" data-tab="${t[0]}" aria-selected="false">${esc(t[1])}<span class="n">${tabRows(t).length}</span></button>`).join("");
document.getElementById("tabs").addEventListener("click", e => {
  const b = e.target.closest("button[data-tab]");
  if (!b) return;
  history.replaceState(null, "", "#" + b.dataset.tab);
  showTab(b.dataset.tab);
});
window.addEventListener("hashchange", () => showTab(location.hash.slice(1)));

const n = k => DATA.filter(r => r.kind === k).length;
document.getElementById("summary").textContent =
  `${DATA.length} records: ${n("resource")} resources, ${n("nam")} NAMs, ${n("partial")} partial NAM records`;

document.getElementById("rows").addEventListener("click", e => {
  if (e.target.closest("a")) return;
  const r = e.target.closest("tr.summary");
  if (!r) return;
  const btn = r.querySelector(".toggle");
  const d = document.getElementById(btn.getAttribute("aria-controls"));
  const open = btn.getAttribute("aria-expanded") === "true";
  btn.setAttribute("aria-expanded", String(!open));
  d.hidden = open;
});
q.addEventListener("input", render);
showTab(location.hash.slice(1));
</script>
</body>
</html>
"""


def to_json(value):
    """Serialize for embedding in a <script> element."""
    return json.dumps(value, default=str, ensure_ascii=False).replace("</", "<\\/")


def load(pattern):
    records = []
    for path in sorted(glob.glob(pattern)):
        with open(path) as fh:
            records.append(yaml.safe_load(fh))
    return records


def main(argv=None):
    """Build the page."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resources", default="resources", help="Directory of resource files (default: resources)")
    parser.add_argument("--nams", default="nams", help="Directory of NAM records (default: nams)")
    parser.add_argument("--partial-nams", default="partial-nams", help="Directory of partial NAM records, one folder per resource (default: partial-nams)")
    parser.add_argument(
        "--output", default="docs/resources/index.html",
        help="Page to write (default: docs/resources/index.html)",
    )
    args = parser.parse_args(argv)

    resources = load(os.path.join(args.resources, "*.yaml"))
    names = {r["id"]: r["name"] for r in resources}
    rows = [resource_row(r) for r in resources]
    rows += [nam_row(r, names) for r in load(os.path.join(args.nams, "*.yaml"))]
    rows += [partial_row(p, names) for p in load(os.path.join(args.partial_nams, "*", "*.yaml"))]
    for r in rows:
        r["kind_label"] = KIND_LABELS[r["kind"]]
    rows.sort(key=lambda r: r["name"].lower())

    page = (
        PAGE.replace("__TABS__", to_json(TABS))
        .replace("__DATA__", to_json(rows))
        .replace("__REPOSITORY__", REPOSITORY)
    )
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as fh:
        fh.write(page)
    counts = {k: sum(r["kind"] == k for r in rows) for k in KIND_LABELS}
    print(f"Wrote {counts['resource']} resources, {counts['nam']} NAM records and {counts['partial']} partial NAM records to {args.output}")


if __name__ == "__main__":
    main()
