# Phase 2 addendum: designing the database and dashboard for grounded question-answering

**Status:** architecture requirement for Phase 2, October 23, 2026. Nothing here builds a chatbot. It fixes the shape of the data so that a later conversational interface can answer a resident's question from Berkeley's own records, show the arithmetic, and cite the page.

**Companion documents:** `plans/phase2-capital-choices-vision-2050-plan-2026-10-22.md` (the research plan this constrains), `plans/dashboard-phase2-spec.md` (the two trackers), `plans/fund-dashboard-and-agents-plan-2026-10-22.md` (fund ledger and agent pipeline), `data/funds/SCHEMA.md`, `AGENT_COORDINATION.md`.

## 0. The target, and what it rules out

The target is a system where a resident types "How much General Fund money went into the Marina since 2022, and how many blocks of paving is that?" and receives: the retrieved figures with page citations, the calculation written out, the one legal fact that changes the answer (which of those dollars were ever transferable), the assumptions behind the paving conversion, and an explicit statement of what the record does not contain.

That rules out a model that "knows about Berkeley". The model's only job is to resolve the question into entities, measures and periods; call retrieval; call a calculator; and write prose around results it did not produce. Every number in an answer must trace to a stored fact or to a calculation over stored facts. This is the same discipline the fund ledger already enforces ("agents never infer a dollar figure"), applied to the answer layer.

**The strongest counterargument** to building toward this now: the Phase 2 research plan has not yet located the FY2027–2031 CIP in machine-readable form, the StreetSaver data, or the asset register. Designing a retrieval layer over data that does not yet exist risks architecture without content. The answer is that the requirements below cost almost nothing when applied at design time (an id column, a basis column, a source locator) and are expensive to retrofit. The fund ledger already satisfies most of them. The addendum therefore specifies conventions for data Phase 2 will create, plus a small compile step over data that exists. It does not add a workstream.

## 1. Stable identifiers

Every record an answer could cite gets a URI-like id in a fixed namespace. Ids are never renamed. A record that is replaced gets `superseded_by`; a record known by other names gets `aliases[]`.

| Namespace | Form | Exists today? | Notes |
|---|---|---|---|
| `fund:` | `fund:608`, `fund:ACFR-park-tax` | Yes, as file names | Keep every current id. The `ACFR-<slug>` ids are FY2025 compatibility ids; the historical fund-identity table the coordination doc calls for maps them to City fund numbers when known, with `aliases[]`. Never rename. |
| `flow:` | `flow:608-2023-07-25-wc-loan` | Yes, within a fund | Existing `id` values are already unique within a fund and carry the fund prefix. Global form is the prefix plus the existing id. |
| `year:` | `fund:608/annual/2025/audited` | Derivable | Annual rows are addressed by their existing identity `(fund, fy, basis, series, balance_version)`. No new stored key; the compile step (section 3) materializes the id. |
| `doc:` | `doc:acfr-fy2025`, `doc:council-2023-07-25-item-NN` | Partly | Today each fund file has a private `sources` map with local keys (`acfr-2025`, `prw-2026-09`). Section 2 adds one global source register; per-fund keys stay as they are and gain a `doc_id` pointer. |
| `action:` | `action:2023-07-25-res-70997`, `action:2026-09-29-item-26` | No | Council and commission decisions: resolution, ordinance, consent item, referral, AAO amendment. The Closer agent (plan section 5.2) is the natural writer. |
| `project:` | `project:cip-<City project number>` or `project:beth-<slug>` when the City prints none | No | Phase 2 workstream 1. The City's own CIP project number is the id when it exists; the crosswalk in implementation step 2 maps CIP, fund, Vision 2050 system and GIS ids. |
| `asset:` | `asset:streetsaver-<segment id>`, `asset:facility-<slug>` | No | Workstream 2 and 5. System-qualified so two registers cannot collide. |
| `measure:` | `measure:U`, `measure:Y`, `measure:T1` | Implicit in text | Ballot measures as entities, because restrictions are the join key for every "could this money have paved streets" question. |
| `scenario:` | `scenario:pci60-reallocation-v1` | No | A named set of assumptions (section 5), versioned. |
| `claim:` | `claim:marina-wc-loan-booking` | No | A BeTH finding or dispute, with its counterargument. Keeps interpretation separate from fact (section 5). |

Rules:

1. Ids are lowercase ASCII, hyphen-separated, with the namespace as prefix. They are strings in JSON; no integer surrogate keys.
2. An id is assigned once, in the file that owns the record. Other files reference it; they do not redefine it.
3. The validator (`tools/ledger.py` and its successors) checks that every reference resolves. A dangling reference fails CI, like a dangling `source` does today.
4. Published pages carry the id of each number they print as a `data-fact` attribute (section 7), so the HTML is itself traversable.

## 2. Provenance, period, basis, and figure status

### 2.1 Source register (`data/sources/registry.json`)

One entry per document, keyed by `doc:` id:

| Field | Meaning |
|---|---|
| `title`, `publisher`, `doc_type` | `acfr`, `adopted_budget`, `aao`, `agenda_item`, `annotated_agenda`, `staff_report`, `presentation`, `auditor_report`, `resolution`, `ordinance`, `plan`, `dataset`, `secondary` |
| `url` | Canonical City URL |
| `retrieved` | ISO date BeTH fetched it |
| `sha256` | Of the fetched file. The FY2025 fixture test already hashes the ACFR; this generalizes it. |
| `published` | Date on the document |
| `period` | `{fy_start, fy_end}` or `{as_of}`: what the document reports on, as distinct from when it was published |
| `pages` | Page count |
| `local_path` | Where the file or its extracted text lives (section 4) |
| `supersedes` / `superseded_by` | For revised packets ("Supp 2" supersedes "Supp 1"; the Sept 2025 Exhibit A supersedes the Dec 2020 T1 roster) |
| `known_defects[]` | Recorded data-quality problems in the document itself. First entry: the FY2025 ACFR ten-year statistical schedule repeats FY2022-level figures under FY2023 and FY2024 for every business-type row, so FY2015–2024 series are taken from the FY2024 ACFR. |

Migration: each fund file's `sources.<key>` gains `"doc_id": "doc:..."`. Nothing else in the fund files changes. The register is a new file, so it is not one of the shared files listed in the coordination doc; adding `doc_id` to the `sources` entries is a schema addition and goes in a PR that names `data/funds/SCHEMA.md` and `tools/ledger.py` as touched, per the coordination rules.

### 2.2 Locator

A citation to a document is not enough for a verifier to check; it needs a place. Every fact carries:

```
"cite": {"doc_id": "doc:acfr-fy2025", "page": 77, "table": "Statement of Revenues, Expenditures and Changes in Fund Balances", "line": "Community development and housing", "quote": "Community development and housing   20,312,…"}
```

`page` is the PDF page index, not the printed folio, so a script can open it. `quote` is the extracted text the number came from, so a checker can confirm the number appears there. This is exactly the check that would have caught the $36.6M wrapped-line gap on p.77 earlier: the quote for "Community development" would have carried only the first line's figure.

The existing `source` string on year blocks and flows remains the short form; `cite` is optional and additive, populated by the extractor where it has the page and by hand on curated rows.

### 2.3 Period and accounting basis

| Field | Values | Where it lives |
|---|---|---|
| `fy` / `as_of` / `period` | Fiscal year ending June 30; a balance-sheet date; or a date range for a flow | Exists on year blocks, flows, obligations |
| `basis` (reporting basis) | `audited`, `adopted`, `amended`, `projected`, `estimated` | Exists with three values; `amended` (AAO) and `estimated` (BeTH or staff estimate not in an adopted document) are additive. The dashboard Phase 2 spec's rule that bases are never summed on one axis extends to these. |
| `accounting_basis` | `modified_accrual` (governmental fund statements), `accrual` (proprietary fund statements, government-wide, statistical section), `budgetary`, `cash` | Derivable from fund type and `series` for existing rows; stored explicitly on facts the compile step emits, so an answer can say "these two figures are on different bases" instead of netting them. The Marina FY2015–2024 rows (government-wide schedule, full accrual) versus FY2025 (fund statement) are the live case; the `series` field exists for it and the coordination doc defers the convention to Steve. |
| `figure_status` | `reported`, `derived`, `disputed` | `reported` is the default. `derived` marks a number BeTH computed (a sum, a difference, a per-unit rate) and must carry a `calc` (section 5). `disputed` marks a reported figure BeTH contests; the figure stays, and a `claim:` record holds the dispute. |

A disputed figure is not a separate basis. The $5.5M Workers' Compensation loan authorized July 25, 2023 is `audited` in neither ACFR as booked; the FY2025 ACFR's $2,477,099 due to the General Fund is `audited` and `disputed`, and `claim:marina-wc-loan-booking` holds both figures, the resolution citation, and the counterargument. Both numbers stay retrievable; neither is "corrected" in the data.

### 2.4 Confidence and review

Unchanged: `confidence` (High/Moderate/Low/Unknown) and `reviewer` (`agent:proposed` until a person signs). The answer layer treats `agent:proposed` rows exactly as the pages do: invisible. A question whose only evidence is an unreviewed proposal returns "no reviewed evidence", not the proposal.

## 3. Machine-readable numbers: the compiled facts table

The fund JSONs are already integers in whole dollars with sources. What is missing is one place where every number from every subject (funds, flows, trackers, projects, assets, Council actions) can be queried with the same columns. That is a build artifact, not a new hand-maintained file.

`tools/build_facts.py` reads `data/funds/*.json`, `data/tracker/*.json`, `data/projects/*.json`, `data/assets/*.json`, `data/actions/*.json` as each comes into existence, and writes:

- `docs/data/facts.jsonl` and `docs/data/facts.csv`: long format, one row per number.
- `docs/data/beth.sqlite`: the same rows plus the entity, document, link and measure tables, for a browser (sql.js) or a serverless function to query with SQL. At current scale (106 funds, a few hundred flows) this is well under a megabyte; with a full CIP and StreetSaver segments it stays in the low tens of megabytes, which a static host serves without difficulty. (Moderate: depends on segment count; Berkeley's network is on the order of a few thousand segments.)
- `docs/data/measures.json`: the measure dictionary.

Fact row:

| Column | Meaning |
|---|---|
| `fact_id` | Derived, stable: `fund:608/annual/2025/audited/revenue`, `flow:608-2023-07-25-wc-loan/amount`, `project:cip-1234/encumbered/2026-06-30` |
| `entity_id` | The `fund:`, `project:`, `asset:`, `action:` it describes |
| `measure` | Key into `measures.json`: `revenue`, `expenditure`, `transfers_in`, `ending_balance`, `flow_amount`, `appropriation`, `encumbrance`, `expended_to_date`, `pci`, `lane_miles`, … |
| `value`, `unit` | Integer dollars, or the measure's unit (`pci_points`, `lane_miles`, `fte`) |
| `fy`, `as_of`, `period_start`, `period_end` | Whichever applies; the rest `null` |
| `basis`, `accounting_basis`, `figure_status` | Section 2.3 |
| `doc_id`, `page`, `quote` | Section 2.2; the per-fund source key is resolved to the global `doc_id` |
| `confidence`, `reviewer` | Carried through |
| `related[]` | For flows: `from_fund`, `to_fund`, `action_id`, `recurring`; for projects: `fund_ids[]`, `measure_ids[]` (ballot measures), `restriction` |
| `series`, `balance_version` | Carried through when set |

`measures.json` defines each measure once: plain-language definition, unit, sign convention, what it includes and excludes (the conventions in `AGENT_COORDINATION.md`: governmental `expenditure` includes capital outlay and debt service and excludes transfers; proprietary `expenditure` includes depreciation), which bases it can carry, and which measures it must never be summed with. The dictionary is what lets a calculator refuse to add `adopted` to `audited`, or revenue to transfers in, rather than relying on a prompt to remember.

Acceptance tests for the compile step, added to CI next to the extraction-safety tests:

1. Every fact has a `doc_id` that resolves in the register and a `confidence`.
2. Every `entity_id` and every id in `related[]` resolves.
3. Summing the facts for FY2025 `audited` fund columns reproduces each statement's Total column in `data/dashboard/statement-totals.json` to within $1. This is the existing dashboard control-total check, moved down to the data layer so every consumer inherits it.
4. No fact with `reviewer: agent:proposed` appears in `docs/data/`.

## 4. Retrieval layer

Two kinds of retrieval, because two kinds of question. "How much did fund X spend in FY2025" is a lookup. "What did staff say the reason was" is a text search. Most real questions need both.

### 4.1 Structured retrieval

The SQLite file is the structured index. An entity table carries names, aliases and synonyms so that "Marina", "Waterfront", "harbor fund" and "608" all resolve to `fund:608`, and "paving", "street rehabilitation", "resurfacing" resolve to the street-related funds (`ACFR-measure-b-local-streets-and-roads`, `ACFR-measure-bb-local-streets-and-roads`, `ACFR-measure-f-alameda-county-vrf-street-and-road`, `ACFR-street-improvement`, the relevant `project:` and `asset:` records). The synonym list is hand-maintained in `data/entities.json` and is the one place where plain civic language is mapped onto City nomenclature, which also serves the jargon-discipline goal of the site.

A `links` table holds typed edges between ids: `flow → fund (from, to)`, `flow → action (authorized_by)`, `fund → measure (restricted_by)`, `project → fund (funded_from)`, `project → asset (improves)`, `action → doc (recorded_in)`, `claim → fact (disputes)`. Edges are written by the same tools that write the records (the ledger clerk writes a flow and its `authorized_by`; the CIP extractor writes `funded_from`). Nothing infers an edge.

### 4.2 Document retrieval

The register (section 2.1) points to extracted text per page: `data/sources/text/<doc_id>/p<NNNN>.txt`. The FY2025 ACFR already sits in the repo; its text is a few megabytes. For the historical ACFRs, budgets and agenda packets the Phase 2 plan will pull, text (not PDFs) goes in the repo, PDFs stay in a scratch location keyed by `sha256`, as the FY2024 ACFR was handled during curation. If text volume becomes a problem for the repo, it moves to a `beth-sources` repository or an object store, with the register's `local_path` becoming a URL. (High that page text is enough for citation checking; the `quote` field is matched against it.)

A chunk index `docs/data/chunks.jsonl` splits page text into passages with `doc_id`, `page`, character offsets, and the entity ids the build step found in the passage by matching `entities.json` aliases. Keyword search over chunks (BM25) runs in a browser or a function with no infrastructure. Dense (embedding) retrieval is deferred: it needs either a precomputed vector file, which is fine at this scale, or a hosted index. The design leaves a `chunk_id` on every citation so adding embeddings later changes the ranker, not the data.

### 4.3 What retrieval returns

A retrieval result is a list of fact rows and chunk passages with their ids. It never returns a number without its `fact_id`, and never a passage without `doc_id` and `page`. This is the boundary the answer contract (section 5) depends on.

## 5. Separating facts, calculations, interpretations, and scenario assumptions

Every answer, whether a future conversational reply or a number on today's dashboard, is an instance of one answer object:

```json
{
  "question": "...",
  "resolution": {
    "entities": ["fund:608", "fund:011"],
    "measures": ["flow_amount"],
    "period": {"fy_start": 2022, "fy_end": 2026},
    "ambiguities": ["'the Marina' taken as fund 608, not the Waterfront parks in the Parks Tax fund"]
  },
  "facts": [
    {"fact_id": "flow:608-2023-07-25-wc-loan/amount", "value": 5500000, "basis": "adopted", "cite": {...}},
    {"fact_id": "fund:608/annual/2025/audited/transfers_in", "value": 2477099, "basis": "audited", "cite": {...}}
  ],
  "calculations": [
    {"id": "c1", "expression": "sum(facts where kind in (transfer_in, loan_in, cost_shift) and to_fund = fund:608 and fy between 2022 and 2026 and from_fund in general_fund_or_unrestricted)", "inputs": ["flow:...", "flow:..."], "result": 0, "unit": "usd", "note": "basis mixed: adopted and audited rows are listed separately, not summed"}
  ],
  "interpretation": [
    {"claim_id": "claim:marina-rescue-sources", "text": "...", "counterargument": "...", "confidence": "Moderate"}
  ],
  "scenario_assumptions": [
    {"scenario_id": "scenario:paving-unit-cost-v1", "parameter": "cost_per_lane_mile", "value": null, "source": "not yet in the record; StreetSaver export pending", "set_by": "default"}
  ],
  "missing_evidence": [
    {"needed": "repayment schedule actually followed for Res. 70,997", "would_be_in": "FY2026 ACFR note on interfund balances; Waterfront TOT receipts by year", "status": "not in record"}
  ],
  "verifier": {"numbers_traced": true, "citations_resolved": true, "quotes_matched": true}
}
```

The four middle blocks are distinct by construction and are rendered as four distinct blocks, with labels a reader cannot miss: **From the record**, **Arithmetic**, **BeTH's reading**, **Assumptions you can change**. The rules:

- `facts[]` contains only rows returned by retrieval, verbatim.
- `calculations[]` are executed by code (SQL or a small expression evaluator over fact ids), not by the model. The model may propose an expression; the system runs it and reports the result. An expression that mixes bases or incompatible measures is rejected by the measure dictionary, and the rejection is itself reported.
- `interpretation[]` entries are `claim:` records or are marked `unreviewed`. A `claim:` carries the counterargument field the fund plan already requires on every finding.
- `scenario_assumptions[]` are the only place a user-supplied or default parameter may enter. A parameter with no source is `null` with a note, never a plausible-looking guess. This matches the ledger rule that agents never infer dollar figures and the Phase 2 rule that forecasts display assumptions and uncertainty.
- `missing_evidence[]` is required, and may be empty only when the verifier confirms every entity and measure in `resolution` has a fact in `facts`.

## 6. Citations and missing evidence as hard requirements

The verifier is a deterministic check that runs on every answer object before anything renders:

1. Every number in the prose (matched by pattern) equals a `value` in `facts[]` or a `result` in `calculations[]`, allowing for the stated rounding. An unmatched number fails the answer.
2. Every `fact_id` and `doc_id` resolves in the published data.
3. Every `cite.quote` appears in the page text the register points to.
4. Every `interpretation` entry has a counterargument.
5. Every entity and measure the resolution named either has a fact or an entry in `missing_evidence`.

A failed answer is not shown with a disclaimer; it is replaced by the list of what failed and the facts that did pass. A gap register `data/gaps.json` (the dashboard's `known-gaps.json` generalized) records recurring missing evidence with the document that would fill it, so repeated questions about, say, FY2026 encumbrances return the same precise statement about where the number will appear and when.

## 7. Cross-subject questions

The join keys are fund ids, ballot-measure ids, action ids and fiscal years. The worked question for Phase 2 acceptance:

> "Could the money that rescued the Marina have paved streets instead?"

Resolution: entities `fund:608`, every `from_fund` on its FY2022–2026 inflow `flow:` records, and the street funds and `project:` records tagged paving; measures `flow_amount`, `restriction`, `cost_per_lane_mile`; period FY2022–2026.

Facts: the six rescue pockets already in `data/funds/608.json` (ARPA $1.4M and $1.15M; the $5.5M Workers' Compensation loan; the $7.69M State grant; the $1.4M General Fund contribution redirected from Measure U1 Small Sites; the $1.579M/yr Parks Tax cost shift), each with its source fund's `restriction` and governing `measure:`.

Calculation, executed by code: partition inflows by the source fund's legal transferability to street work. ARPA (federal purpose rules), the State grant (grant agreement), and Parks Tax (Measure Y, parks) are not transferable to paving; the General Fund contribution is unrestricted; the Workers' Compensation loan is an internal-service loan whose transferability is a legal question, not a data fact. Sum only the unrestricted set. Convert to lane-miles only if `cost_per_lane_mile` has a sourced value; otherwise report the dollar figure and a `null` conversion.

Interpretation: `claim:` record stating what the partition shows, with the counterargument (the General Fund dollars were themselves backfilled by a U1 redirection, so "unrestricted" understates the chain of displacement).

Assumptions: which unit cost, which treatment mix; defaults `null` until the StreetSaver export exists.

Missing evidence: actual Workers' Compensation repayment to date; whether any Waterfront TOT has been diverted; FY2026 figures (ACFR expected early 2027).

Everything this question needs is either in the fund ledger today or is a field the Phase 2 workstreams already plan to collect. The requirement this addendum adds is that workstreams 1, 2 and 3 record their data with the same `entity_id`, `basis`, `doc_id`/`page`, `restriction` and `measure:` columns, so the join exists when the question is asked. Concretely, for the capital inventory in workstream 1 the field list in the Phase 2 plan is kept and three columns are made mandatory: `project_id` (section 1), `funded_from[] {fund_id, measure_id, restriction, amount, basis, doc_id, page}`, and `as_of` on every balance (appropriation, expended to date, encumbrance), since a capital balance without a date is not a fact.

## 8. Architecture, including the conversational interface, in three stages

### Stage A (Phase 2, static, no backend)

```
data/funds, data/tracker, data/projects, data/assets, data/actions, data/sources
        │
        ▼  tools/build_facts.py  (CI: resolves ids, reproduces control totals)
docs/data/facts.jsonl · beth.sqlite · measures.json · entities.json · chunks.jsonl
        │
        ├──► dashboard and fund pages: every printed number carries data-fact="<fact_id>";
        │    an evidence drawer shows the fact row, citation and page text on click
        │
        └──► docs/ask/<slug>.html: canonical questions answered offline through the
             answer contract, verified, reviewed by Steve, published as pages
```

The "Ask" pages are the conversational interface rehearsed without a model in the loop at run time: an agent (Claude Code task, same guardrails as the pipeline agents) drafts the answer object for a listed question, the verifier runs, Steve reviews the PR, the page renders the four blocks. This proves the contract, builds the FAQ corpus that later caches the most common live questions, and costs no infrastructure. It is compatible with GitHub Pages and the Vercel static project as they are.

Client-side querying is also possible at this stage: sql.js and a BM25 library can run against the published SQLite and chunks in the browser, giving a "find a number" box with no server. (High that this works at the stated scale.)

### Stage B (after Phase 2 publishes: the smallest backend)

A live question requires a model call, which requires a secret, which requires a server. The smallest arrangement that fits what BeTH already runs:

- **One serverless function** on the existing Vercel project (`berkeley-transparency-hub`), `POST /api/ask`.
- **No database server.** The function reads the same published `beth.sqlite`, `chunks.jsonl` and `entities.json` from the deployment bundle. The static site remains the database; a deploy is a data release.
- **One model with tool use.** The function exposes three tools to the model: `resolve(question) → entities, measures, period`, `query(sql) → fact rows` (read-only, against the SQLite), `search(text) → chunks`, and `calculate(expression over fact_ids) → result`. The model writes the prose; the function assembles the answer object, runs the verifier (section 6), and returns the object, not free text. Claude via the Messages API is the default given the existing toolchain; the contract is provider-neutral.
- **One key-value store** (Upstash Redis, already used by MNVscore) for rate limiting per IP, an answer cache keyed by normalized question, and an anonymized question log to feed the Ask pages.
- **Secrets:** one model API key and one Redis token, in Vercel environment variables. No user accounts, no PII stored, no write path to the repo from the function.
- **Cost control:** a token cap per answer, cache hits served without a model call, and a daily spend ceiling that switches the endpoint to cache-only when reached.

Everything on the public page stays static. The one dynamic element is a form that posts to the function and renders the returned object in the same four-block layout the Ask pages use.

### Stage C (when Stage B shows the need)

Precomputed embeddings for `chunks.jsonl` stored as a static file, or a hosted vector index, to improve passage retrieval. A conversation memory limited to the resolved entities of the previous turn, so "and the General Fund?" works, with no persistence beyond the session. A feedback control ("this citation is wrong") that opens an issue, not a write.

## 9. What changes in Phase 2 now

Small, additive, and in priority order:

1. **`data/sources/registry.json`** with `doc:` ids for every document the fund files and the Phase 2 plan cite, and `doc_id` pointers added to each fund file's `sources` entries. Half a day. Touches `SCHEMA.md` and `ledger.py` (additive field), to be named in the PR per `AGENT_COORDINATION.md`.
2. **`tools/build_facts.py`** emitting `facts.jsonl`, `beth.sqlite`, `measures.json` from the fund files, with the four acceptance tests in section 3. One day. Dashboard-owned (Claude), reading ledgers, writing only to `docs/data/`.
3. **`data/entities.json`** aliases for the funds and the first street and Marina entities. Two hours, grows with use.
4. **Workstream 1 schema** for `data/projects/*.json` using section 7's three mandatory columns, written before any CIP extraction starts.
5. **`data/actions/*.json`** schema for Council decisions, written before the Closer agent is built, so the pipeline writes `action:` records from its first run.
6. **Evidence drawer** on the dashboard: `data-fact` attributes on every number and a click-through to the fact row and citation. This is the first user-visible product of the addendum and the test of whether the data supports it.
7. **Five Ask pages** on the Phase 2 research questions, produced through the contract and verified, as the acceptance test for Stage A.

Items 1 to 3 can start before the Phase 2 data exists, because they run on the 106 fund files already in the repo. Items 4 and 5 are schema decisions that cost nothing if made first and a migration if made later.

## 10. What this addendum does not claim

- That a conversational interface will be accurate because the data is structured. It will be accurate only to the extent the verifier is strict and the record is complete; the `missing_evidence` field exists because the record is not complete.
- That the CIP, StreetSaver or asset-register data exist in machine-readable form. The Phase 2 plan lists them as unknowns and this addendum only fixes the shape they take when found.
- That dense retrieval, conversation memory or a hosted database are needed. Each is deferred until a measured shortfall in Stage A or B shows it is.
- Any dollar figure. The numbers quoted above are the fund ledger's, cited there; none is new.
