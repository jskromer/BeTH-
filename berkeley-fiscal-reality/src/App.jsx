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
    dark: { bg: "#1a2a4a", border: "#2a3a5a", accent: "#93b8e8" },
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
  { key: "shellgame", label: "HOW IT WORKS" },
  { key: "numbers",   label: "THE NUMBERS" },
  { key: "record",    label: "AUDIT RECORD" },
  { key: "aao",       label: "AAO TRACKER" },
  { key: "demands",   label: "OUR POSITION" },
  { key: "compare",   label: "COMPARISONS" },
];

function ShellGameSection() {
  const cycle = [
    { n: "1", title: "Appropriate", body: "Council adopts a budget with more spending authority than departments typically use. This gives programs the resources to execute — but actual spending usually comes in 10–20% below the appropriated amount." },
    { n: "2", title: "Underspend", body: "Departments spend 80–90% of their appropriations. The remaining balance is unencumbered at year-end — funds that were authorized but not needed." },
    { n: "3", title: "Carry Forward", body: "Each November, AAO #1 brings unspent prior-year amounts into the new fiscal year as 'carryovers' and 'encumbrances.' This is passed on the consent calendar, typically without a standalone public hearing." },
    { n: "4", title: "Accumulate Balances", body: "Over three years, $316M in carryovers (all funds) and $367M in encumbrances have moved through the AAO process — significant appropriation activity that happens outside the main budget cycle." },
    { n: "5", title: "Draw on Available Funds", body: "When the structural deficit appears, the City draws on internal fund balances — including the pension pre-funding trust, Workers' Comp reserves, and IT fund surpluses — to reach a balanced budget." },
    { n: "6", title: "Ask Voters for More Revenue", body: "With the budget balanced, the City presents voters with a $33M structural challenge and proposes a sales tax to address it. The question worth asking: has every internal option been fully explored first?" },
  ];

  const patches = [
    { source: "Section 115 Pension Trust", amount: 6.0, note: "Pre-funding trust — intended for pension obligations, not operations" },
    { source: "IT Cost Allocation Fund", amount: 6.2, note: "Internal service fund — one-time transfer to General Fund" },
    { source: "Workers' Compensation Fund", amount: 5.2, note: "Claims reserve — drew down above-target balance" },
    { source: "Measure U1 Funds", amount: 2.5, note: "Voter-approved special revenue — applied to operating budget" },
    { source: "44.4 Vacant Positions Left Unfunded", amount: null, note: "~$8–10M est. — positions deferred rather than eliminated" },
    { source: "11.8 GF Positions Moved to Other Funds", amount: null, note: "~$2–3M est. — cost shifted to non-GF accounts" },
  ];

  const policyPoints = [
    {
      label: "City Fiscal Policy #5 — TENSION",
      quote: "\"Primarily allocating one-time revenue for one-time expenditures\"",
      detail: "The City's own fiscal policy calls for one-time funds to cover one-time costs. Using the Section 115 Trust and Workers' Comp reserve for recurring operating gaps raises the question of whether this principle is being followed.",
      color: "#8b6914",
    },
    {
      label: "City Fiscal Policy #6 — FLAGGED IN TWO AUDITS",
      quote: "\"Enterprise and grant funds to balance and new programs to pay for themselves\"",
      detail: "Both the 2022 and 2026 City Auditor reports flag enterprise fund shortfalls as unresolved. The recommendation has been carried forward without resolution, suggesting this policy goal has not yet been achieved.",
      color: "#8b6914",
    },
    {
      label: "Section 115 Trust — QUESTION OF INTENT",
      quote: "Council Resolution establishing trust for pension pre-funding",
      detail: "The trust was established specifically to pre-fund pension obligations. Withdrawals of $3M (FY25) and $6M (FY26) for operating purposes raise a reasonable question about whether this is consistent with the trust's stated purpose.",
      color: "#8b6914",
    },
    {
      label: "Prop 218 (CA Constitution) — VOTER INFORMATION",
      quote: "Voter approval required; voters must be accurately informed",
      detail: "California's Prop 218 requires voter approval for new taxes. Residents casting that vote would benefit from a clear, plain-language accounting of how the current budget was balanced — including all internal fund transfers.",
      color: "#8b6914",
    },
  ];

  return (
    <>
      <SectionTitle color="#1a4a8b">HOW OUR BUDGET WORKS</SectionTitle>
      <p style={{ fontSize: 14, lineHeight: 1.7, marginBottom: 24, color: "#333", fontWeight: 600 }}>
        Berkeley faces a $33M structural deficit and is considering a 0.5% sales tax and a $300M bond for November 2026.
        As residents, we think it's worth understanding how the City's budget is built, balanced, and amended each year —
        and what questions that process raises before we're asked to vote on new revenue.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px,1fr))", border: "2px solid #1a1a1a", borderRadius: 8, overflow: "hidden", marginBottom: 28 }}>
        {[
          { value: "~$20M", label: "One-Time FY26 Transfers", sub: "Used to balance this year's budget", color: "#1a4a8b" },
          { value: "$316M", label: "AAO Carryovers (3 yrs)", sub: "All funds FY24–26 ($32M GF portion)", color: "#1a4a8b" },
          { value: "$33M", label: "Structural Deficit", sub: "Projected recurring FY27–28 gap", color: "#c41e1e" },
          { value: "0 of 5", label: "Audit Recs Resolved", sub: "2022 recommendations, still open", color: "#8b6914" },
        ].map((s, i, arr) => (
          <div key={i} style={{ padding: "16px 12px", background: "#faf8f5", borderRight: i < arr.length - 1 ? "1px solid #e0dcd6" : "none", textAlign: "center" }}>
            <StatBlock {...s} />
          </div>
        ))}
      </div>

      <SubHead>The Annual Budget Cycle — Six Steps</SubHead>
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

      <SubHead>FY 2026: How the Budget Was Balanced</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 12, lineHeight: 1.6 }}>
        The City's Annual Comprehensive Financial Report (FY2025, pp. v–xix) notes that the FY26 budget
        relied on one-time measures to close the gap. Here's what those measures were, in plain language:
      </p>
      <div style={{ border: "1px solid #d5cfc8", borderRadius: 6, overflow: "hidden", marginBottom: 20 }}>
        <div style={{ background: "#1a2a4a", color: "#fff", padding: "9px 14px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 10, fontWeight: 800, letterSpacing: "1.5px", fontFamily: "'JetBrains Mono', monospace" }}>FY26 ONE-TIME BALANCING MEASURES</span>
          <span style={{ fontSize: 10, fontWeight: 800, fontFamily: "'JetBrains Mono', monospace" }}>~$20M TOTAL</span>
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

      <SubHead>Policy Questions Worth Asking</SubHead>
      {policyPoints.map((v, i) => (
        <div key={i} style={{ marginBottom: 10, padding: "13px 15px", background: "#faf8f5", border: `1px solid ${v.color}44`, borderLeft: `4px solid ${v.color}`, borderRadius: "0 6px 6px 0" }}>
          <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "1px", color: v.color, fontFamily: "'JetBrains Mono', monospace", marginBottom: 5 }}>{v.label}</div>
          <div style={{ fontSize: 12, fontStyle: "italic", color: "#555", marginBottom: 6 }}>{v.quote}</div>
          <div style={{ fontSize: 12, color: "#333", lineHeight: 1.65 }}>{v.detail}</div>
        </div>
      ))}

      <Callout type="warning">
        <div style={{ fontWeight: 800, fontSize: 14, marginBottom: 8 }}>What Would Help Residents Understand Their Budget</div>
        AAO amendments move through the consent calendar each November without a standalone public hearing or a
        plain-language summary of cumulative carryover patterns. The one-time balancing measures are disclosed in
        the ACFR — but that's a technical document most residents never see.
        <div style={{ marginTop: 10, fontWeight: 700, fontSize: 13, color: "#8b6914" }}>
          A simple, annual plain-language budget summary — showing what carried forward, what was transferred, and what the real structural gap is — would go a long way toward the informed electorate Berkeley says it values.
        </div>
      </Callout>
    </>
  );
}

function NumbersSection() {
  return (
    <>
      <SectionTitle color="#1a4a8b">THE NUMBERS</SectionTitle>
      <p style={{ fontSize: 14, lineHeight: 1.7, marginBottom: 24, color: "#333", fontWeight: 600 }}>
        Berkeley is a well-funded city — managing over <strong>$700M/year</strong> in total revenues.
        Understanding where that money goes, and how the budget is balanced each year,
        gives residents the context they need before any vote on new taxes.
      </p>

      {/* ── Excess Equity Explainer ── */}
      <div style={{ background: "#1a2a4a", color: "#fffdf9", padding: "18px 20px", borderRadius: 8, marginBottom: 24 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "2px", color: "#93b8e8", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10 }}>
          KEY CONCEPT: EXCESS EQUITY
        </div>
        <p style={{ fontSize: 13, lineHeight: 1.75, margin: 0, color: "#e8f0fa" }}>
          <strong style={{ color: "#fff" }}>Excess equity</strong> is the balance that accumulates in internal service funds
          and enterprise funds above their stated reserve targets. Berkeley's IT Cost Allocation Fund, Workers' Compensation Fund,
          and other internal accounts had built up surpluses beyond what they needed as reserves.
          When the General Fund faced a structural gap, the City transferred funds from these pools to balance the budget.
          <strong style={{ color: "#93b8e8" }}> This is a one-time measure — it resolves the current year's gap
          but reduces the cushion those funds were built to maintain going forward.</strong>
        </p>
        <div style={{ marginTop: 14, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 10 }}>
          {[
            { label: "IT Fund Transfer", value: "$6.2M", note: "Excess balance moved to General Fund" },
            { label: "Workers' Comp Transfer", value: "$5.2M", note: "Above-target reserve drawn down" },
            { label: "Pension Trust Transfer", value: "$6.0M", note: "Pre-funding trust — used for operations" },
            { label: "Measure U1 Applied", value: "$2.5M", note: "Special revenue applied to operating budget" },
          ].map((item, i) => (
            <div key={i} style={{ background: "rgba(255,255,255,0.08)", borderRadius: 6, padding: "10px 12px", border: "1px solid rgba(255,255,255,0.12)" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#93b8e8", fontFamily: "'JetBrains Mono', monospace" }}>{item.value}</div>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#fff", marginTop: 3 }}>{item.label}</div>
              <div style={{ fontSize: 10, color: "#93b8e8", marginTop: 2 }}>{item.note}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── ACFR Key Numbers ── */}
      <SubHead>What the Audited Books Show (FY2025 ACFR)</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The Annual Comprehensive Financial Report is the City's audited financial statement — the most reliable source
        of numbers we have. Here's what it shows for FY2025:
      </p>
      <DataTable
        headers={["Metric", "FY 2025 (Audited)", "FY 2024", "Direction"]}
        rows={[
          ["Total Government Revenue", "$703M+", "—", { v: "Strong revenue base", c: "#2a7d4f" }],
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
      <SubHead>Revenue vs. Expenditure Trends</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        General Fund revenue has been <strong>essentially flat for three years</strong> — it declined from $273M in FY23 to $262M in FY24 before recovering slightly.
        Meanwhile, expenditures have grown each year. The gap reflects benefit cost growth that consistently outpaces revenue.
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

      <Callout type="warning">
        <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 10 }}>
          Putting It in Context
        </div>
        <p style={{ margin: "0 0 10px", fontSize: 13, lineHeight: 1.7 }}>
          Property tax revenue grew 9% in one year. Total city revenues exceed $700M. The General Fund collects $268M annually.
          At the same time, $316M in appropriations moved through the AAO process across all funds over three years,
          and internal fund balances were drawn down to close the FY26 gap.
        </p>
        <p style={{ margin: 0, fontSize: 13, lineHeight: 1.7 }}>
          The structural deficit is real — and it is driven primarily by benefit cost growth that outpaces revenue.
          The reforms needed are known, the savings are calculable, and comparable cities have implemented them.
          That is the conversation we'd like to see happen before new taxes are placed on the ballot.
        </p>
      </Callout>
    </>
  );
}

function DemandsSection() {
  const asks = [
    {
      n: "01",
      title: "Pause the November 2026 Sales Tax — Reform First",
      color: "#1a4a8b",
      body: "A 0.5% sales tax falls hardest on lower-income residents. Before asking for new revenue, Berkeley should demonstrate it has fully explored internal cost reform. The structural deficit is largely a compensation structure problem, not a revenue shortfall — and there are concrete, measurable steps that can close it.",
      tag: "BALLOT TIMING",
    },
    {
      n: "02",
      title: "Reconsider the $300M Bond Until Capital Backlogs Are Explained",
      color: "#1a4a8b",
      body: "Berkeley's unfunded capital need grew from $1.2B to $1.8B in three years — despite Measure FF. Before issuing more debt, voters deserve a clear accounting of why the gap widened and what specifically the new bond would accomplish that existing measures have not.",
      tag: "BALLOT TIMING",
    },
    {
      n: "03",
      title: "Publish a Plain-Language AAO Summary Before Any Tax Vote",
      color: "#1a4a8b",
      body: "The annual AAO process moves hundreds of millions in mid-cycle amendments through the consent calendar with minimal public explanation. A one-page summary — total carryovers, total new adjustments, and General Fund impact — should accompany every AAO package sent to Council and posted publicly.",
      tag: "TRANSPARENCY",
    },
    {
      n: "04",
      title: "Bring Employee Pension Cost-Sharing to the Table",
      color: "#2a5c3f",
      body: "Berkeley pays the employee's own 8% CalPERS contribution on their behalf — a negotiated benefit that most peer cities ended years ago. At ~$16–17M/year, this single item represents more than half the structural deficit. We ask that the City open an honest public conversation about what cost-sharing could look like in future MOU negotiations.",
      tag: "COST REFORM",
    },
    {
      n: "05",
      title: "Protect the Section 115 Pension Pre-Funding Trust",
      color: "#2a5c3f",
      body: "The City withdrew $9M from the Section 115 Trust over FY25–26 to cover operating expenses — precisely the use the 2022 audit warned against. We ask Council to formally clarify the permitted uses of the trust and commit to a replenishment schedule. Long-term pension stability depends on keeping this fund intact.",
      tag: "FIDUCIARY DUTY",
    },
    {
      n: "06",
      title: "Disclose Internal Service Fund Balances Annually",
      color: "#2a5c3f",
      body: "When internal funds like IT Cost Allocation and Workers' Compensation accumulate balances above their reserve targets, those surpluses should be reported to Council and the public — not quietly swept into the General Fund when a budget gap appears. Annual disclosure with target vs. actual comparisons is a reasonable standard.",
      tag: "TRANSPARENCY",
    },
    {
      n: "07",
      title: "Set a Completion Date for the 2022 Audit Recommendations",
      color: "#8b6914",
      body: "The City Auditor's 2022 report made five specific, actionable recommendations. Four years later, none are fully resolved — and the 2026 audit largely repeats them. We ask Council to assign named staff to each recommendation, set a completion timeline, and report quarterly on progress.",
      tag: "ACCOUNTABILITY",
    },
    {
      n: "08",
      title: "Formalize the Vacancy Management Policy",
      color: "#8b6914",
      body: "Berkeley left 44.4 positions unfunded in FY26, saving an estimated $8–10M. This reflects a practical judgment that those positions aren't currently essential. We ask that this be made an explicit policy decision rather than an informal workaround — with clear criteria for when positions are backfilled.",
      tag: "FISCAL DISCIPLINE",
    },
  ];

  const tagColors = {
    "BALLOT TIMING":    "#1a4a8b",
    "TRANSPARENCY":     "#1a4a8b",
    "COST REFORM":      "#2a5c3f",
    "FIDUCIARY DUTY":   "#2a5c3f",
    "ACCOUNTABILITY":   "#8b6914",
    "FISCAL DISCIPLINE":"#8b6914",
  };

  return (
    <>
      <SectionTitle color="#1a4a8b">OUR POSITION</SectionTitle>

      {/* ── Framing Banner ── */}
      <div style={{ background: "#1a2a4a", color: "#fff", padding: "20px 22px", borderRadius: 8, marginBottom: 28 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "3px", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10, color: "#93b8e8" }}>
          THE CASE FOR REFORM BEFORE NEW REVENUE — 2026
        </div>
        <p style={{ fontSize: 14, fontWeight: 600, lineHeight: 1.7, margin: "0 0 14px", color: "#e8f0fa" }}>
          We support Berkeley's long-term fiscal health. That's precisely why we think new taxes should wait
          until the City demonstrates it has addressed the structural issues its own auditors have identified.
          The data shows a management challenge that precedes any revenue shortfall.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 10 }}>
          {[
            { label: "Revenue > $700M/yr", note: "Berkeley is not underfunded" },
            { label: "$316M in AAO Amendments", note: "All-fund mid-cycle moves, minimal public review" },
            { label: "~$20M in Fund Transfers", note: "Internal equity used to close the FY26 gap" },
            { label: "0 of 5 Audit Recs Done", note: "2022 recommendations, still unresolved in 2026" },
          ].map((item, i) => (
            <div key={i} style={{ background: "rgba(255,255,255,0.08)", borderRadius: 6, padding: "10px 12px", border: "1px solid rgba(255,255,255,0.12)" }}>
              <div style={{ fontSize: 13, fontWeight: 800, fontFamily: "'JetBrains Mono', monospace", color: "#fff" }}>{item.label}</div>
              <div style={{ fontSize: 10, color: "#93b8e8", marginTop: 3 }}>{item.note}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Asks List ── */}
      <SubHead>What We're Asking of Council</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 18, lineHeight: 1.6 }}>
        These eight reforms are grounded in the City's own audit findings and financial reports.
        They are achievable, measurable, and — we believe — what responsible stewardship looks like
        before asking Berkeley residents to contribute more.
      </p>
      {asks.map((d) => (
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
      <SubHead>A Path to Fiscal Balance — Without New Taxes</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The structural deficit is real — but it is closeable through reforms the City has the authority to pursue today.
        These are not speculative; they are based on comparable reforms in other California cities.
      </p>
      <DataTable
        headers={["Reform", "Est. Annual Savings"]}
        rows={[
          ["Employee cost-sharing on 8% CalPERS contribution", { v: "~$16–17M", c: "#2a5c3f" }],
          ["Negotiate 1–3% UAL cost-sharing in future MOUs", { v: "~$4–6M", c: "#2a5c3f" }],
          ["50/50 OPEB pre-funding split (California state model)", { v: "~$4–6M", c: "#2a5c3f" }],
          ["5% workforce reduction through attrition only", { v: "~$6–9M", c: "#8b6914" }],
          ["Program sunset review + contract renegotiation", { v: "~$4–8M", c: "#8b6914" }],
          [{ v: "Total Potential Annual Savings", bold: true }, { v: "$34–46M", c: "#2a5c3f" }],
          [{ v: "Structural deficit to close (FY27–28 proj.)", bold: false }, { v: "$27–33M", c: "#555" }],
        ]}
      />

      <Callout type="warning">
        <div style={{ fontWeight: 800, fontSize: 14, marginBottom: 8 }}>
          Our ask is simple: reform first, then ask.
        </div>
        <p style={{ margin: "0 0 10px", fontSize: 13, lineHeight: 1.75 }}>
          Berkeley has passed significant new revenue measures since 2020 — Measure FF, Measure W, Measure P,
          transfer tax increases, and more. The structural deficit grew alongside them. That pattern suggests
          the problem is structural cost growth, not insufficient taxation.
        </p>
        <p style={{ margin: 0, fontSize: 13, lineHeight: 1.75 }}>
          Demonstrate the reforms. Show voters that the cost structure is under control.
          Build the trust — then make the case for new revenue. That is the path to a yes we can believe in.
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
    { source: "Section 115 Pension Trust", amount: "$6.0M", note: "Transfer from pre-funding trust to General Fund" },
    { source: "IT Cost Allocation Fund balance", amount: "$6.2M", note: "Above-target balance transferred to GF" },
    { source: "Workers' Compensation Fund", amount: "$5.2M", note: "Above-target reserve drawn down" },
    { source: "Measure U1 funds", amount: "$2.5M", note: "Special revenue applied to operating budget" },
    { source: "44.4 vacant positions left unfunded", amount: "~$8–10M", note: "Positions deferred rather than eliminated" },
    { source: "11.8 GF positions moved to other funds", amount: "~$2–3M", note: "Costs shifted to non-GF accounts" },
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
      <SectionTitle color="#1a4a8b">THE AUDIT RECORD</SectionTitle>
      <p style={{ fontSize: 13, color: "#555", marginBottom: 24, lineHeight: 1.6 }}>
        Berkeley's City Auditor has issued two comprehensive financial condition reports using the same ICMA methodology —
        in 2022 (covering FY 2012–2021) and 2026 (covering FY 2016–2025). Comparing them side by side shows
        where conditions have improved, held steady, or worsened — and how the City has responded to
        the five specific recommendations made in 2022.
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
      <SubHead>2022 Audit Recommendations: Where Things Stand</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The 2022 audit made five specific recommendations. The 2026 audit assessed where each one stands today.
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
      <SubHead>How the FY 2026 Budget Was Balanced</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The ACFR notes that the FY26 budget used one-time measures to close the structural gap.
        These measures addressed the current year but don't resolve the underlying cost trends.
      </p>
      <div style={{ border: "1px solid #d5cfc8", borderRadius: 6, overflow: "hidden", marginBottom: 16 }}>
        <div style={{ background: "#1a2a4a", color: "#fff", padding: "8px 14px", fontSize: 10, fontWeight: 800, letterSpacing: "1.5px", fontFamily: "'JetBrains Mono', monospace" }}>
          FY26 ONE-TIME BALANCING MEASURES (~$20M)
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
        <strong>The Section 115 Trust withdrawal stands out.</strong> The 2022 audit specifically
        flagged that Berkeley was missing its pension trust contribution targets and recommended
        consistent annual contributions. Four years later, the City drew $3M from the trust to help
        balance the operating budget — the opposite direction from what the audit advised.
        The 2026 audit notes this as an ongoing concern.
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
      <SectionTitle color="#1a4a8b">HOW BERKELEY COMPARES</SectionTitle>

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

      <Callout type="warning">
        <strong>A notable difference:</strong> Classic Berkeley employees do not pay toward their own pension —
        the City covers their 8% statutory CalPERS contribution as an employer-paid benefit.
        This is a negotiated arrangement, not a legal requirement, and most peer cities have
        moved away from it. The cost to Berkeley taxpayers is approximately <strong>$16–17M/year</strong>.
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

      <Callout type="warning">
        <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 10 }}>
          Questions worth raising:
        </div>
        If employee cost-sharing is standard practice across California, why hasn't Berkeley brought it to the table?
        If infrastructure needs keep growing despite dedicated measures, what would change with a bond?
        If audit recommendations have gone unresolved for four years, what would change after a new tax?
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #e8d6a8", fontWeight: 700 }}>
          These are the conversations we'd like to see before November 2026.
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
        background: "#1e2d4a", color: "#fffdf9",
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
            Berkeley's Budget:<br />What the Data Shows
          </h1>
          <p style={{ fontSize: "clamp(13px,2vw,15px)", color: "#aaa", marginTop: 12, maxWidth: 560, lineHeight: 1.55 }}>
            Berkeley manages over $700M in annual revenues. Understanding how those funds are appropriated,
            carried forward, and balanced is essential context for any conversation about new taxes in 2026.
          </p>
          <div style={{ display: "flex", gap: 16, marginTop: 18, flexWrap: "wrap", alignItems: "center" }}>
            <div style={{
              padding: "6px 18px", border: "2px solid #c41e1e", color: "#c41e1e",
              fontSize: 11, fontWeight: 800, letterSpacing: "2.5px", textTransform: "uppercase",
              fontFamily: "'JetBrains Mono', monospace"
            }}>
              REFORM BEFORE NEW REVENUE
            </div>
            <div style={{ fontSize: 11, color: "#888" }}>
              $33M structural deficit · closeable through internal reform · audit findings unresolved
            </div>
          </div>
        </div>
      </header>

      {/* ── TAB NAV ── */}
      <nav style={{
        display: "flex", borderBottom: "2px solid #1e2d4a",
        background: "#f5f1eb", position: "sticky", top: 0, zIndex: 10
      }}>
        {TABS.map((t, i) => (
          <button
            key={t.key}
            onClick={() => setTab(i)}
            style={{
              flex: 1, padding: "12px 8px", border: "none", cursor: "pointer",
              fontSize: 10, fontWeight: 800, letterSpacing: "1.5px",
              background: tab === i ? "#1e2d4a" : "transparent",
              color: tab === i ? "#fffdf9" : "#1e2d4a",
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
        padding: "20px clamp(20px,4vw,36px)", borderTop: "2px solid #1e2d4a",
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
