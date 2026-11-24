# Spec: An interactive visual model of water flowing into and out of Berkeley's Aquatic Park

*Prepared for Steve Kromer, Learn About Berkeley, November 24, 2026. Hand this to any coding tool. Everything a builder needs is here: the physical picture, the numbers with sources, the equations, the scenarios, the screens, and the checks that tell you the build is right.*

## 1. What to build, in one paragraph

A single web page that shows, in motion, how water gets into and out of the main lagoon at Aquatic Park, and lets a viewer change the five things that matter: how well the five tide tubes under I-80 work, whether the 12-inch board on the Strawberry Creek weir is in place, how big a storm is falling on the City, how high the tide is, and how deep the lagoon is. The page runs a simple hourly water balance for 14 to 90 simulated days, animates the result on a map-like picture of the park, and shows four numbers that change as the viewer moves the sliders: tidal exchange per cycle, lagoon water level, lagoon salinity, and days to flush a storm. It should be beautiful before it is precise. The precision it does have comes from the City's own 2008 study, and the page must say where every number comes from.

## 2. Form and constraints

- **One self-contained HTML file** (inline CSS, inline JavaScript, inline SVG). No CDN, no build step, no external fonts required (system sans-serif is fine; Jost if available). It will be hosted as a static file at jskromer.github.io/BeTH-/ and learn-about-berkeley.vercel.app, next to the existing page `berkeley-aquatic-park.html`, and must work offline from a file:// URL.
- If the builder prefers Streamlit or Observable, that is acceptable as a second deliverable, but the HTML file is the one that ships.
- Must render on a phone (375 px wide) and a laptop. Target under 300 KB. No images; the picture is drawn in SVG.
- Palette, to match the site: royal blue #002198, navy #000d6b, deep navy #000845, light blue #7a90d9, wash #e4e7f3, paper #ebecee, ink #0b1540, muted #4b5577, rule #d3d6db, flag red #b3261e, ok green #1f6b4a, warn amber #8a5a00. Bay water #cdd3e8; lagoon water graded from #7a90d9 (salty) toward #c8e6c9 (fresh) as salinity falls.
- Tone: a civic explainer, not a game. No sound. Animation should be calm: particles drifting, a tide gauge rising and falling, a clock advancing.

## 3. The physical picture (what the drawing must show)

Draw a stylized plan view, north up, roughly 900 × 520 units:

1. **San Francisco Bay** on the left, a band of light blue.
2. **I-80 / Eastshore Highway** as a dark vertical band on 1930s fill.
3. **The main lagoon**, about 1 mile long and 58.3 acres, a long blue shape east of the freeway. The **Model Yacht Basin** is a small basin at the south end, joined to the main lagoon by two small culverts.
4. **The railroad** as a dashed line east of the lagoon; West Berkeley and "the rest of the City" to the right.
5. **Five tide tubes** drawn as five short parallel lines through the freeway band at mid-lagoon. These are two-way: Bay water flows in on a rising tide and out on a falling tide. Their state (clean, clogged, collapsed) is the single most important control.
6. **The Strawberry Creek storm drain** entering from the right at the north end and running under University Avenue to a Bay outfall. On it, at 2nd Street, a small red square: **the weir**, a concrete crest with a 12-inch board on top, and a dashed red overflow pipe from the weir to the lagoon's north end at Addison Street. The overflow runs only when the water in the storm drain stands higher than the board. With the board gone, the crest is a foot lower and high tides also spill over it into the lagoon.
7. **The Potter Street storm drain** entering from the right at the south end, tidal, connected to the Model Yacht Basin by two culverts set about three feet above the pipe floor; large storms and high tides push water from it into the basin and on into the main lagoon.
8. **East-side street drains** (Grayson, Carleton, Parker, Dwight, Channing, Bancroft, Heinz) as short brown arrows from the City straight into the lagoon.
9. A **tide gauge** in the Bay band and a **lagoon gauge** beside the lagoon, each a vertical bar with the current level and a thin trace of the last 48 hours.
10. A **clock and calendar** (simulated day and hour) and a **weather glyph** that shows rain while a storm hydrograph is running.

Animation: water is drawn as particles. Blue particles move through the tide tubes toward the lagoon on a rising tide and toward the Bay on a falling tide, at a rate proportional to the computed flow. Red particles pour over the weir and along the overflow pipe only while the weir is spilling. Brown particles come down the east-side arrows during a storm. The lagoon's fill color shifts toward green as salinity drops. Nothing moves when nothing is flowing; that stillness is part of the story.

## 4. The numbers (fixed inputs, with sources)

All elevations in feet above MLLW (the Bay tide datum). Confidence: **High** = read from the cited document; **Moderate** = inferred; **Assumption** = chosen for this model and must be labeled as such on the page.

| Quantity | Value | Source | Confidence |
|---|---|---|---|
| Main lagoon water area | 58.3 acres (2,539,500 ft²) | APIP 2008, p. 1 and Table 1 | High |
| Mean depth of the main lagoon | 3.0 ft (slider 1.5–6) | Assumption; a June 2024 Council item says average depth "decreased by approximately 50% since 1970" | Assumption |
| Tide tubes | Five 24-inch pipes, ~250 ft long, under I-80 | APIP 2008 Table 2; Harris & Associates CCTV memo, Nov 11, 2020 | High |
| Tube condition benchmarks | 60% efficiency in 2007; "less than 10%" in 2019; repaired 2020–22 | City fact sheet, April 2022; City Manager memo, Feb 15, 2023 | High |
| Tidal exchange, existing condition | About 22 acre-feet per tidal cycle | APIP 2008, executive summary | High |
| Tidal exchange, APIP Alternative 4B | 115 acre-feet per cycle | APIP 2008, executive summary | High |
| Days to clear a 100-year storm's water | 48.5 days existing; 10.4 days with Alternative 4B | APIP 2008, executive summary | High |
| Strawberry drain at the park | 90-inch concrete pipe; overflow to the lagoon begins at about 5.5 ft of depth in the pipe | APIP 2008 Table 2 and p. 111 | High |
| Weir board | 12 inches high, redwood until Dec 10, 2019, metal since | City fact sheet, April 2022 | High |
| Weir length | 15 ft | Field notes (unpublished) | Low; label as assumption |
| Strawberry watershed | 2,022 acres | APIP 2008 Table 16 | High |
| Potter watershed | 1,995 acres | APIP 2008 Table 16 | High |
| East-side direct drainage to the lagoon | 231 acres (sub-basins 15–21) | APIP 2008 Table 16 | High |
| Share of Potter runoff reaching the lagoons | up to about 29% in a 10-year storm (68 acre-feet) | Watershed Management Plan 2012, Appendix D | Moderate |
| Bay salinity off Berkeley | 28 ppt | Assumption (central Bay, dry season) | Assumption |
| Mean tide level; semidiurnal and diurnal amplitudes | 3.2 ft; 1.9 ft (M2); 1.0 ft (K1+O1) | Assumption consistent with Berkeley tide tables (MHHW ≈ 6.0, MLLW = 0) | Assumption |

**Design storms at the park, from APIP 2008 Table 16** (24-hour events; peak flow in cfs, runoff volume in acre-feet):

| Storm | Strawberry peak | Strawberry volume | Potter peak | Potter volume | East-side peak | East-side volume |
|---|---|---|---|---|---|---|
| First flush (0.3-yr, 1.0 in) | 212 | 84.3 | 358 | 133.5 | 48 | 15.8 |
| 5-year | 883 | 394.8 | 1,396 | 511.3 | 185 | 61.3 |
| 10-year | 1,040 | 469.2 | 1,619 | 593.9 | 218 | 72.1 |
| 25-year | 1,299 | 592.3 | 1,978 | 727.9 | 265 | 91.6 |
| 100-year | 1,664 | 768.3 | 2,477 | 915.5 | 335 | 113.4 |

(East-side peak and volume are the sums of the seven direct sub-basins in Table 16.)

## 5. The model (hourly water balance)

Time step 1 hour. State variables: lagoon level `h` (ft MLLW), lagoon salinity `S` (ppt), storm-water tracer volume `F` (ft³). Lagoon area `A` is constant (prismatic lagoon). Lagoon volume `V = A × (depth + (h − 3.2))`.

**Tide.** `h_bay(t) = 3.2 + a × (1.9 sin(2πt/12.4206) + 1.0 sin(2πt/23.9345 + 1.1))`, `t` in hours, `a` the tide-amplitude slider (1.0 mean tides, 1.25 king tide).

**Tide tubes (two-way).** `Q_tube = e × K × sign(Δh) × √|Δh|` with `Δh = h_bay − h`, `e` the tube-efficiency slider (0–1), `K = 110 cfs/√ft`. K is calibrated so that `e = 0.6` at mean tides gives about 22 acre-feet of inflow per flood tide, the APIP's existing-condition figure. The Alternative 4B preset multiplies K by 3.1 to reach about 115 acre-feet per cycle.

**Potter connection (two-way, through the Model Yacht Basin).** `Q_potter_tide = p × 0.35 × K × sign(Δh) × √|Δh|`, `p` the Potter-connection slider (default 0.5).

**Strawberry storm flow.** A triangular hydrograph with the table's peak `Qp` and volume `Vs`: base `T = 2 Vs / Qp` hours, rising limb `T/3`, starting at the chosen storm hour. Depth in the 90-inch pipe: `y = 7.5 × (Q/420)^0.55` for `Q ≤ 420 cfs` (an assumed full-pipe capacity), and surcharged above that: `y = 7.5 + 2.5 × (Q − 420)/420`. Water level at the weir `= max(0.5 + y, h_bay)`; the 0.5 ft is the assumed pipe invert, and the max term is tidal backwater from the outfall.

**The weir.** Crest with board `= 7.0 ft MLLW`; without board `= 6.0` (which equals invert + 5.5 ft, the APIP overflow threshold, and is about MHHW, so without the board the higher high tides spill). `Q_weir = 3.0 × L × (level − crest)^1.5` when positive, `L = 15 ft`. If the storm flow is below 5 cfs and the Bay is above the crest, the spill is tagged as Bay water (salty); otherwise as storm water (fresh). The spill is capped at what is actually in the pipe.

**Potter storm inflow.** The Potter hydrograph times the Potter-share slider (default 0.25).

**East-side drains.** The east-side hydrograph, all of it into the lagoon.

**Evaporation.** 0.12 in/day off the lagoon surface (assumption; make it a slider under "advanced").

**Mass balance each hour.** `h += (ΣQ_in − ΣQ_out) × 3600 / A`. Salinity is perfectly mixed: salt in from tubes, Potter tide and tidal weir spill at Bay salinity; salt out with every outflow at lagoon salinity. Tracer `F` gains all fresh inflow and loses `F/V` of every outflow.

**Outputs per run.** Time series of `h_bay`, `h`, every flow, `S`, `F`. Summary numbers: inflow through the tubes per flood tide (average over the run), days to flush (from the tracer's peak until it falls below 10% of that peak), minimum salinity, peak lagoon level, cumulative acre-feet by source (tubes in, tubes out, weir storm, weir tidal, Potter tidal, Potter storm, east side).

A working reference implementation of exactly this model, in 120 lines of plain JavaScript, accompanies this spec (`aquatic-park-water-model-reference.js`). It runs in Node and in a browser. A builder may use it as is.

## 6. Scenarios (preset buttons, each sets the sliders and shows a one-line caption)

| Preset | Tubes | Board | Tide | Storm | Depth | Caption |
|---|---|---|---|---|---|---|
| 2007: the APIP baseline | 0.60 | in | mean | none | 3.0 | "Five tubes at 60%: about 22 acre-feet in and out each tide." |
| Summer 2019: tubes clogged | 0.08 | in | mean | none | 3.0 | "Under 10% efficiency: the lagoon barely breathes." |
| Fall 2019: the board is gone | 0.08 | out | king (1.25) | none | 3.0 | "With the redwood board missing, high tides pour over the crest into the lagoon." |
| December 2019: metal weir, tubes still clogged | 0.08 | in | mean | first flush | 3.0 | "The first rains bring the first-flush load into a lagoon that cannot flush it." |
| 2022: tubes repaired | 1.00 | in | mean | none | 3.0 | "Repair roughly doubles the exchange." |
| January 2023: atmospheric river | 1.00 | in | mean | 100-year | 3.0 | "Salinity crashes under 10 ppt; the sharks and rays die." |
| APIP Alternative 4B (never built) | 1.00 ×3.1 | removed | mean | 100-year | 3.0 | "115 acre-feet per cycle: storm water is gone in days, not weeks." |
| Custom | sliders free | | | | | |

For the "board removed" state in Alternative 4B, model it as crest = 4.0 ft with a gate that closes during the storm hydrograph (the APIP's slide-gate idea); simplest acceptable version: board out, and the weir tagged as two-way.

## 7. Screens and layout

Top: title "Aquatic Park: where the water comes from, where it goes," one sentence of explanation, and a row of preset buttons.

Left two-thirds: the animated plan view (Section 3). Hovering any element shows a short tooltip with what it is and today's state (for the tubes: efficiency and current flow in cfs; for the weir: board in or out, crest elevation, current spill; for the lagoon: level, salinity, volume).

Right third: the controls.
- Tube efficiency (0–100%), with tick marks at 8% ("2019"), 60% ("2007"), 100% ("repaired").
- Weir board: in / out toggle.
- Tide: mean / spring / king.
- Storm: none / first flush / 5-yr / 10-yr / 25-yr / 100-yr, and a start-day slider.
- Lagoon mean depth (1.5–6 ft).
- Advanced (collapsed): Potter share, Potter tidal connection, weir length, Bay salinity, evaporation, run length (14/30/60/90 days), playback speed.
- Play / pause / step / reset.

Below the picture, three small charts, drawn in SVG, sharing the time axis:
1. **Levels**: Bay tide (thin line) and lagoon level (bold line), ft MLLW, with the weir crest drawn as a dashed horizontal line so the viewer sees when tides top it.
2. **Flows**: stacked area of inflows by source (tubes, weir storm, weir tidal, Potter, east side) above the axis and outflows below, cfs.
3. **Salinity and storm water**: salinity in ppt (left axis) and storm-water tracer in acre-feet (right axis), with a marker at the flush point.

Four stat tiles above the charts: **Exchange per tide** (acre-feet), **Lagoon level now** (ft, with "+x in above normal"), **Salinity now** (ppt, colored), **Days to flush the storm** (or "no storm yet"). Each tile has a one-line comparison to the City's published figure where one exists (22 and 115 acre-feet; 48.5 and 10.4 days).

Footer: "What this model is and is not" (Section 9), the source list (Section 10), and a link back to `berkeley-aquatic-park.html`.

## 8. Acceptance checks (the builder's numbers must land near these)

Run each check with the reference parameters; a build is acceptable within about 15%.

| Check | Setting | Expected |
|---|---|---|
| Baseline exchange | tubes 0.60, mean tide, no storm, 14 days | ~23 acre-feet per flood tide; ~70 acre-feet/day in; no weir flow |
| Clogged tubes | tubes 0.08 | ~3 acre-feet per flood tide |
| Board missing, king tide | tubes 0.08, board out, tide 1.25 | tidal spill over the weir of ~30 acre-feet in 14 days; peak spill ~30 cfs |
| Board in, king tide | tubes 0.08, board in, tide 1.25 | zero spill |
| Repaired tubes | tubes 1.00 | ~40 acre-feet per flood tide |
| 5-year storm, repaired | tubes 1.00, storm 5-yr, 60 days | weir storm spill ~80 acre-feet, peak ~290 cfs; east side ~60 acre-feet; salinity minimum ~11 ppt; flush ~2–3 days |
| 5-year storm, 2019 tubes | tubes 0.08, storm 5-yr, 60 days | same inflows; flush ~12 days |
| 100-year storm, baseline | tubes 0.60, storm 100-yr, 90 days | weir spill ~340 acre-feet, peak ~1,000 cfs; salinity minimum ~5 ppt |
| Alternative 4B | tubes 1.00, K×3.1, storm 100-yr | ~220 acre-feet per flood tide; flush under 1 day |

Note that the simple tracer flushes far faster than the APIP's 48.5 days because the lagoon is modeled as perfectly mixed and prismatic. That is a known limitation (Section 9), and the page must say so beside the "days to flush" tile. A builder who wants to match the APIP can add a mixing-efficiency factor (default 0.15) that scales how much of each ebb is storm water; with it, baseline 100-year flush lands in the 30–50 day range.

## 9. What the model is and is not (text to show on the page)

This is a lumped water balance, not a hydraulic model. It treats the lagoon as one well-mixed box with vertical sides, the tide as two sine waves, each storm as a triangle, and the tubes as a single orifice whose size you set with a slider. It reproduces the City's published exchange figures by construction (the tube constant is calibrated to them), so it cannot independently confirm them. It does not model the Model Yacht Basin or Radio Tower Pond separately, wind, stratification, sediment, groundwater, or the east-side trash separators. The weir's crest elevation, length and the pipe invert are assumptions; the City has not published them. Use it to see how the pieces interact, not to size anything.

## 10. Sources

- Aquatic Park Improvement Program, technical report and appendices, Laurel Marcus & Associates / Hydrologic Systems Inc. for the City of Berkeley, March 2008. Tables 1, 2 and 16; pp. 20–21, 111, 145; Figure 94. https://aquaticpark.org/wp-content/uploads/2024/06/APIP_Study_2008_W_TechnicalReportAndAppendices.pdf
- City of Berkeley, "Aquatic Park Water Quality," fact sheet, April 2022. https://berkeleyca.gov/sites/default/files/2022-04/AP_Water-Quality-Information.pdf
- Harris & Associates, technical memorandum on final CCTV observations, Aquatic Park Central Tide Tubes, November 11, 2020. https://berkeleyca.gov/sites/default/files/documents/AQ%20P%20TT_Technical%20Memo%20on%20final%20CCTV%20observations.pdf
- SF Bay Regional Water Quality Control Board, Executive Officer's Report, February 5, 2020. https://www.waterboards.ca.gov/rwqcb2/board_info/agendas/2020/February/5_ssr.pdf
- City of Berkeley Watershed Management Plan (2011 Version 1.0, adopted October 30, 2012) and Appendix D (Balance Hydrologics). https://berkeleyca.gov/sites/default/files/2022-03/WatershedMgtPlan_2011October_Version1.0.pdf
- City Manager, Update on Aquatic Park, February 15, 2023. https://berkeleyca.gov/sites/default/files/documents/2023-02-15-PRW-aquatic%20park.pdf
- Council Item 37, June 25, 2024 (EPA grant; lagoon depth statement). https://berkeleyca.gov/sites/default/files/documents/2024-06-25%20Item%2037%20Accepting%20Grant%20Funds%20from%20the%20U.S.%20Environmental.pdf
- Learn About Berkeley, "Aquatic Park: The Lagoon, the Weir and the Tide Tubes," November 2026. https://jskromer.github.io/BeTH-/berkeley-aquatic-park.html

## 11. Deliverables from the builder

1. `aquatic-park-water-model.html`, single file, passing the checks in Section 8.
2. A screenshot of each preset.
3. A short note listing every constant the builder changed from this spec and why.
