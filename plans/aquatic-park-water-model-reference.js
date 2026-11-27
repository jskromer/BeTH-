/* Aquatic Park water-balance model. Learn About Berkeley, 2026.
   A lumped, hourly-step model of the main lagoon: tide tubes to the Bay, the Strawberry weir,
   the Potter connection, east-side drains, rain on the water and evaporation.
   Units: feet, square feet, cubic feet, hours. Elevations in feet above MLLW (Bay datum).
   Sources for the fixed numbers: APIP 2008 (Laurel Marcus & Assoc./Hydrologic Systems) Tables 2 and 16;
   City fact sheet April 2022; Harris & Associates CCTV memo Nov 2020. Everything else is a stated assumption. */
(function (root) {
  const ACRE = 43560;
  const STORMS = {
    none:  { label: "No storm", peakSB: 0, volSB: 0, volPot: 0, volEast: 0 },
    ff:    { label: "First flush (0.3-yr, 1.0 in / 24 h)", peakSB: 212, volSB: 84.3, volPot: 133.5, volEast: 15.8 },
    y5:    { label: "5-year, 24-hour", peakSB: 883, volSB: 394.8, volPot: 511.3, volEast: 61.3 },
    y10:   { label: "10-year, 24-hour", peakSB: 1040, volSB: 469.2, volPot: 593.9, volEast: 72.1 },
    y25:   { label: "25-year, 24-hour", peakSB: 1299, volSB: 592.3, volPot: 727.9, volEast: 91.6 },
    y100:  { label: "100-year, 24-hour", peakSB: 1664, volSB: 768.3, volPot: 915.5, volEast: 113.4 }
  };
  // east-side volumes = sum of APIP sub-basins 15-21 "Directly Entering the Lagoon" (Table 16), acre-feet.

  const DEFAULTS = {
    days: 14,
    lagoonAcres: 58.3,      // main lagoon, APIP 2008
    meanDepth: 3.0,         // ft, assumption; "average depth decreased ~50% since 1970" (Council item, June 2024)
    tubeEff: 0.6,           // 1.0 = five clean 24-in tubes; City: 60% in 2007, <10% in 2019
    tubeCal: 1.0,           // multiplier on calibrated conductance (used by the Alt 4B preset)
    potterEff: 0.5,         // fraction of a clean two-culvert tidal connection via the Model Yacht Basin
    boardIn: true,          // 12-in weir board present
    crestBoard: 7.0,        // ft MLLW, top of board; crest without board = 6.0 = invert + 5.5 ft (APIP threshold), about MHHW
    weirLen: 15,            // ft, from field notes (unverified)
    storm: "none",
    stormStartDay: 3,
    tideAmp: 1.0,           // 1.0 = mean tides; 1.25 = spring; 1.45 = king tide (~7.4 ft MLLW, NOAA 9414816, Nov 25 2026)
    potterStormFrac: 0.25,  // share of Potter runoff that reaches the lagoons (WMP: up to ~29% in a 10-yr storm)
    baySalinity: 28,        // ppt, assumption for central Bay off Berkeley
    initSalinity: 24,
    evapInPerDay: 0.12      // in/day, summer assumption
  };

  function tide(tHours, amp) {
    // Synthetic mixed semidiurnal tide, ft above MLLW. Mean level 3.2; M2 1.9 ft; K1+O1 ~1.0 ft.
    const M2 = 12.4206, K1 = 23.9345;
    return 3.2 + amp * (1.9 * Math.sin(2 * Math.PI * tHours / M2) + 1.0 * Math.sin(2 * Math.PI * tHours / K1 + 1.1));
  }

  function hydrograph(tHoursSinceStart, peak, volAcFt) {
    // Triangular hydrograph with the APIP peak and volume: base T = 2V/Qp hours, rising limb T/3.
    if (peak <= 0 || volAcFt <= 0) return 0;
    const T = 2 * volAcFt * ACRE / peak / 3600;
    if (tHoursSinceStart < 0 || tHoursSinceStart > T) return 0;
    const tr = T / 3;
    return tHoursSinceStart < tr ? peak * tHoursSinceStart / tr : peak * (T - tHoursSinceStart) / (T - tr);
  }
  // For the Potter and east-side volumes the peak is set from the APIP peaks scaled to the volume.
  const PEAK_POT = { ff: 358, y5: 1396, y10: 1619, y25: 1978, y100: 2477 }, PEAK_EAST = { ff: 48, y5: 185, y10: 218, y25: 265, y100: 335 };

  // Strawberry culvert stage near the weir: 90-in pipe (APIP). Overflow begins at ~5.5 ft of depth (APIP).
  // Depth-flow: y/D = (Q/Qfull)^0.55 up to full (approximation of a partially full circular pipe), Qfull assumed 420 cfs.
  function culvertDepth(q) {
    const D = 7.5, Qfull = 420;
    if (q <= 0) return 0.3;
    return Math.min(D + Math.max(0, (q - Qfull) / Qfull) * 2.5, D * Math.pow(q / Qfull, 0.55)); // surcharge above full
  }
  const INVERT = 0.5; // ft MLLW, assumed invert of the Strawberry pipe at the weir

  function weirFlow(headFt, len) { // broad-crested weir, cfs
    return headFt > 0 ? 3.0 * len * Math.pow(headFt, 1.5) : 0;
  }

  function run(p) {
    p = Object.assign({}, DEFAULTS, p || {});
    const dt = 1; // hour
    const n = Math.round(p.days * 24 / dt);
    const A = p.lagoonAcres * ACRE;
    const storm = STORMS[p.storm] || STORMS.none;
    const crest = p.boardIn ? p.crestBoard : p.crestBoard - 1.0;
    // Tube conductance K (cfs per sqrt(ft)): calibrated so eff=0.6 at mean tide gives ~22 ac-ft per tidal cycle (APIP existing condition).
    const K = 110 * p.tubeCal;
    let h = tide(0, p.tideAmp); // lagoon starts at bay level
    let S = p.initSalinity; let F = 0; // F = storm-water (tracer) volume in the lagoon, cf
    let V = A * p.meanDepth; // reference volume at mean depth; stage changes modify it
    const out = { t: [], bay: [], lagoon: [], qTube: [], qWeir: [], qPotter: [], qEast: [], sal: [], storm: [], tracer: [], cum: { tubeIn: 0, tubeOut: 0, weir: 0, weirTide: 0, potterTide: 0, potterStorm: 0, east: 0 }, exchangePerCycle: 0 };
    let cycleIn = 0, cycles = 0, lastSign = 0;
    for (let i = 0; i <= n; i++) {
      const t = i * dt;
      const hb = tide(t, p.tideAmp);
      const vol = A * (p.meanDepth + (h - 3.2));
      // 1. tide tubes (bidirectional)
      const dh = hb - h;
      const qT = p.tubeEff * K * Math.sign(dh) * Math.sqrt(Math.abs(dh));
      // 2. Potter connection via MYB (bidirectional, smaller)
      const qP = p.potterEff * 0.35 * K * Math.sign(dh) * Math.sqrt(Math.abs(dh));
      // 3. Strawberry storm flow and weir
      const ts = t - p.stormStartDay * 24;
      const qSB = hydrograph(ts, storm.peakSB, storm.volSB);
      const stage = Math.max(INVERT + culvertDepth(qSB), hb); // tidal backwater near the outfall
      const head = stage - crest;
      let qW = weirFlow(head, p.weirLen);
      qW = Math.min(qW, qSB + (hb > crest ? weirFlow(hb - crest, p.weirLen) : 0)); // cannot spill more than is there
      const weirIsTidal = qSB < 5 && hb > crest;
      // 4. Potter storm inflow and east-side drains (fresh)
      const qPS = hydrograph(ts, PEAK_POT[p.storm] || 0, storm.volPot) * p.potterStormFrac;
      const qE = hydrograph(ts, PEAK_EAST[p.storm] || 0, storm.volEast);
      // 5. rain on the lagoon / evaporation
      const qEvap = -(p.evapInPerDay / 12 / 24) * A / 3600;
      const qIn = qT + qP + qW + qPS + qE + qEvap;
      // salinity mixing (perfectly mixed)
      const inSalt = (Math.max(qT, 0) + Math.max(qP, 0)) * p.baySalinity * 3600 + qW * 3600 * (weirIsTidal ? p.baySalinity : 0);
      const inVol = (Math.max(qT, 0) + Math.max(qP, 0) + qW + qPS + qE) * 3600;
      const outVol = (Math.max(-qT, 0) + Math.max(-qP, 0)) * 3600;
      const salt = S * vol + inSalt - S * outVol;
      const freshIn = (qW * (weirIsTidal ? 0 : 1) + qPS + qE) * 3600; F = Math.max(0, F + freshIn - (F / vol) * outVol);
      const newVol = vol + qIn * 3600;
      S = Math.max(0, salt / newVol);
      h = h + qIn * 3600 / A;
      // bookkeeping
      out.t.push(t); out.bay.push(hb); out.lagoon.push(h); out.qTube.push(qT); out.qWeir.push(qW); out.qPotter.push(qP + qPS); out.qEast.push(qE); out.sal.push(S); out.storm.push(qSB); out.tracer.push(F / ACRE);
      const c = out.cum, k = 3600 / ACRE;
      if (qT > 0) c.tubeIn += qT * k; else c.tubeOut += -qT * k;
      if (weirIsTidal) c.weirTide += qW * k; else c.weir += qW * k;
      if (qP > 0) c.potterTide += qP * k;
      c.potterStorm += qPS * k; c.east += qE * k;
      // exchange per cycle: volume in through tubes during each flood
      const sgn = Math.sign(qT);
      if (sgn > 0) cycleIn += qT * k;
      if (lastSign > 0 && sgn <= 0) { cycles++; out.exchangePerCycle = cycleIn; cycleIn = 0; }
      lastSign = sgn;
    }
    // residence time: lagoon volume / mean daily tidal inflow
    const meanDailyIn = out.cum.tubeIn / p.days + out.cum.potterTide / p.days;
    out.residenceDays = meanDailyIn > 0 ? (A * p.meanDepth / ACRE) / meanDailyIn : Infinity;
    out.params = p; out.crest = crest; out.stormDef = storm;
    // days to flush: from peak tracer volume until it falls below 10% of the peak
    let pk = 0, ipk = 0; out.tracer.forEach((v, i) => { if (v > pk) { pk = v; ipk = i; } });
    out.flushDays = null;
    if (pk > 0) { for (let i = ipk; i < out.tracer.length; i++) { if (out.tracer[i] < 0.1 * pk) { out.flushDays = (i - ipk) / 24; break; } } }
    out.tracerPeak = pk;
    return out;
  }
  const api = { run, STORMS, DEFAULTS, tide };
  if (typeof module !== "undefined") module.exports = api; else root.APModel = api;
})(typeof window !== "undefined" ? window : globalThis);
