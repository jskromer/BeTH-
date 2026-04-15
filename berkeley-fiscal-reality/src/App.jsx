import { useState, useEffect, useRef } from "react";
import CarryoverTracker from "./CarryoverTracker";

/* ──────────────────── shared helpers ──────────────────── */
const fmt = (n) => (n >= 1000 ? `$${(n / 1000).toFixed(1)}B` : `$${n}M`);

function StatBlock({ value, label, sub, color = "#c41e1e" }) {
  return (
    <div className="stat-block">
      <div style={{ fontSize: "clamp(24px,5vw,36px)", fontWeight: 900, color, letterSpacing: "-1px", lineHeight: 1.1, fontFamily: "'JetBrains Mono', monospace" }}>{value}</div>
      <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "1.5px", marginTop: 6, color: "#1a1a1a" }}>{label}</div>
      {sub && <div style={{ fontSize: 10, color: "#888", marginTop: 3 }}>{sub}</div>}
    </div>
  );
}

function Bar({ label, value, max, color = "#c41e1e", funded, suffix = " unfunded" }) {
  const pct = (value / max) * 100;
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 600, marginBottom: 4, flexWrap: "wrap", gap: 4 }}>
        <span>{label}</span>
        <span style={{ color: "#666", fontFamily: "'JetBrains Mono', monospace", fontSize: 10 }}>
          ${value}M{suffix}
          {funded !== undefined && (
            <span style={{ marginLeft: 6, color: funded < 20 ? "#c41e1e" : funded < 50 ? "#d4860b" : "#666", fontWeight: 700 }}>
              ({funded}% funded)
            </span>
          )}
        </span>
      </div>
      <div style={{ height: 8, background: "#e8e4df", borderRadius: 2, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${Math.min(pct, 100)}%`, background: color, borderRadius: 2, transition: "width 0.8s cubic-bezier(.22,1,.36,1)" }} />
      </div>
    </div>
  );
}

// Bar where width = % funded; right label = unfunded % + $ amount
function FundingBar({ label, funded, unfundedDollars, color = "#d4860b" }) {
  const unfundedPct = (100 - funded).toFixed(1);
  const labelColor = funded < 20 ? "#c41e1e" : funded < 50 ? "#d4860b" : "#555";
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 600, marginBottom: 4, flexWrap: "wrap", gap: 4 }}>
        <span>{label}</span>
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "#666" }}>
          <span style={{ color: labelColor, fontWeight: 700 }}>{unfundedPct}% unfunded</span>
          {unfundedDollars !== undefined && (
            <span style={{ marginLeft: 6 }}>(${unfundedDollars}M gap)</span>
          )}
        </span>
      </div>
      <div style={{ height: 8, background: "#e8e4df", borderRadius: 2, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${funded}%`, background: color, borderRadius: 2, transition: "width 0.8s cubic-bezier(.22,1,.36,1)" }} />
      </div>
    </div>
  );
}

function SolutionRow({ title, savings, detail, urgency }) {
  const colors = { high: "#c41e1e", medium: "#d4860b", low: "#2a7d4f" };
  const labels = { high: "IMMEDIATE", medium: "NEAR-TERM", low: "STRUCTURAL" };
  return (
    <div style={{
      padding: "14px 16px", background: "#faf8f5",
      borderLeft: `4px solid ${colors[urgency] || "#999"}`,
      marginBottom: 10, borderRadius: "0 6px 6px 0",
      transition: "transform 0.15s", cursor: "default"
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: 8 }}>
        <span style={{ fontWeight: 700, fontSize: 14 }}>{title}</span>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            fontSize: 9, fontWeight: 800, letterSpacing: "1px", padding: "2px 8px",
            background: colors[urgency] + "18", color: colors[urgency], borderRadius: 3
          }}>{labels[urgency]}</span>
          <span style={{ fontWeight: 800, fontSize: 15, color: "#2a7d4f", fontFamily: "'JetBrains Mono', monospace", whiteSpace: "nowrap" }}>{savings}</span>
        </div>
      </div>
      <div style={{ fontSize: 12, color: "#555", marginTop: 6, lineHeight: 1.65 }}>{detail}</div>
    </div>
  );
}

function Callout({ children, type = "danger" }) {
  const styles = {
    danger: { bg: "#fdf0f0", border: "#e8c4c4", accent: "#8b0000" },
    warning: { bg: "#fdf6e8", border: "#e8d6a8", accent: "#8b6914" },
    success: { bg: "#edf7f0", border: "#b8dcc4", accent: "#2a7d4f" },
    dark: { bg: "#1a1a1a", border: "#333", accent: "#6fc97f" },
  };
  const s = styles[type];
  return (
    <div style={{
      marginTop: 20, padding: "16px 18px",
      background: s.bg, border: `1px solid ${s.border}`,
      borderRadius: 6, fontSize: 13, lineHeight: 1.65,
      color: type === "dark" ? "#fffdf9" : "#333"
    }}>
      {children}
    </div>
  );
}

/* ──────────────────── SECTIONS ──────────────────── */
const TABS = [
  { key: "shellgame", label: "THE SHELL GAME" },
  { key: "numbers",   label: "THE NUMBERS" },
  { key: "record",    label: "AUDIT RECORD" },
  { key: "aao",       label: "AAO TRACKER" },
  { key: "demands",   label: "DEMANDS" },
  { key: "compare",   label: "COMPARISONS" },
];

function ShellGameSection() {
  const cycle = [
    { n: "1", title: "Overappropriate", body: "Council adopts a budget with more spending authority than departments can realistically execute. Every program gets funded on paper — politically convenient, fiscally misleading." },
    { n: "2", title: "Underspend", body: "Departments spend 80–90% of their appropriations. The remaining 10–20% sits unencumbered at year-end — money that was never going to be spent." },
    { n: "3", title: "Roll It Forward", body: "Every November, AAO #1 quietly carries unspent amounts into the new fiscal year as 'carryovers' and 'encumbrances.' No public hearing. Typically passed on the consent calendar." },
    { n: "4", title: "Build the Shadow Reserve", body: "Over three years, $316M in unspent carryovers and $367M in encumbrances have rolled forward — a massive pool of appropriated money outside normal General Fund accounting." },
    { n: "5", title: "Raid When Needed", body: "When the structural deficit appears, the City taps these pools — plus dedicated funds like the pension trust, Workers' Comp, and IT reserves — to declare the budget 'balanced.'" },
    { n: "6", title: "Ask Voters for More", body: "With the budget technically balanced, the City tells voters there's a $33M crisis requiring a new sales tax. The shadow reserves, the fund raids, the ignored audit recommendations — none of it disclosed in plain language." },
  ];

  const patches = [
    { source: "Section 115 Pension Trust", amount: 6.0, note: "Established to pre-fund pension obligations — not for operations" },
    { source: "IT Cost Allocation Fund", amount: 6.2, note: "Internal service fund. One-time transfer to plug GF gap" },
    { source: "Workers' Compensation Fund", amount: 5.2, note: "Reserve for employee injury claims — not a budget tool" },
    { source: "Measure U1 Funds", amount: 2.5, note: "Voter-approved for specific purposes" },
    { source: "44.4 Vacant Positions Left Unfunded", amount: null, note: "~$8–10M est. Deferred hiring, not structural savings" },
    { source: "11.8 GF Positions Moved to Other Funds", amount: null, note: "~$2–3M est. Cost-shifting, not cost-cutting" },
  ];

  const legalPoints = [
    {
      label: "City Fiscal Policy #5 — VIOLATED",
      quote: "\"Primarily allocating one-time revenue for one-time expenditures\"",
      detail: "The Section 115 Trust and Workers' Comp fund are being used for recurring operating gaps. That is precisely the definition of one-time money for ongoing costs.",
      color: "#c41e1e",
    },
    {
      label: "City Fiscal Policy #6 — UNRESOLVED (2 AUDITS)",
      quote: "\"Enterprise and grant funds to balance and new programs to pay for themselves\"",
      detail: "Both the 2022 and 2026 City Auditor reports flag enterprise fund shortfalls as unresolved. The City simply repeated the recommendation. Nothing changed.",
      color: "#c41e1e",
    },
    {
      label: "Section 115 Trust Instrument — LEGAL QUESTION",
      quote: "Council Resolution establishing trust for pension pre-funding",
      detail: "Withdrawing $3M (FY25) and $6M (FY26) for operating expenses may violate the trust's stated purpose. The 2022 audit specifically warned against this. A formal legal opinion is warranted.",
      color: "#d4860b",
    },
    {
      label: "Prop 218 (CA Constitution) — ETHICAL QUESTION",
      quote: "Voter approval required; voters must be accurately informed",
      detail: "Asking voters for a new sales tax while concealing that the 'balanced' budget required raiding the pension fund may misrepresent the true fiscal picture to voters whose approval is constitutionally required.",
      color: "#d4860b",
    },
  ];

  return (
    <>
      <SectionTitle color="#c41e1e">THE SHELL GAME</SectionTitle>
      <p style={{ fontSize: 14, lineHeight: 1.7, marginBottom: 24, color: "#333", fontWeight: 600 }}>
        Berkeley has a $33M structural deficit. The City wants a new 0.5% sales tax (~$10M/yr) and a $300M bond (~$20M/yr debt service).
        Before voters decide, they should understand how the City has been "balancing" its budget for the past three years.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px,1fr))", border: "2px solid #1a1a1a", borderRadius: 8, overflow: "hidden", marginBottom: 28 }}>
        {[
          { value: "~$20M", label: "FY26 Fund Raids", sub: "Used to fake a 'balanced' budget", color: "#c41e1e" },
          { value: "$316M", label: "Carryovers Rolled", sub: "All funds FY24–26 ($32M GF portion)", color: "#c41e1e" },
          { value: "$33M", label: "Stated Deficit", sub: "What voters are being told", color: "#1a1a1a" },
          { value: "0 of 5", label: "Audit Recs Resolved", sub: "Four years, no action", color: "#8b0000" },
        ].map((s, i, arr) => (
          <div key={i} style={{ padding: "16px 12px", background: "#faf8f5", borderRight: i < arr.length - 1 ? "1px solid #e0dcd6" : "none", textAlign: "center" }}>
            <StatBlock {...s} />
          </div>
        ))}
      </div>

      <SubHead>How the Cycle Works — Six Steps</SubHead>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px,1fr))", gap: 10, marginBottom: 28 }}>
        {cycle.map((step) => (
          <div key={step.n} style={{ padding: "14px 16px", background: "#faf8f5", borderLeft: "3px solid #c41e1e", borderRadius: "0 6px 6px 0" }}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 6 }}>
              <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 900, fontSize: 20, color: "#c41e1e", lineHeight: 1 }}>{step.n}</span>
              <span style={{ fontWeight: 800, fontSize: 13 }}>{step.title}</span>
            </div>
            <p style={{ fontSize: 12, lineHeight: 1.65, color: "#555", margin: 0 }}>{step.body}</p>
          </div>
        ))}
      </div>

      {/* ── Household Analogy Sidebar ── */}
      <div style={{
        background: "#fffbf0", border: "1px solid #e8d6a8", borderLeft: "4px solid #d4860b",
        borderRadius: "0 8px 8px 0", padding: "18px 20px", marginBottom: 28
      }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "2px", color: "#d4860b", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10 }}>
          📋 HOW TO FOLLOW THE MONEY — A HOUSEHOLD ANALOGY
        </div>
        <p style={{ fontSize: 13, fontWeight: 700, margin: "0 0 12px", color: "#1a1a1a" }}>
          Imagine your household earns $10,000/month and budgets $10,000 in expenses.
          You actually only spend $8,500. Here's what Berkeley does with that $1,500:
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px,1fr))", gap: 10, marginBottom: 14 }}>
          {[
            { step: "What a normal household does", desc: "Note the $1,500 surplus. Put it in savings or reduce next month's budget.", color: "#2a7d4f" },
            { step: "What Berkeley does", desc: "Quietly roll that $1,500 into next month as extra spending authority — on top of the new $10,000 budget. Don't mention it.", color: "#c41e1e" },
          ].map((item, i) => (
            <div key={i} style={{ background: i === 0 ? "#edf7f0" : "#fdf0f0", borderRadius: 6, padding: "12px 14px", border: `1px solid ${i === 0 ? "#b8dcc4" : "#e8c4c4"}` }}>
              <div style={{ fontSize: 10, fontWeight: 800, color: item.color, letterSpacing: "1px", marginBottom: 6, fontFamily: "'JetBrains Mono', monospace" }}>{item.step.toUpperCase()}</div>
              <div style={{ fontSize: 12, lineHeight: 1.65, color: "#333" }}>{item.desc}</div>
            </div>
          ))}
        </div>
        <p style={{ fontSize: 12, lineHeight: 1.75, color: "#555", margin: "0 0 10px" }}>
          Do that for three years and you've built a hidden pool of carry-forward money — tens of thousands of dollars
          that doesn't show up in your stated monthly budget. Then one month you tell your spouse:
          <em> "We have a $1,500 monthly deficit. We need you to get a second job."</em>
          But you never mentioned the hidden pool. <strong style={{ color: "#c41e1e" }}>That's the AAO.</strong>
        </p>
        <div style={{ background: "#fff8e8", borderRadius: 6, padding: "10px 14px", border: "1px solid #e8d6a8" }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#8b6914", marginBottom: 5 }}>On the numbers: All Funds vs. General Fund</div>
          <p style={{ fontSize: 12, lineHeight: 1.7, margin: 0, color: "#555" }}>
            The $316M carryover figure covers <strong>all city funds</strong> — including capital projects, enterprise funds,
            and grants that legitimately span multiple years (think: a road project that takes 3 years to finish).
            The <strong>General Fund</strong> portion — the operating budget that pays for day-to-day city services — is
            about <strong>$32M</strong> in carryovers over three years. Both numbers matter:
            the $32M shows the operating pattern; the $316M shows the scale of a system
            that moves hundreds of millions with minimal public scrutiny.
          </p>
        </div>
      </div>

      <SubHead>FY 2026: How "Balanced" Was Actually Achieved</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 12, lineHeight: 1.6 }}>
        The City's own ACFR (Annual Comprehensive Financial Report, FY2025, pp. v–xix) openly admits the FY26 budget
        is balanced only through one-time measures. Here is what that means in plain language:
      </p>
      <div style={{ border: "2px solid #e8c4c4", borderRadius: 6, overflow: "hidden", marginBottom: 20 }}>
        <div style={{ background: "#8b0000", color: "#fff", padding: "9px 14px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 10, fontWeight: 800, letterSpacing: "1.5px", fontFamily: "'JetBrains Mono', monospace" }}>THE FY26 PATCH KIT</span>
          <span style={{ fontSize: 10, fontWeight: 800, fontFamily: "'JetBrains Mono', monospace" }}>~$20M IN ONE-TIME FIXES</span>
        </div>
        {patches.map((item, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8, padding: "10px 14px", borderBottom: i < patches.length - 1 ? "1px solid #e8e4df" : "none", background: i % 2 === 0 ? "#fdf8f8" : "#fff" }}>
            <div>
              <span style={{ fontWeight: 700, fontSize: 12 }}>{item.source}</span>
              <span style={{ fontSize: 11, color: "#888", display: "block", marginTop: 2 }}>{item.note}</span>
            </div>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 800, fontSize: 13, color: "#c41e1e", whiteSpace: "nowrap" }}>
              {item.amount ? `$${item.amount}M` : "~est."}
            </span>
          </div>
        ))}
      </div>

      <SubHead>Three Years of Rolling Unspent Money (All Funds)</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        Each November, AAO#1 carries unspent prior-year appropriations into the new fiscal year across <em>all</em> city funds.
        The <strong style={{ color: "#c41e1e" }}>red bars</strong> are true unspent carryovers.
        The <strong style={{ color: "#d4860b" }}>amber bars</strong> are encumbrances — money contracted but not yet paid.
        The gray bars are new mid-cycle adjustments. General Fund carryovers specifically: $13.5M (FY24), $13.2M (FY25), $5.4M (FY26).
        Use the <strong>AAO TRACKER</strong> tab to drill into every line item.
      </p>
      {[
        { fy: "FY2024", carryover: 85.0, encumbered: 111.2, adjustments: 53.7 },
        { fy: "FY2025", carryover: 137.7, encumbered: 111.1, adjustments: 42.3 },
        { fy: "FY2026", carryover: 93.3, encumbered: 145.2, adjustments: 135.8 },
      ].map(row => {
        const maxVal = 375;
        const bars = [
          { label: "Unspent Carryovers", value: row.carryover, color: "#c41e1e" },
          { label: "Encumbrances (committed, unpaid)", value: row.encumbered, color: "#d4860b" },
          { label: "New Mid-Cycle Adjustments", value: row.adjustments, color: "#aaa" },
        ];
        return (
          <div key={row.fy} style={{ marginBottom: 18 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 700, marginBottom: 6 }}>
              <span style={{ fontFamily: "'JetBrains Mono', monospace" }}>{row.fy} AAO#1</span>
              <span style={{ color: "#666" }}>Total all funds: ${(row.carryover + row.encumbered + row.adjustments).toFixed(1)}M</span>
            </div>
            {bars.map(bar => (
              <div key={bar.label} style={{ marginBottom: 5 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, marginBottom: 2 }}>
                  <span style={{ color: "#666" }}>{bar.label}</span>
                  <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 700, color: bar.color }}>${bar.value}M</span>
                </div>
                <div style={{ height: 7, background: "#e8e4df", borderRadius: 2 }}>
                  <div style={{ height: "100%", width: `${(bar.value / maxVal) * 100}%`, background: bar.color, borderRadius: 2, transition: "width 0.8s ease" }} />
                </div>
              </div>
            ))}
          </div>
        );
      })}

      <SubHead>The Legal and Ethical Questions</SubHead>
      {legalPoints.map((v, i) => (
        <div key={i} style={{ marginBottom: 10, padding: "13px 15px", background: "#faf8f5", border: `1px solid ${v.color}44`, borderLeft: `4px solid ${v.color}`, borderRadius: "0 6px 6px 0" }}>
          <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "1px", color: v.color, fontFamily: "'JetBrains Mono', monospace", marginBottom: 5 }}>{v.label}</div>
          <div style={{ fontSize: 12, fontStyle: "italic", color: "#555", marginBottom: 6 }}>{v.quote}</div>
          <div style={{ fontSize: 12, color: "#333", lineHeight: 1.65 }}>{v.detail}</div>
        </div>
      ))}

      <Callout type="dark">
        <div style={{ fontWeight: 800, fontSize: 14, marginBottom: 8, color: "#c41e1e" }}>What Isn't Being Disclosed</div>
        AAO amendments go to Council on the consent calendar — no public hearing, no plain-language summary of cumulative
        carryover patterns. Fund raids are mentioned in ACFR footnotes. No budget document tells Berkeley residents that their
        city's "balanced" FY26 budget required raiding the pension savings account, the workers' injury fund, and voter-restricted Measure U1 money.
        <div style={{ marginTop: 10, fontWeight: 700, fontSize: 13, color: "#6fc97f" }}>
          Before asking for a new tax, voters deserve a clear answer: where did the money go?
        </div>
      </Callout>
    </>
  );
}

function NumbersSection() {
  return (
    <>
      <SectionTitle color="#c41e1e">THE NUMBERS</SectionTitle>
      <p style={{ fontSize: 14, lineHeight: 1.7, marginBottom: 24, color: "#333", fontWeight: 600 }}>
        The City of Berkeley is not broke. It manages over <strong>$700M/year</strong> in total revenues and sits on
        hundreds of millions in fund balances. The problem is not a lack of money —
        it's how the money is allocated, hidden, and misrepresented.
      </p>

      {/* ── Excess Equity Explainer ── */}
      <div style={{ background: "#1a1a1a", color: "#fffdf9", padding: "18px 20px", borderRadius: 8, marginBottom: 24 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "2px", color: "#c41e1e", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10 }}>
          KEY CONCEPT: EXCESS EQUITY
        </div>
        <p style={{ fontSize: 13, lineHeight: 1.75, margin: 0, color: "#e8e4df" }}>
          <strong style={{ color: "#fff" }}>Excess equity</strong> is what happens when internal service funds and enterprise funds accumulate
          balances far beyond what they actually need as reserves. Berkeley's IT Cost Allocation Fund, Workers' Compensation Fund,
          and other internal accounts had built up surpluses — money sitting idle, far exceeding their stated reserve targets.
          When the General Fund deficit appeared, the City quietly tapped these pools. <strong style={{ color: "#6fc97f" }}>This is not fiscal management.
          It is a one-time fix that destroys the cushion those funds were built to provide.</strong> And it is precisely how
          a city can claim a deficit while actually sitting on a hidden pile of cash.
        </p>
        <div style={{ marginTop: 14, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 10 }}>
          {[
            { label: "IT Fund Equity Tapped", value: "$6.2M", note: "Excess balance swept to GF" },
            { label: "Workers' Comp Equity Tapped", value: "$5.2M", note: "Reserve above target, raided" },
            { label: "Pension Trust Equity Tapped", value: "$6.0M", note: "Violated its own stated purpose" },
            { label: "Measure U1 Equity Used", value: "$2.5M", note: "Voter-restricted funds repurposed" },
          ].map((item, i) => (
            <div key={i} style={{ background: "#2a2a2a", borderRadius: 6, padding: "10px 12px" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#c41e1e", fontFamily: "'JetBrains Mono', monospace" }}>{item.value}</div>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#fff", marginTop: 3 }}>{item.label}</div>
              <div style={{ fontSize: 10, color: "#888", marginTop: 2 }}>{item.note}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── ACFR Key Numbers ── */}
      <SubHead>What the Audited Books Actually Show (FY2025 ACFR)</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The City's own Annual Comprehensive Financial Report — audited, not estimated — tells the real story.
        Liabilities are enormous, but so are revenues. The mismatch is mismanagement, not underfunding.
      </p>
      <DataTable
        headers={["Metric", "FY 2025 (Audited)", "FY 2024", "Direction"]}
        rows={[
          ["Total Government Revenue", "$703M+", "—", { v: "Berkeley is not poor", c: "#2a7d4f" }],
          ["Property Tax Revenue", "$148.4M", "$135.7M", { v: "▲ +9% YoY", c: "#2a7d4f" }],
          ["General Fund Revenue", "$268M", "$262M", { v: "Essentially flat 3 yrs", c: "#d4860b" }],
          ["General Fund Expenditure", "$295M", "$274M", { v: "▲ +7.7% YoY", c: "#c41e1e" }],
          ["Stated Structural Deficit", "$27–33M", "—", { v: "Recurring, not one-time", c: "#c41e1e" }],
          ["Net Pension Liability", "$686.4M", "$723.8M", { v: "▼ improved slightly", c: "#d4860b" }],
          ["Net OPEB Liability", "$43.2M", "$83.4M", { v: "▼ improved (restructuring)", c: "#2a7d4f" }],
          ["Unrestricted Net Position", "−$415.2M", "−$400.4M", { v: "▲ Getting worse", c: "#c41e1e" }],
          ["Health & Welfare Expenses", "$54.8M", "$44.5M", { v: "▲ +23% in one year", c: "#c41e1e" }],
          ["Stability Reserve", "$32.8M", "—", { v: "19.5% of GF (target: 25%)", c: "#d4860b" }],
        ]}
      />
      <div style={{ fontSize: 11, color: "#999", marginTop: 6, fontStyle: "italic", marginBottom: 20 }}>
        Source: City of Berkeley ACFR FY2025 (year ended June 30, 2025). City Auditor Jenny Wong, "Berkeley's Financial Condition FY2016–2025" (2026).
      </div>

      {/* ── Revenue vs Expenditure ── */}
      <SubHead>Revenue vs. Expenditure — It's a Spending Problem</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        General Fund revenue has been <strong>essentially flat for three years</strong> — it actually declined from $273M in FY23 to $262M in FY24.
        The deficit is not a revenue shortfall. It is a cost structure that grows automatically regardless of what comes in.
      </p>
      <DataTable
        headers={["", "FY23", "FY24", "FY25", "FY26", "FY27"]}
        rows={[
          ["GF Revenue", "$273M", "$262M", "$262M", "$268M", "$273M"],
          ["GF Expenditure", "$276M", "$274M", "$294M", "$295M", "$300M"],
          [{ v: "Annual Gap", bold: true }, { v: "−$3M", c: "#c41e1e" }, { v: "−$12M", c: "#c41e1e" }, { v: "−$32M", c: "#c41e1e" }, { v: "−$27M", c: "#c41e1e" }, { v: "−$27M", c: "#c41e1e" }],
        ]}
      />

      {/* ── Personnel Spiral ── */}
      <SubHead>Where the Spending Goes: The Personnel Cost Spiral</SubHead>
      <p style={{ fontSize: 13, lineHeight: 1.7, marginBottom: 16, color: "#444" }}>
        Even with <strong>zero raises</strong>, total personnel costs will rise from $342M to <strong>$487M</strong> over
        the next decade — a $145M automatic increase driven entirely by benefit cost growth.
        The fringe rate (benefits as a % of payroll) balloons from 65% to <strong>134%</strong>.
      </p>
      <DataTable
        headers={["Cost Driver", "FY2024", "FY2034 (proj.)", "Δ Change"]}
        rows={[
          ["Base Payroll (held flat)", "$208M", "$208M", { v: "$0 change", c: "#333" }],
          ["  ↳ Health Premiums", "$31M", "$96M", { v: "+$65M", c: "#c41e1e" }],
          ["  ↳ CalPERS Employer Contribution", "$78M", "$130M", { v: "+$52M", c: "#c41e1e" }],
          ["Total Benefits", "$134M", "$279M", { v: "+$145M", c: "#c41e1e" }],
          ["Total Personnel", "$342M", "$487M", { v: "+42% auto-growth", c: "#c41e1e" }],
          ["Fringe Rate (benefits/payroll)", "65%", "134%", { v: "+69 pts", c: "#c41e1e" }],
        ]}
      />

      <Callout type="dark">
        <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 10, color: "#6fc97f" }}>
          Berkeley Has the Money. It Doesn't Manage It Well.
        </div>
        <p style={{ margin: "0 0 10px", fontSize: 13, lineHeight: 1.7, color: "#e8e4df" }}>
          Property tax revenue grew 9% in one year. Total city revenues exceed $700M. The General Fund collects $268M annually.
          Meanwhile, $316M in unspent appropriations rolled forward through the AAO process over three years.
          Internal service funds accumulated excess equity and were raided when the deficit appeared.
        </p>
        <p style={{ margin: 0, fontSize: 13, lineHeight: 1.7, color: "#e8e4df" }}>
          <strong style={{ color: "#c41e1e" }}>The deficit is real — but it is self-inflicted.</strong> It results from a cost
          structure that was never disciplined, benefit promises that were never funded, and an appropriation process
          that was never transparent. Asking voters for a new tax before fixing any of that is not fiscal management.
          It is the same shell game, one more time.
        </p>
      </Callout>
    </>
  );
}

function DemandsSection() {
  const demands = [
    {
      n: "01",
      title: "Vote NO on the November 2026 Sales Tax",
      color: "#8b0000",
      body: "A 0.5% sales tax is regressive — it hits low-income residents hardest. Before asking for new revenue, the City must demonstrate it has exhausted internal reform. It has not. The structural deficit was created by management choices, not by insufficient taxation.",
      tag: "BALLOT MEASURE",
    },
    {
      n: "02",
      title: "Vote NO on the $300M Bond",
      color: "#8b0000",
      body: "Berkeley's unfunded capital need grew from $1.2B (2022) to $1.8B (2026) — $600M worse in three years — despite Measure FF passing. Bonding more does not fix a maintenance and management failure. Debt service will crowd out the operating budget further.",
      tag: "BALLOT MEASURE",
    },
    {
      n: "03",
      title: "Require a Full AAO Transparency Report Before Any Tax Vote",
      color: "#c41e1e",
      body: "Council must publish a plain-language accounting of every AAO carryover from FY2024–2026 before placing any measure on the ballot. Voters cannot give informed consent under Prop 218 if the City conceals how it actually manages appropriations.",
      tag: "TRANSPARENCY",
    },
    {
      n: "04",
      title: "Stop Paying Employees' 8% Pension Contribution",
      color: "#c41e1e",
      body: "Berkeley covers the employee's own statutory pension share — a negotiated perk that costs taxpayers ~$16–17M/year. No peer city does this. Classic employees pay nothing toward their own pension. This single reform closes more than half the deficit.",
      tag: "COST REFORM",
    },
    {
      n: "05",
      title: "Restore the Section 115 Trust — and Stop Raiding It",
      color: "#d4860b",
      body: "The City withdrew $3M in FY25 and $6M in FY26 from the pension pre-funding trust to close the operating gap. The 2022 audit warned explicitly against this. Council must pass a resolution banning further operational use of the trust and commit to restoring the $9M withdrawn.",
      tag: "FIDUCIARY DUTY",
    },
    {
      n: "06",
      title: "Publish Excess Equity Balances for All Internal Service Funds",
      color: "#d4860b",
      body: "IT Cost Allocation, Workers' Compensation, and other internal funds accumulated excess equity above their reserve targets — and that equity was swept to balance the General Fund. Council must disclose these balances annually, explain variances from targets, and prohibit transfers that exceed defined thresholds without a public vote.",
      tag: "TRANSPARENCY",
    },
    {
      n: "07",
      title: "Implement All Five 2022 Audit Recommendations — Now",
      color: "#d4860b",
      body: "The City Auditor issued five specific recommendations in 2022. Zero were fully resolved by 2026. Council must assign a named staff member accountable for each recommendation, set a 90-day compliance deadline, and report publicly on implementation status quarterly.",
      tag: "ACCOUNTABILITY",
    },
    {
      n: "08",
      title: "Freeze Non-Essential Hiring Until Deficit Is Closed",
      color: "#1a1a1a",
      body: "Berkeley has 44.4 vacant positions left unfunded in FY26 to save ~$8–10M. This confirms positions exist that the City itself doesn't believe are needed. Formalize that freeze as policy and do not backfill vacancies in administrative roles until the structural deficit is eliminated.",
      tag: "FISCAL DISCIPLINE",
    },
  ];

  const tagColors = {
    "BALLOT MEASURE": "#8b0000",
    "TRANSPARENCY": "#1a4a8b",
    "COST REFORM": "#c41e1e",
    "FIDUCIARY DUTY": "#c41e1e",
    "ACCOUNTABILITY": "#d4860b",
    "FISCAL DISCIPLINE": "#1a1a1a",
  };

  return (
    <>
      <SectionTitle color="#c41e1e">DEMANDS</SectionTitle>

      {/* ── Anti-tax 2026 Banner ── */}
      <div style={{ background: "#8b0000", color: "#fff", padding: "20px 22px", borderRadius: 8, marginBottom: 28 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "3px", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10, color: "#ffaaaa" }}>
          THE CASE AGAINST NEW TAXES IN 2026
        </div>
        <p style={{ fontSize: 15, fontWeight: 700, lineHeight: 1.65, margin: "0 0 12px", color: "#fff" }}>
          The City of Berkeley has the money. It doesn't manage it well. And it lies — by omission — about how it uses the money it has,
          hiding hundreds of millions in the AAO process while asking voters for more.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 10 }}>
          {[
            { label: "Revenue > $700M/yr", note: "City is not underfunded" },
            { label: "$316M Rolled Forward", note: "Unspent money the City 'forgot' to tell you about" },
            { label: "~$20M Fund Raids", note: "Excess equity swept to fake a balanced budget" },
            { label: "0 of 5 Audit Recs", note: "Not one implemented in four years" },
          ].map((item, i) => (
            <div key={i} style={{ background: "rgba(255,255,255,0.1)", borderRadius: 6, padding: "10px 12px" }}>
              <div style={{ fontSize: 13, fontWeight: 800, fontFamily: "'JetBrains Mono', monospace", color: "#fff" }}>{item.label}</div>
              <div style={{ fontSize: 10, color: "#ffcccc", marginTop: 3 }}>{item.note}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Demands List ── */}
      <SubHead>What We Are Demanding from Council Members</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 18, lineHeight: 1.6 }}>
        These are not requests. They are the minimum conditions that should be met before any new tax measure is placed on a Berkeley ballot.
        Every Council member should be asked — on the record — whether they support each of the following.
      </p>
      {demands.map((d) => (
        <div key={d.n} style={{
          marginBottom: 12, padding: "14px 16px",
          borderLeft: `4px solid ${d.color}`, background: "#faf8f5",
          borderRadius: "0 6px 6px 0"
        }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap", marginBottom: 7 }}>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, fontWeight: 900, color: d.color }}>{d.n}</span>
            <span style={{ fontWeight: 800, fontSize: 14, flex: 1 }}>{d.title}</span>
            <span style={{
              fontSize: 9, fontWeight: 800, letterSpacing: "1px", padding: "2px 8px",
              background: (tagColors[d.tag] || "#888") + "18",
              color: tagColors[d.tag] || "#888", borderRadius: 3,
              fontFamily: "'JetBrains Mono', monospace", whiteSpace: "nowrap"
            }}>{d.tag}</span>
          </div>
          <div style={{ fontSize: 12, color: "#555", lineHeight: 1.7 }}>{d.body}</div>
        </div>
      ))}

      {/* ── Savings Table ── */}
      <SubHead>The Deficit Is Closeable — Without You</SubHead>
      <DataTable
        headers={["Reform", "Annual Savings"]}
        rows={[
          ["Stop paying employee's 8% CalPERS share", { v: "~$16–17M", c: "#c41e1e" }],
          ["Negotiate 1–3% UAL cost-sharing from employees", { v: "~$4–6M", c: "#c41e1e" }],
          ["50/50 OPEB pre-funding split (follow state model)", { v: "~$4–6M", c: "#c41e1e" }],
          ["5% FTE reduction via attrition (no layoffs)", { v: "~$6–9M", c: "#d4860b" }],
          ["Program sunset review + contract audits", { v: "~$4–8M", c: "#d4860b" }],
          [{ v: "Total Potential Savings", bold: true }, { v: "$34–46M/yr", c: "#2a7d4f" }],
          ["Structural deficit to close", { v: "−$27–33M", c: "#c41e1e" }],
        ]}
      />

      <Callout type="dark">
        <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 10, color: "#c41e1e" }}>
          The Bottom Line for November 2026
        </div>
        <p style={{ margin: "0 0 12px", fontSize: 13, lineHeight: 1.75, color: "#e8e4df" }}>
          Berkeley has collected hundreds of millions in new taxes since 2020 — Measure FF, Measure W, Measure P,
          the soda tax, the transfer tax, parcel tax increases. The structural deficit exists anyway.
          The 2022 audit warned about every single problem visible today. Nothing changed.
        </p>
        <p style={{ margin: 0, fontSize: 13, lineHeight: 1.75, fontWeight: 700, color: "#fff" }}>
          More taxes will not fix a management failure. Council members must be held accountable
          before voters are asked to pay more. The money is there. The will to manage it — that's what's missing.
        </p>
      </Callout>
    </>
  );
}

function AuditSection() {
  const recs = [
    {
      id: "1.1",
      rec: "Complete risk assessment; propose plan to replenish Stability & Catastrophic Reserves; consider revising FY 2027 goal",
      status: "Backsliding",
      outcome: "Goal pushed back 6 years (FY 2027 → FY 2033) AND reduced (30% → 25%). City drew $3M from Section 115 Trust in FY 2025.",
    },
    {
      id: "1.2",
      rec: "Assess appropriate fund balance for each enterprise fund; report to Council; explore policy options",
      status: "Not Addressed",
      outcome: "Enterprise funds still experiencing recurring shortfalls. No target fund balance policy adopted. 2026 audit repeats the same recommendation.",
    },
    {
      id: "2.1",
      rec: "Update Debt Management Policy; consider additional debt capacity factors (per capita, debt-to-income, debt service ratios)",
      status: "Partial",
      outcome: "Policy updated in FY 2023, but 15% threshold unchanged. 2026 audit notes it still lacks robust quantitative criteria.",
    },
    {
      id: "3.1",
      rec: "Present plan for Section 115 Trust contributions to Council; ensure consistent annual contributions",
      status: "Backsliding",
      outcome: "Trust balance grew to $29.5M — then City withdrew $3M in FY 2025 to balance the General Fund. Exactly what the 2022 audit warned against.",
    },
    {
      id: "4.1",
      rec: "Collaborate with DPW on funding plan to reduce unfunded capital needs; ensure regular maintenance",
      status: "Not Addressed",
      outcome: "Unfunded needs grew from $1.2B to $1.8B. Measure FF passed but the gap continues to widen. Problem worsened significantly.",
    },
  ];

  const statusStyle = {
    "Not Addressed": { bg: "#fdf0f0", border: "#e8c4c4", color: "#8b0000", label: "NOT ADDRESSED" },
    "Backsliding":   { bg: "#fdf0f0", border: "#e8c4c4", color: "#c41e1e", label: "BACKSLIDING" },
    "Partial":       { bg: "#fdf6e8", border: "#e8d6a8", color: "#8b6914", label: "PARTIAL" },
    "Addressed":     { bg: "#edf7f0", border: "#b8dcc4", color: "#2a7d4f", label: "ADDRESSED" },
  };

  const patchItems = [
    { source: "Section 115 Pension Trust", amount: "$6.0M", note: "Raided the pension savings account" },
    { source: "IT Cost Allocation Fund balance", amount: "$6.2M", note: "One-time transfer to GF" },
    { source: "Workers' Compensation Fund", amount: "$5.2M", note: "Internal service fund raid" },
    { source: "Measure U1 funds", amount: "$2.5M", note: "Using restricted revenue for operations" },
    { source: "44.4 vacant positions left unfunded", amount: "~$8–10M", note: "Deferred hiring, not structural savings" },
    { source: "11.8 GF positions moved to other funds", amount: "~$2–3M", note: "Cost-shifting, not cost-cutting" },
  ];

  const auditDelta = [
    { metric: "Report Framing", v2022: "Pension Liabilities Need Attention", v2026: "Structural Deficit Poses Risk", dir: "worse" },
    { metric: "Expense Growth (inflation-adj.)", v2022: "+20% over decade", v2026: "+39% over decade", dir: "worse" },
    { metric: "Structural Deficit", v2022: "Not identified", v2026: "$32–33M projected FY27–28", dir: "worse" },
    { metric: "Unfunded Capital Needs", v2022: "$1.2B", v2026: "$1.8B (+50% in 3 yrs)", dir: "worse" },
    { metric: "Pension Funded Ratio", v2022: "66% — HIGH RISK", v2026: "66–72% — still HIGH RISK", dir: "flat" },
    { metric: "Govt. Net Position", v2022: "−$101.7M", v2026: "−$188.7M", dir: "worse" },
    { metric: "Section 115 Trust (per audit)", v2022: "$12.1M; missed targets", v2026: "$29.5M — then City raided $3M", dir: "worse" },
    { metric: "Reserve Goal", v2022: "Target 30% by FY 2027", v2026: "Deferred to FY 2033; target cut to 25%", dir: "worse" },
    { metric: "Personal Income per Resident", v2022: "+11% real growth", v2026: "+1% real growth", dir: "worse" },
    { metric: "Net OPEB Liability", v2022: "+91% over decade", v2026: "Declined to $43.2M (FY25)", dir: "better" },
  ];

  const dirStyle = { worse: "#c41e1e", flat: "#d4860b", better: "#2a7d4f" };
  const dirLabel = { worse: "▼ Worse", flat: "► Flat", better: "▲ Better" };

  return (
    <>
      <SectionTitle color="#c41e1e">THE AUDIT TRAIL</SectionTitle>
      <p style={{ fontSize: 13, color: "#555", marginBottom: 24, lineHeight: 1.6 }}>
        Berkeley's City Auditor has issued two comprehensive financial condition reports using the same ICMA methodology —
        in 2022 (covering FY 2012–2021) and 2026 (covering FY 2016–2025). The verdict: nearly every metric got worse.
        And of the five recommendations from 2022, not one was fully implemented.
      </p>

      {/* ── Audit Comparison ── */}
      <SubHead>2022 Audit vs. 2026 Audit: What Changed</SubHead>
      <div style={{ overflowX: "auto", marginBottom: 8 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, minWidth: 560 }}>
          <thead>
            <tr style={{ background: "#1a1a1a", color: "#fff" }}>
              {["Indicator", "2022 Audit Finding", "2026 Audit Finding", ""].map((h, i) => (
                <th key={i} style={{ padding: "9px 12px", textAlign: "left", fontSize: 10, fontWeight: 700, letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {auditDelta.map((row, i) => (
              <tr key={i} style={{ borderBottom: "1px solid #e8e4df", background: i % 2 === 0 ? "#faf8f5" : "transparent" }}>
                <td style={{ padding: "8px 12px", fontWeight: 700, fontSize: 11, color: "#333", whiteSpace: "nowrap" }}>{row.metric}</td>
                <td style={{ padding: "8px 12px", fontSize: 11, color: "#555" }}>{row.v2022}</td>
                <td style={{ padding: "8px 12px", fontSize: 11, fontWeight: 600, color: dirStyle[row.dir] }}>{row.v2026}</td>
                <td style={{ padding: "8px 12px", fontSize: 10, fontWeight: 800, color: dirStyle[row.dir], whiteSpace: "nowrap", fontFamily: "'JetBrains Mono', monospace" }}>
                  {dirLabel[row.dir]}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Callout type="danger">
        <strong style={{ color: "#8b0000" }}>The OPEB improvement is real</strong> — net OPEB liability fell from $83M to $43M in FY25,
        partly due to favorable actuarial assumptions and benefit restructuring. But it's the one bright spot in an otherwise
        deteriorating picture. Pension liabilities remain at $686M, the structural deficit has arrived, and the capital backlog
        grew another $600M in just three years.
      </Callout>

      {/* ── Recommendations Scorecard ── */}
      <SubHead>What the City Was Told to Do — And Didn't</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The 2022 audit made five specific recommendations. Four years later, zero are fully resolved.
      </p>
      {recs.map((r) => {
        const s = statusStyle[r.status];
        return (
          <div key={r.id} style={{
            marginBottom: 12, padding: "12px 14px",
            background: s.bg, border: `1px solid ${s.border}`,
            borderRadius: 6
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 8, marginBottom: 6 }}>
              <span style={{ fontSize: 11, fontWeight: 700, color: "#333" }}>
                <span style={{ fontFamily: "'JetBrains Mono', monospace", color: "#999", marginRight: 8 }}>{r.id}</span>
                {r.rec}
              </span>
              <span style={{
                fontSize: 9, fontWeight: 800, letterSpacing: "1px", padding: "3px 8px",
                background: s.color + "18", color: s.color, borderRadius: 3, whiteSpace: "nowrap",
                fontFamily: "'JetBrains Mono', monospace"
              }}>{s.label}</span>
            </div>
            <div style={{ fontSize: 11, color: "#555", lineHeight: 1.6 }}>→ {r.outcome}</div>
          </div>
        );
      })}

      {/* ── Budget Patch Kit ── */}
      <SubHead>The FY 2026 "Balanced" Budget Patch Kit</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The City's own ACFR admits the FY26 budget is balanced only through one-time measures.
        The structural deficit wasn't solved — it was papered over with ~$20M in fund raids and accounting shifts.
      </p>
      <div style={{ border: "2px solid #e8c4c4", borderRadius: 6, overflow: "hidden", marginBottom: 16 }}>
        <div style={{ background: "#8b0000", color: "#fff", padding: "8px 14px", fontSize: 10, fontWeight: 800, letterSpacing: "1.5px", fontFamily: "'JetBrains Mono', monospace" }}>
          ONE-TIME PATCHES USED TO CLOSE THE FY26 GAP
        </div>
        {patchItems.map((item, i) => (
          <div key={i} style={{
            display: "flex", justifyContent: "space-between", alignItems: "baseline",
            flexWrap: "wrap", gap: 8,
            padding: "9px 14px", borderBottom: i < patchItems.length - 1 ? "1px solid #e8e4df" : "none",
            background: i % 2 === 0 ? "#fdf8f8" : "#fff"
          }}>
            <div>
              <span style={{ fontWeight: 700, fontSize: 12 }}>{item.source}</span>
              <span style={{ fontSize: 11, color: "#888", marginLeft: 10 }}>{item.note}</span>
            </div>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 800, fontSize: 13, color: "#c41e1e", whiteSpace: "nowrap" }}>{item.amount}</span>
          </div>
        ))}
      </div>

      <Callout type="warning">
        <strong>The Section 115 Trust raid is the most telling detail.</strong> The 2022 audit specifically
        warned that Berkeley was missing its pension trust contribution targets. Four years later, the city
        not only didn't fix the problem — it took $3M <em>out</em> of the trust to plug the operating budget.
        This is the definition of kicking the can.
      </Callout>

      {/* ── ACFR FY25 Key Numbers ── */}
      <SubHead>FY 2025 ACFR: Audited Numbers at a Glance</SubHead>
      <DataTable
        headers={["Metric", "FY 2025", "FY 2024", "Direction"]}
        rows={[
          ["Net Pension Liability", "$686.4M", "$723.8M", { v: "▼ $37M", c: "#2a7d4f" }],
          ["Net OPEB Liability", "$43.2M", "$83.4M", { v: "▼ $40M", c: "#2a7d4f" }],
          ["Unrestricted Net Position", "−$415.2M", "−$400.4M", { v: "▲ $14M worse", c: "#c41e1e" }],
          ["Health & Welfare Expenses", "$54.8M", "$44.5M", { v: "▲ +23%", c: "#c41e1e" }],
          ["Public Safety Expenses", "$162.3M", "$190.0M", { v: "▼ −15%", c: "#2a7d4f" }],
          ["Property Tax Revenue", "$148.4M", "$135.7M", { v: "▲ +9%", c: "#2a7d4f" }],
          ["Stability Reserve", "$32.8M", "—", { v: "19.5% of GF", c: "#d4860b" }],
          ["Section 115 Trust", "$29.5M*", "$35.5M", { v: "*After $6M withdrawal", c: "#c41e1e" }],
        ]}
      />
      <div style={{ fontSize: 11, color: "#999", marginTop: 8, fontStyle: "italic" }}>
        Source: City of Berkeley Annual Comprehensive Financial Report, FY 2025 (year ended June 30, 2025).
        City Auditor Jenny Wong, "Berkeley's Financial Condition FY 2016–2025" (2026).
      </div>
    </>
  );
}

function CompareSection() {
  return (
    <>
      <SectionTitle color="#c41e1e">HOW BERKELEY COMPARES</SectionTitle>

      <SubHead>Employee Pension Contributions: Berkeley vs. Everyone</SubHead>
      <div style={{ overflowX: "auto", marginBottom: 8 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, minWidth: 540 }}>
          <thead>
            <tr style={{ background: "#1a1a1a", color: "#fff" }}>
              {["Entity", "Employee Pays", "Employer Pays", "Notes"].map(h => (
                <th key={h} style={{ padding: "10px 12px", textAlign: h === "Notes" ? "left" : "center", fontSize: 10, fontWeight: 700, letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              ["Berkeley (Classic)", "0% — city pays it", "~38% + empl's 8%", "City covers employee's own share"],
              ["Berkeley (PEPRA)", "~50% normal cost", "Remainder + UAL", "Post-2013 hires per state law"],
              ["Escondido", "9% + UAL share", "Remainder", "Cost-sharing since 2018"],
              ["San José", "~11–16%", "Remainder", "Measure B reforms (modified)"],
              ["San Diego (new hires)", "Employee 401(k)", "Match only", "Defined contribution plan"],
              ["CA State (OPEB)", "50% of ADC", "50% of ADC", "Equal split adopted 2015"],
              ["Private Sector (avg)", "6–10% salary", "3–6% match", "Defined contribution (401k)"],
            ].map(([entity, emp, er, note], i) => (
              <tr key={i} style={{ borderBottom: "1px solid #e8e4df", background: i === 0 ? "#fdf0f0" : "transparent" }}>
                <td style={{ padding: "9px 12px", fontWeight: 700, fontSize: 12 }}>{entity}</td>
                <td style={{ padding: "9px 12px", textAlign: "center", fontSize: 12, color: i === 0 ? "#c41e1e" : "#333", fontWeight: i === 0 ? 700 : 400 }}>{emp}</td>
                <td style={{ padding: "9px 12px", textAlign: "center", fontSize: 12 }}>{er}</td>
                <td style={{ padding: "9px 12px", fontSize: 11, color: "#666" }}>{note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Callout type="danger">
        <strong style={{ color: "#8b0000" }}>The Berkeley anomaly:</strong> Classic Berkeley employees pay <em>nothing</em> toward 
        their own pension — the city covers their 8% statutory contribution as an employer-paid benefit. 
        This is not required by law. It is a negotiated perk. It costs taxpayers approximately <strong>$16–17M/year</strong>.
      </Callout>

      <SubHead>CalPERS Funded Status: Berkeley vs. Benchmarks</SubHead>
      {[
        ["Sonoma County (SCERA)", 93, "#2a7d4f"],
        ["Well-Funded Threshold", 90, "#2a7d4f"],
        ["Berkeley Fire", 80.9, "#d4860b"],
        ["Berkeley Misc", 80.1, "#d4860b"],
        ["Avg. CalPERS Agency (2024)", 80.2, "#d4860b"],
        ["Berkeley Police", 68.7, "#c41e1e"],
      ].map(([name, pct, color]) => (
        <div key={name} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 600, marginBottom: 3 }}>
            <span>{name}</span>
            <span style={{ color, fontFamily: "'JetBrains Mono', monospace" }}>{pct}%</span>
          </div>
          <div style={{ height: 7, background: "#e8e4df", borderRadius: 2, overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 2, transition: "width 0.8s ease" }} />
          </div>
        </div>
      ))}

      <SubHead>What Voters Are Already Being Asked (Nov 2026)</SubHead>
      <div style={{ fontSize: 12, lineHeight: 1.5 }}>
        {[
          ["0.5% City Sales Tax", "~$10M/yr", "General Fund deficit"],
          ["$300M GO Bond", "~$20M/yr debt svc", "Infrastructure capital"],
          ["Regional Transit Tax (SB63)", "0.5% sales tax", "BART / AC Transit"],
          ["Arts & Creative Economy Parcel Tax", "TBD", "Performing arts orgs"],
        ].map(([name, cost, purpose]) => (
          <div key={name} style={{ display: "flex", gap: 8, borderBottom: "1px dotted #ddd", padding: "7px 0", alignItems: "baseline", flexWrap: "wrap" }}>
            <span style={{ fontWeight: 700, minWidth: 220 }}>{name}</span>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "#c41e1e", minWidth: 120 }}>{cost}</span>
            <span style={{ color: "#666", fontSize: 11 }}>{purpose}</span>
          </div>
        ))}
      </div>
      <div style={{ fontSize: 11, color: "#999", marginTop: 8, fontStyle: "italic" }}>
        Plus existing measures already passed: Measure FF (streets parcel tax), Measure W/P (property transfer tax for homeless services), 
        parks parcel tax increase, library parcel tax, soda tax reauthorization, streetlight assessment, clean stormwater fee, and more.
      </div>

      <Callout type="dark">
        <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 10, color: "#c41e1e" }}>
          The question taxpayers should ask:
        </div>
        Why should residents pay more when the city hasn't required employees to pay their own pension share? 
        Why bond for infrastructure when benefit costs consume every dollar of revenue growth? 
        Why add a sales tax when program effectiveness isn't being measured?
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #444", fontWeight: 700 }}>
          Reform the cost structure first. Then — and only then — come to voters.
        </div>
      </Callout>
    </>
  );
}

/* ──────────────────── sub-components ──────────────────── */
function SectionTitle({ children, color }) {
  return (
    <h2 style={{ fontSize: 11, fontWeight: 800, letterSpacing: "2.5px", textTransform: "uppercase", color, margin: "0 0 22px", fontFamily: "'JetBrains Mono', monospace" }}>
      {children}
    </h2>
  );
}
function SubHead({ children }) {
  return <h3 style={{ fontSize: 14, fontWeight: 700, margin: "28px 0 14px", fontFamily: "'Source Serif 4', Georgia, serif" }}>{children}</h3>;
}
function GroupHead({ children }) {
  return (
    <h3 style={{
      fontSize: 12, fontWeight: 800, letterSpacing: "1.5px", textTransform: "uppercase",
      margin: "28px 0 12px", paddingBottom: 8, borderBottom: "2px solid #e8e4df",
      fontFamily: "'JetBrains Mono', monospace", color: "#1a1a1a"
    }}>
      {children}
    </h3>
  );
}

function DataTable({ headers, rows }) {
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, minWidth: 400 }}>
        <thead>
          <tr style={{ background: "#1a1a1a", color: "#fff" }}>
            {headers.map((h, i) => (
              <th key={i} style={{ padding: "8px 12px", textAlign: i === 0 ? "left" : "right", fontSize: 10, fontWeight: 700, letterSpacing: "1px" }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, ri) => (
            <tr key={ri} style={{ borderBottom: "1px solid #e8e4df", background: typeof row[0] === "object" && row[0].bold ? "#fdf0f0" : row[0]?.toString().startsWith("  ") ? "#faf8f5" : "transparent" }}>
              {row.map((cell, ci) => {
                const isObj = typeof cell === "object" && cell !== null;
                const value = isObj ? cell.v : cell;
                const color = isObj ? cell.c : undefined;
                const bold = isObj ? cell.bold : (typeof row[0] === "string" && row[0].startsWith("Total")) || (typeof row[0] === "object" && row[0]?.bold);
                return (
                  <td key={ci} style={{
                    padding: "8px 12px", textAlign: ci === 0 ? "left" : "right",
                    fontWeight: (ci === 0 && bold) || color ? 700 : 400,
                    color: color || "#333",
                    fontFamily: ci > 0 ? "'JetBrains Mono', monospace" : "inherit",
                    fontSize: ci > 0 ? 11 : 12
                  }}>
                    {value}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* ──────────────────── MAIN APP ──────────────────── */
export default function App() {
  const [tab, setTab] = useState(0);
  const contentRef = useRef(null);

  useEffect(() => {
    contentRef.current?.scrollTo({ top: 0, behavior: "smooth" });
  }, [tab]);

  const sections = [ShellGameSection, NumbersSection, AuditSection, CarryoverTracker, DemandsSection, CompareSection];
  const ActiveSection = sections[tab];

  return (
    <div style={{ fontFamily: "'Source Serif 4', Georgia, serif", maxWidth: 820, margin: "0 auto", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* ── HEADER ── */}
      <header style={{
        background: "#1a1a1a", color: "#fffdf9",
        padding: "clamp(24px,5vw,40px) clamp(20px,4vw,36px) clamp(20px,4vw,32px)",
        position: "relative", overflow: "hidden"
      }}>
        <div style={{
          position: "absolute", top: 0, right: 0, width: "40%", height: "100%",
          background: "repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(196,30,30,0.06) 10px, rgba(196,30,30,0.06) 20px)"
        }} />
        <div style={{ position: "relative" }}>
          <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "3px", textTransform: "uppercase", color: "#c41e1e", marginBottom: 8, fontFamily: "'JetBrains Mono', monospace" }}>
            BERKELEY TRANSPARENCY HUB — FISCAL BRIEF
          </div>
          <h1 style={{
            fontSize: "clamp(28px,5vw,42px)", fontWeight: 900, lineHeight: 1.08, margin: 0,
            fontFamily: "'Playfair Display', Georgia, serif"
          }}>
            Berkeley Has the Money.<br />They Just Hide It.
          </h1>
          <p style={{ fontSize: "clamp(13px,2vw,15px)", color: "#aaa", marginTop: 12, maxWidth: 560, lineHeight: 1.55 }}>
            Berkeley overbudgets, quietly rolls unspent money forward through the AAO process, raids dedicated funds
            to fake a balanced budget — then asks voters for a new sales tax. The money exists.
            The management doesn't.
          </p>
          <div style={{ display: "flex", gap: 16, marginTop: 18, flexWrap: "wrap", alignItems: "center" }}>
            <div style={{
              padding: "6px 18px", border: "2px solid #c41e1e", color: "#c41e1e",
              fontSize: 11, fontWeight: 800, letterSpacing: "2.5px", textTransform: "uppercase",
              fontFamily: "'JetBrains Mono', monospace"
            }}>
              NO NEW TAXES — NOV 2026
            </div>
            <div style={{ fontSize: 11, color: "#888" }}>
              $316M hidden carryovers · ~$20M fund raids · $33M deficit · Closeable through reform
            </div>
          </div>
        </div>
      </header>

      {/* ── TAB NAV ── */}
      <nav style={{
        display: "flex", borderBottom: "2px solid #1a1a1a",
        background: "#f5f1eb", position: "sticky", top: 0, zIndex: 10
      }}>
        {TABS.map((t, i) => (
          <button
            key={t.key}
            onClick={() => setTab(i)}
            style={{
              flex: 1, padding: "12px 8px", border: "none", cursor: "pointer",
              fontSize: 10, fontWeight: 800, letterSpacing: "1.5px",
              background: tab === i ? "#1a1a1a" : "transparent",
              color: tab === i ? "#fffdf9" : "#1a1a1a",
              transition: "all 0.15s",
              fontFamily: "'JetBrains Mono', monospace",
              borderRight: i < TABS.length - 1 ? "1px solid #ddd" : "none"
            }}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {/* ── CONTENT ── */}
      <main ref={contentRef} style={{ padding: "clamp(20px,4vw,36px)", flex: 1 }}>
        <ActiveSection />
      </main>

      {/* ── FOOTER ── */}
      <footer style={{
        padding: "20px clamp(20px,4vw,36px)", borderTop: "2px solid #1a1a1a",
        fontSize: 10, color: "#999", lineHeight: 1.6,
        fontFamily: "'JetBrains Mono', monospace"
      }}>
        <strong style={{ color: "#666" }}>Sources:</strong> City of Berkeley Unfunded Liability Obligations Report (Apr 2023); 
        CalPERS Actuarial Valuations (June 30, 2021); Foster & Foster Pension &amp; OPEB Funding Study (Feb 2023); 
        City of Berkeley FY2024 Revenue Narratives; Daily Californian (Mar 2026); Berkeleyside; CalPERS Circular Letters.
        <div style={{ marginTop: 8, color: "#bbb" }}>
          Compiled by <strong>Berkeley Transparency Hub</strong> · Data as of Spring 2026 · 
          This is a civic transparency resource, not legal or financial advice.
        </div>
      </footer>
    </div>
  );
}
