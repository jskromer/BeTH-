import { useState, useEffect, useRef } from "react";
import CarryoverTracker from "./CarryoverTracker";
import { Analytics } from "@vercel/analytics/react";

/* ──────────────────── shared helpers ──────────────────── */
const fmt = (n) => (n >= 1000 ? `$${(n / 1000).toFixed(1)}B` : `$${n}M`);

function StatBlock({ value, label, sub, color = "#002198" }) {
  return (
    <div className="stat-block">
      <div style={{ fontSize: "clamp(24px,5vw,36px)", fontWeight: 900, color, letterSpacing: "-1px", lineHeight: 1.1, fontFamily: "'JetBrains Mono', monospace" }}>{value}</div>
      <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "1.5px", marginTop: 6, color: "#0b1540" }}>{label}</div>
      {sub && <div style={{ fontSize: 10, color: "#888", marginTop: 3 }}>{sub}</div>}
    </div>
  );
}

function Bar({ label, value, max, color = "#a8322c", funded, suffix = " unfunded" }) {
  const pct = (value / max) * 100;
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 600, marginBottom: 4, flexWrap: "wrap", gap: 4 }}>
        <span>{label}</span>
        <span style={{ color: "#666", fontFamily: "'JetBrains Mono', monospace", fontSize: 10 }}>
          ${value}M{suffix}
          {funded !== undefined && (
            <span style={{ marginLeft: 6, color: funded < 20 ? "#a8322c" : funded < 50 ? "#8a5a00" : "#666", fontWeight: 700 }}>
              ({funded}% funded)
            </span>
          )}
        </span>
      </div>
      <div style={{ height: 8, background: "#d3d6db", borderRadius: 2, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${Math.min(pct, 100)}%`, background: color, borderRadius: 2, transition: "width 0.8s cubic-bezier(.22,1,.36,1)" }} />
      </div>
    </div>
  );
}

// Bar where width = % funded; right label = unfunded % + $ amount
function FundingBar({ label, funded, unfundedDollars, color = "#8a5a00" }) {
  const unfundedPct = (100 - funded).toFixed(1);
  const labelColor = funded < 20 ? "#a8322c" : funded < 50 ? "#8a5a00" : "#555";
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
      <div style={{ height: 8, background: "#d3d6db", borderRadius: 2, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${funded}%`, background: color, borderRadius: 2, transition: "width 0.8s cubic-bezier(.22,1,.36,1)" }} />
      </div>
    </div>
  );
}

function SolutionRow({ title, savings, detail, urgency }) {
  const colors = { high: "#a8322c", medium: "#8a5a00", low: "#1f6b4a" };
  const labels = { high: "IMMEDIATE", medium: "NEAR-TERM", low: "STRUCTURAL" };
  return (
    <div style={{
      padding: "14px 16px", background: "#e4e7f3",
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
          <span style={{ fontWeight: 800, fontSize: 15, color: "#1f6b4a", fontFamily: "'JetBrains Mono', monospace", whiteSpace: "nowrap" }}>{savings}</span>
        </div>
      </div>
      <div style={{ fontSize: 12, color: "#555", marginTop: 6, lineHeight: 1.65 }}>{detail}</div>
    </div>
  );
}

function Callout({ children, type = "danger" }) {
  const styles = {
    danger: { bg: "#fbeeed", border: "#efcfcc", accent: "#7a221d" },
    warning: { bg: "#fbf1dc", border: "#ecd9a6", accent: "#6b4500" },
    success: { bg: "#e3efe9", border: "#bfdccb", accent: "#1f6b4a" },
    dark: { bg: "#000d6b", border: "#002198", accent: "#cfd8ff" },
  };
  const s = styles[type];
  return (
    <div style={{
      marginTop: 20, padding: "16px 18px",
      background: s.bg, border: `1px solid ${s.border}`,
      borderRadius: 6, fontSize: 13, lineHeight: 1.65,
      color: type === "dark" ? "#ebecee" : "#333"
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
  { key: "habit",     label: "THE HABIT",    href: "/history-of-the-habit.html" },
  { key: "mayor",     label: "MAYOR'S BUDGET", href: "/mayors-budget.html" },
  { key: "reform",    label: "THE FIX",      href: "/rational-budgeting-process.html" },
  { key: "messaging", label: "MESSAGING",    href: "/two-messages.html" },
  { key: "beth",      label: "BETH DATA HUB ↗", href: "https://learn-about-berkeley.vercel.app/", external: true },
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
    { source: "Section 115 Pension Trust", amount: 6.0, note: "$6.0M used for FY26 pension obligations (FY2025 ACFR, MD&A)" },
    { source: "IT Cost Allocation Fund", amount: 6.2, note: "Above-target balance transferred to GF, FY26 (FY2025 ACFR)" },
    { source: "Workers' Compensation Fund", amount: 5.2, note: "$5.2M transferred to GF, FY26 (FY2025 ACFR, MD&A)" },
    { source: "Measure U1 Funds", amount: 2.5, note: "Voter-approved special revenue — applied to operating budget" },
    { source: "44.4 Vacant Positions Left Unfunded", amount: null, note: "~$8–10M est. — positions deferred rather than eliminated" },
    { source: "11.8 GF Positions Moved to Other Funds", amount: null, note: "~$2–3M est. — cost shifted to non-GF accounts" },
  ];

  const policyPoints = [
    {
      label: "City Fiscal Policy #5 — TENSION",
      quote: "\"Primarily allocating one-time revenue for one-time expenditures\"",
      detail: "The City's own fiscal policy calls for one-time funds to cover one-time costs. Using the Section 115 Trust and Workers' Comp reserve for recurring operating gaps raises the question of whether this principle is being followed.",
      color: "#6b4500",
    },
    {
      label: "City Fiscal Policy #6 — FLAGGED IN TWO AUDITS",
      quote: "\"Enterprise and grant funds to balance and new programs to pay for themselves\"",
      detail: "Both the 2022 and 2026 City Auditor reports flag enterprise fund shortfalls as unresolved. The recommendation has been carried forward without resolution, suggesting this policy goal has not yet been achieved.",
      color: "#6b4500",
    },
    {
      label: "Section 115 Trust — QUESTION OF INTENT",
      quote: "Council Resolution establishing trust for pension pre-funding",
      detail: "The trust was established specifically to pre-fund pension obligations. Withdrawals of $3M (FY25) and $6M (FY26) for operating purposes raise a reasonable question about whether this is consistent with the trust's stated purpose.",
      color: "#6b4500",
    },
    {
      label: "Prop 218 (CA Constitution) — VOTER INFORMATION",
      quote: "Voter approval required; voters must be accurately informed",
      detail: "California's Prop 218 requires voter approval for new taxes. Residents casting that vote would benefit from a clear, plain-language accounting of how the current budget was balanced — including all internal fund transfers.",
      color: "#6b4500",
    },
  ];

  return (
    <>
      <SectionTitle color="#002198">HOW OUR BUDGET WORKS</SectionTitle>
      <p style={{ fontSize: 14, lineHeight: 1.7, marginBottom: 24, color: "#333", fontWeight: 600 }}>
        Berkeley faces a $33M structural deficit and is considering a 0.5% sales tax and a $300M bond for November 2026.
        As residents, we think it's worth understanding how the City's budget is built, balanced, and amended each year —
        and what questions that process raises before we're asked to vote on new revenue.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px,1fr))", border: "2px solid #0b1540", borderRadius: 8, overflow: "hidden", marginBottom: 28 }}>
        {[
          { value: "~$20M", label: "One-Time FY26 Transfers", sub: "Internal-fund redirects to balance the General Fund", color: "#002198" },
          { value: "$316M", label: "AAO Carryovers (3 yrs)", sub: "All funds FY24–26 ($32M GF portion)", color: "#002198" },
          { value: "$33M", label: "Structural Deficit", sub: "Projected recurring FY27–28 gap", color: "#a8322c" },
          { value: "0 of 5", label: "2022 Audit Recs Fully Resolved", sub: "BeTH assessment against the 2026 audit · 76 of 384 dropped citywide", color: "#6b4500" },
        ].map((s, i, arr) => (
          <div key={i} style={{ padding: "16px 12px", background: "#e4e7f3", borderRight: i < arr.length - 1 ? "1px solid #bfc4cb" : "none", textAlign: "center" }}>
            <StatBlock {...s} />
          </div>
        ))}
      </div>

      <SubHead>The Annual Budget Cycle — Six Steps</SubHead>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px,1fr))", gap: 10, marginBottom: 28 }}>
        {cycle.map((step) => (
          <div key={step.n} style={{ padding: "14px 16px", background: "#e4e7f3", borderLeft: "3px solid #a8322c", borderRadius: "0 6px 6px 0" }}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 6 }}>
              <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 900, fontSize: 20, color: "#a8322c", lineHeight: 1 }}>{step.n}</span>
              <span style={{ fontWeight: 800, fontSize: 13 }}>{step.title}</span>
            </div>
            <p style={{ fontSize: 12, lineHeight: 1.65, color: "#555", margin: 0 }}>{step.body}</p>
          </div>
        ))}
      </div>

      {/* ── Household Analogy Sidebar ── */}
      <div style={{
        background: "#f5f6f8", border: "1px solid #ecd9a6", borderLeft: "4px solid #8a5a00",
        borderRadius: "0 8px 8px 0", padding: "18px 20px", marginBottom: 28
      }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "2px", color: "#8a5a00", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10 }}>
          📋 HOW TO FOLLOW THE MONEY — A HOUSEHOLD ANALOGY
        </div>
        <p style={{ fontSize: 13, fontWeight: 700, margin: "0 0 12px", color: "#0b1540" }}>
          Imagine your household earns $10,000/month and budgets $10,000 in expenses.
          You actually only spend $8,500. Here's what Berkeley does with that $1,500:
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px,1fr))", gap: 10, marginBottom: 14 }}>
          {[
            { step: "What a normal household does", desc: "Note the $1,500 surplus. Put it in savings or reduce next month's budget.", color: "#1f6b4a" },
            { step: "What Berkeley does", desc: "Quietly roll that $1,500 into next month as extra spending authority — on top of the new $10,000 budget. Don't mention it.", color: "#a8322c" },
          ].map((item, i) => (
            <div key={i} style={{ background: i === 0 ? "#e3efe9" : "#fbeeed", borderRadius: 6, padding: "12px 14px", border: `1px solid ${i === 0 ? "#bfdccb" : "#efcfcc"}` }}>
              <div style={{ fontSize: 10, fontWeight: 800, color: item.color, letterSpacing: "1px", marginBottom: 6, fontFamily: "'JetBrains Mono', monospace" }}>{item.step.toUpperCase()}</div>
              <div style={{ fontSize: 12, lineHeight: 1.65, color: "#333" }}>{item.desc}</div>
            </div>
          ))}
        </div>
        <p style={{ fontSize: 12, lineHeight: 1.75, color: "#555", margin: "0 0 10px" }}>
          Do that for three years and you've built a hidden pool of carry-forward money — tens of thousands of dollars
          that doesn't show up in your stated monthly budget. Then one month you tell your spouse:
          <em> "We have a $1,500 monthly deficit. We need you to get a second job."</em>
          But you never mentioned the hidden pool. <strong style={{ color: "#a8322c" }}>That's the AAO.</strong>
        </p>
        <div style={{ background: "#f5f6f8", borderRadius: 6, padding: "10px 14px", border: "1px solid #ecd9a6" }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#6b4500", marginBottom: 5 }}>On the numbers: All Funds vs. General Fund</div>
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
        The FY2025 ACFR (MD&A) notes that the FY26 budget update, though balanced, relies on one-time
        measures to close the gap. Here's what those measures were, in plain language:
      </p>
      <div style={{ border: "1px solid #bfc4cb", borderRadius: 6, overflow: "hidden", marginBottom: 20 }}>
        <div style={{ background: "#000d6b", color: "#fff", padding: "9px 14px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 10, fontWeight: 800, letterSpacing: "1.5px", fontFamily: "'JetBrains Mono', monospace" }}>FY26 ONE-TIME BALANCING MEASURES</span>
          <span style={{ fontSize: 10, fontWeight: 800, fontFamily: "'JetBrains Mono', monospace" }}>~$20M TOTAL</span>
        </div>
        {patches.map((item, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8, padding: "10px 14px", borderBottom: i < patches.length - 1 ? "1px solid #d3d6db" : "none", background: i % 2 === 0 ? "#fbeeed" : "#fff" }}>
            <div>
              <span style={{ fontWeight: 700, fontSize: 12 }}>{item.source}</span>
              <span style={{ fontSize: 11, color: "#888", display: "block", marginTop: 2 }}>{item.note}</span>
            </div>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 800, fontSize: 13, color: "#a8322c", whiteSpace: "nowrap" }}>
              {item.amount ? `$${item.amount}M` : "~est."}
            </span>
          </div>
        ))}
      </div>

      <SubHead>Three Years of Rolling Unspent Money (All Funds)</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        Each November, AAO#1 carries unspent prior-year appropriations into the new fiscal year across <em>all</em> city funds.
        The <strong style={{ color: "#a8322c" }}>red bars</strong> are true unspent carryovers.
        The <strong style={{ color: "#8a5a00" }}>amber bars</strong> are encumbrances — money contracted but not yet paid.
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
          { label: "Unspent Carryovers", value: row.carryover, color: "#a8322c" },
          { label: "Encumbrances (committed, unpaid)", value: row.encumbered, color: "#8a5a00" },
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
                <div style={{ height: 7, background: "#d3d6db", borderRadius: 2 }}>
                  <div style={{ height: "100%", width: `${(bar.value / maxVal) * 100}%`, background: bar.color, borderRadius: 2, transition: "width 0.8s ease" }} />
                </div>
              </div>
            ))}
          </div>
        );
      })}

      <SubHead>Policy Questions Worth Asking</SubHead>
      {policyPoints.map((v, i) => (
        <div key={i} style={{ marginBottom: 10, padding: "13px 15px", background: "#e4e7f3", border: `1px solid ${v.color}44`, borderLeft: `4px solid ${v.color}`, borderRadius: "0 6px 6px 0" }}>
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
        <div style={{ marginTop: 10, fontWeight: 700, fontSize: 13, color: "#6b4500" }}>
          A simple, annual plain-language budget summary — showing what carried forward, what was transferred, and what the real structural gap is — would go a long way toward the informed electorate Berkeley says it values.
        </div>
      </Callout>
    </>
  );
}

function NumbersSection() {
  return (
    <>
      <SectionTitle color="#002198">THE NUMBERS</SectionTitle>
      <p style={{ fontSize: 14, lineHeight: 1.7, marginBottom: 24, color: "#333", fontWeight: 600 }}>
        Berkeley is a well-funded city — its adopted FY2027 budget is <strong>$905M</strong> across all funds, and audited FY2025 revenues were $620M.
        Understanding where that money goes, and how the budget is balanced each year,
        gives residents the context they need before any vote on new taxes.
      </p>

      {/* ── Excess Equity Explainer ── */}
      <div style={{ background: "#000d6b", color: "#ebecee", padding: "18px 20px", borderRadius: 8, marginBottom: 24 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "2px", color: "#cfd8ff", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10 }}>
          KEY CONCEPT: EXCESS EQUITY
        </div>
        <p style={{ fontSize: 13, lineHeight: 1.75, margin: 0, color: "#e4e7f3" }}>
          <strong style={{ color: "#fff" }}>Excess equity</strong> is the balance that accumulates in internal service funds
          and enterprise funds above their stated reserve targets. Berkeley's IT Cost Allocation Fund, Workers' Compensation Fund,
          and other internal accounts had built up surpluses beyond what they needed as reserves.
          When the General Fund faced a structural gap, the City transferred funds from these pools to balance the budget.
          <strong style={{ color: "#cfd8ff" }}> This is a one-time measure — it resolves the current year's gap
          but reduces the cushion those funds were built to maintain going forward.</strong>
        </p>
        <div style={{ marginTop: 14, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 10 }}>
          {[
            { label: "IT Fund Transfer", value: "$6.2M", note: "Excess balance moved to General Fund" },
            { label: "Workers' Comp Transfer", value: "$5.2M", note: "Transferred to GF, FY26 (FY2025 ACFR)" },
            { label: "Pension Trust Transfer", value: "$6.0M", note: "Section 115 Trust — FY26 pension obligations (FY2025 ACFR)" },
            { label: "Measure U1 Applied", value: "$2.5M", note: "Special revenue applied to operating budget" },
          ].map((item, i) => (
            <div key={i} style={{ background: "rgba(255,255,255,0.08)", borderRadius: 6, padding: "10px 12px", border: "1px solid rgba(255,255,255,0.12)" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#cfd8ff", fontFamily: "'JetBrains Mono', monospace" }}>{item.value}</div>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#fff", marginTop: 3 }}>{item.label}</div>
              <div style={{ fontSize: 10, color: "#cfd8ff", marginTop: 2 }}>{item.note}</div>
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
          ["Total Revenues (government-wide)", "$619.6M", "$593.8M", { v: "▲ +4.3% YoY", c: "#1f6b4a" }],
          ["Property Tax (general-purpose levy)", "$148.4M", "$135.7M", { v: "▲ +9.4% YoY", c: "#1f6b4a" }],
          ["General Fund Revenue", "$285.8M", "$261.8M", { v: "▲ +9.2% YoY", c: "#1f6b4a" }],
          ["General Fund Expenditures + transfers out", "$310.9M", "$282.9M", { v: "▲ +9.9% YoY", c: "#a8322c" }],
          ["Stated Structural Deficit", "$27–33M", "—", { v: "Recurring, not one-time", c: "#a8322c" }],
          ["Net Pension Liability", "$686.4M", "$723.8M", { v: "▼ improved slightly", c: "#8a5a00" }],
          ["Net OPEB Liability", "$43.2M", "$83.4M", { v: "▼ improved (restructuring)", c: "#1f6b4a" }],
          ["Unrestricted Net Position", "−$415.2M", "−$400.4M", { v: "▲ Getting worse", c: "#a8322c" }],
          ["Health & Welfare Expenses", "$54.8M", "$44.5M", { v: "▲ +23% in one year", c: "#a8322c" }],
          ["Reserves (Stability $32.8M + Catastrophic $25.5M)", "$58.3M", "—", { v: "21.3% of GF revenue (goal: 20–30%)", c: "#8a5a00" }],
        ]}
      />
      <div style={{ fontSize: 11, color: "#999", marginTop: 6, fontStyle: "italic", marginBottom: 20 }}>
        Source: City of Berkeley ACFR FY2025 (year ended June 30, 2025). City Auditor Jenny Wong, "Berkeley's Financial Condition FY2016–2025" (2026).
      </div>

      {/* ── Revenue vs Expenditure ── */}
      <SubHead>Revenue vs. Expenditure Trends</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        General Fund revenue dipped in FY24 and recovered in FY25. The FY27 columns are the adopted budget: the City projected a $32M gap at baseline and closed it on paper with position cuts and re-based personnel costs.
        Meanwhile, expenditures have grown each year. The gap reflects benefit cost growth that consistently outpaces revenue.
      </p>
      <DataTable
        headers={["", "FY23", "FY24", "FY25", "FY26 adopted", "FY27 baseline", "FY27 adopted"]}
        rows={[
          ["GF Revenue", "$273M", "$262M", "$286M", "$268M", "$297M", "$315M"],
          ["GF Expenditure", "$276M", "$274M", "$277M", "$295M", "$329M", "$314M"],
          [{ v: "Annual Gap", bold: true }, { v: "−$3M", c: "#a8322c" }, { v: "−$12M", c: "#a8322c" }, { v: "+$9M", c: "#1f6b4a" }, { v: "−$27M", c: "#a8322c" }, { v: "−$32M", c: "#a8322c" }, { v: "+$1M", c: "#1f6b4a" }],
        ]}
      />

      {/* ── Personnel Spiral ── */}
      <SubHead>Where the Spending Goes: The Personnel Cost Spiral</SubHead>
      <p style={{ fontSize: 13, lineHeight: 1.7, marginBottom: 16, color: "#444" }}>
        Per the City's 2023 Foster &amp; Foster study (pre-dating the FY27 re-basing that removed $16.5M of personnel budget), even with <strong>zero raises</strong> total personnel costs would rise from $342M to <strong>$487M</strong> over
        the next decade — a $145M automatic increase driven entirely by benefit cost growth.
        The fringe rate (benefits as a % of payroll) balloons from 65% to <strong>134%</strong>.
      </p>
      <DataTable
        headers={["Cost Driver", "FY2024", "FY2034 (proj.)", "Δ Change"]}
        rows={[
          ["Base Payroll (held flat)", "$208M", "$208M", { v: "$0 change", c: "#333" }],
          ["  ↳ Health Premiums", "$31M", "$96M", { v: "+$65M", c: "#a8322c" }],
          ["  ↳ CalPERS Employer Contribution", "$78M", "$130M", { v: "+$52M", c: "#a8322c" }],
          ["Total Benefits", "$134M", "$279M", { v: "+$145M", c: "#a8322c" }],
          ["Total Personnel", "$342M", "$487M", { v: "+42% auto-growth", c: "#a8322c" }],
          ["Fringe Rate (benefits/payroll)", "65%", "134%", { v: "+69 pts", c: "#a8322c" }],
        ]}
      />

      <Callout type="warning">
        <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 10 }}>
          Putting It in Context
        </div>
        <p style={{ margin: "0 0 10px", fontSize: 13, lineHeight: 1.7 }}>
          General-purpose property tax revenue grew 9% in one year. Audited FY2025 revenues were $620M and the adopted FY2027 budget is $905M across all funds. The General Fund — the roughly $315M the Council can spend at its discretion — is where the deficit lives.
          At the same time, $316M in appropriations moved through the AAO process across all funds over three years,
          and internal fund balances were drawn down to close the FY26 gap.
        </p>
        <p style={{ margin: 0, fontSize: 13, lineHeight: 1.7 }}>
          The structural deficit is real — and it is driven primarily by benefit cost growth that outpaces revenue.
          The reforms needed are known, and comparable cities have implemented versions of them — though the precise savings depend on contract and actuarial data the City has not yet published.
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
      color: "#002198",
      body: "A 0.5% sales tax falls hardest on lower-income residents. Before asking for new revenue, Berkeley should demonstrate it has fully explored internal cost reform. The structural deficit is largely a compensation structure problem, not a revenue shortfall — and there are concrete, measurable steps that can close it.",
      tag: "BALLOT TIMING",
    },
    {
      n: "02",
      title: "Reconsider the $300M Bond Until Capital Backlogs Are Explained",
      color: "#002198",
      body: "Berkeley's unfunded capital need grew from $1.2B to $1.8B in three years — despite Measure FF. Before issuing more debt, voters deserve a clear accounting of why the gap widened and what specifically the new bond would accomplish that existing measures have not.",
      tag: "BALLOT TIMING",
    },
    {
      n: "03",
      title: "Publish a Plain-Language AAO Summary Before Any Tax Vote",
      color: "#002198",
      body: "The annual AAO process moves hundreds of millions in mid-cycle amendments through the consent calendar with minimal public explanation. A one-page summary — total carryovers, total new adjustments, and General Fund impact — should accompany every AAO package sent to Council and posted publicly.",
      tag: "TRANSPARENCY",
    },
    {
      n: "04",
      title: "Bring Employee Pension Cost-Sharing to the Table",
      color: "#174f37",
      body: "Berkeley pays the employee's own 8% CalPERS contribution on their behalf — a negotiated benefit several peer California cities have moved away from. Estimates put this on the order of $16–17M/year, but the precise figure can't be confirmed without the current MOU terms and CalPERS contribution schedules, and any change is a bargained outcome rather than a unilateral lever. We ask that the City open an honest public conversation about what cost-sharing could look like in future MOU negotiations.",
      tag: "COST REFORM",
    },
    {
      n: "05",
      title: "Protect the Section 115 Pension Pre-Funding Trust",
      color: "#174f37",
      body: "The City drew on the Section 115 Trust to balance operations — about $3M in FY2025 and $6M in FY26, roughly $9M over two years (City Auditor; FY2025 ACFR) — precisely the use the 2022 audit warned against. We ask Council to formally clarify the permitted uses of the trust and commit to a replenishment schedule. Long-term pension stability depends on keeping this fund intact.",
      tag: "FIDUCIARY DUTY",
    },
    {
      n: "06",
      title: "Disclose Internal Service Fund Balances Annually",
      color: "#174f37",
      body: "When internal funds like IT Cost Allocation and Workers' Compensation accumulate balances above their reserve targets, those surpluses should be reported to Council and the public — not quietly swept into the General Fund when a budget gap appears. Annual disclosure with target vs. actual comparisons is a reasonable standard.",
      tag: "TRANSPARENCY",
    },
    {
      n: "07",
      title: "Set a Completion Date for the 2022 Audit Recommendations",
      color: "#6b4500",
      body: "The City Auditor's 2022 report made five specific, actionable recommendations. Four years later, none are fully resolved — and the 2026 audit largely repeats them. We ask Council to assign named staff to each recommendation, set a completion timeline, and report quarterly on progress.",
      tag: "ACCOUNTABILITY",
    },
    {
      n: "08",
      title: "Formalize the Vacancy Management Policy",
      color: "#6b4500",
      body: "Berkeley left 44.4 positions unfunded in FY26, saving an estimated $8–10M. This reflects a practical judgment that those positions aren't currently essential. We ask that this be made an explicit policy decision rather than an informal workaround — with clear criteria for when positions are backfilled.",
      tag: "FISCAL DISCIPLINE",
    },
  ];

  const tagColors = {
    "BALLOT TIMING":    "#002198",
    "TRANSPARENCY":     "#002198",
    "COST REFORM":      "#174f37",
    "FIDUCIARY DUTY":   "#174f37",
    "ACCOUNTABILITY":   "#6b4500",
    "FISCAL DISCIPLINE":"#6b4500",
  };

  return (
    <>
      <SectionTitle color="#002198">OUR POSITION</SectionTitle>

      {/* ── Framing Banner ── */}
      <div style={{ background: "#000d6b", color: "#fff", padding: "20px 22px", borderRadius: 8, marginBottom: 28 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "3px", fontFamily: "'JetBrains Mono', monospace", marginBottom: 10, color: "#cfd8ff" }}>
          THE CASE FOR REFORM BEFORE NEW REVENUE — 2026
        </div>
        <p style={{ fontSize: 14, fontWeight: 600, lineHeight: 1.7, margin: "0 0 14px", color: "#e4e7f3" }}>
          We support Berkeley's long-term fiscal health. That's precisely why we think new taxes should wait
          until the City demonstrates it has addressed the structural issues its own auditors have identified.
          The data shows a management challenge that precedes any revenue shortfall.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 10 }}>
          {[
            { label: "$905M Budget (FY27)", note: "Berkeley is not underfunded" },
            { label: "$316M in AAO Amendments", note: "All-fund mid-cycle moves, minimal public review" },
            { label: "~$20M in Fund Transfers", note: "Internal equity used to close the FY26 gap" },
            { label: "0 of 5 Audit Recs Done", note: "2022 recommendations, still unresolved in 2026" },
          ].map((item, i) => (
            <div key={i} style={{ background: "rgba(255,255,255,0.08)", borderRadius: 6, padding: "10px 12px", border: "1px solid rgba(255,255,255,0.12)" }}>
              <div style={{ fontSize: 13, fontWeight: 800, fontFamily: "'JetBrains Mono', monospace", color: "#fff" }}>{item.label}</div>
              <div style={{ fontSize: 10, color: "#cfd8ff", marginTop: 3 }}>{item.note}</div>
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
          borderLeft: `4px solid ${d.color}`, background: "#e4e7f3",
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
      <SubHead>A Path to Fiscal Balance — Reform Levers</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The structural deficit is real. The levers below are drawn from comparable California cities and the City
        Auditor's findings. The dollar ranges are <strong>illustrative estimates, not precise projections</strong> —
        several (especially the cost-sharing items) are bargained outcomes that depend on MOU terms and CalPERS/actuarial
        data the City has not yet published. They show the order of magnitude available through internal reform, not a
        guaranteed total. See <a href="/rational-budgeting-process.html" style={{ color: "#002198" }}>The Fix</a> for the
        confidence level behind each lever.
      </p>
      <DataTable
        headers={["Reform", "Est. Annual Savings"]}
        rows={[
          ["Employee cost-sharing on 8% CalPERS contribution", { v: "~$16–17M", c: "#174f37" }],
          ["Negotiate 1–3% UAL cost-sharing in future MOUs", { v: "~$4–6M", c: "#174f37" }],
          ["50/50 OPEB pre-funding split (California state model)", { v: "~$4–6M", c: "#174f37" }],
          ["5% workforce reduction through attrition only", { v: "~$6–9M", c: "#6b4500" }],
          ["Program sunset review + contract renegotiation", { v: "~$4–8M", c: "#6b4500" }],
          [{ v: "Illustrative Total (estimates, not additive certainty)", bold: true }, { v: "$34–46M", c: "#174f37" }],
          [{ v: "Structural deficit to close (FY27–28 proj.)", bold: false }, { v: "$27–33M", c: "#555" }],
        ]}
      />

      <Callout type="warning">
        <div style={{ fontWeight: 800, fontSize: 14, marginBottom: 8 }}>
          Our ask is simple: reform first, then ask.
        </div>
        <p style={{ margin: "0 0 10px", fontSize: 13, lineHeight: 1.75 }}>
          Berkeley has passed significant new revenue measures since 2018 — Measure P (2018), Measure FF (2020), Measure W (2024),
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
      outcome: "Goal replaced in July 2025: 20–30% of GF revenues within ten years (was 30% by FY 2027). Reserves at 21.3% in FY 2025. City drew $3M from Section 115 Trust in FY 2025.",
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
    "Not Addressed": { bg: "#fbeeed", border: "#efcfcc", color: "#7a221d", label: "NOT ADDRESSED" },
    "Backsliding":   { bg: "#fbeeed", border: "#efcfcc", color: "#a8322c", label: "BACKSLIDING" },
    "Partial":       { bg: "#fbf1dc", border: "#ecd9a6", color: "#6b4500", label: "PARTIAL" },
    "Addressed":     { bg: "#e3efe9", border: "#bfdccb", color: "#1f6b4a", label: "ADDRESSED" },
  };

  const patchItems = [
    { source: "Section 115 Pension Trust", amount: "$6.0M", note: "FY26 pension obligations (FY2025 ACFR, MD&A)" },
    { source: "IT Cost Allocation Fund balance", amount: "$6.2M", note: "Above-target balance transferred to GF, FY26" },
    { source: "Workers' Compensation Fund", amount: "$5.2M", note: "Transferred to GF, FY26 (FY2025 ACFR, MD&A)" },
    { source: "Measure U1 funds", amount: "$2.5M", note: "Special revenue applied to operating budget" },
    { source: "44.4 vacant positions left unfunded", amount: "~$8–10M", note: "Positions deferred rather than eliminated" },
    { source: "11.8 GF positions moved to other funds", amount: "~$2–3M", note: "Costs shifted to non-GF accounts" },
  ];

  const auditDelta = [
    { metric: "Report Framing", v2022: "Pension Liabilities Need Attention", v2026: "Structural Deficit Poses Risk", dir: "worse" },
    { metric: "Expense Growth (inflation-adj.)", v2022: "+20% over decade", v2026: "+33% over decade", dir: "worse" },
    { metric: "Structural Deficit", v2022: "Not identified", v2026: "$32–33M projected FY27–28", dir: "worse" },
    { metric: "Unfunded Capital Needs", v2022: "$1.2B", v2026: "$1.8B (+50% in 3 yrs)", dir: "worse" },
    { metric: "Pension Funded Ratio", v2022: "66% (FY20) — HIGH RISK", v2026: "66% (FY24) — still HIGH RISK", dir: "flat" },
    { metric: "Unrestricted Net Position", v2022: "−$400.4M (FY24)", v2026: "−$415.2M (FY25)", dir: "worse" },
    { metric: "Section 115 Trust (per audit)", v2022: "$12.1M; missed targets", v2026: "$29.5M — then City raided $3M", dir: "worse" },
    { metric: "Reserve Goal", v2022: "Target 30% by FY 2027", v2026: "Reset to 20–30% within ten years (July 2025); at 21.3%", dir: "flat" },
    { metric: "Median Household Income (real)", v2022: "+11% growth", v2026: "+1% growth, 2016–2024", dir: "worse" },
    { metric: "Net OPEB Liability", v2022: "+91% over decade", v2026: "Declined to $43.2M (FY25)", dir: "better" },
  ];

  const dirStyle = { worse: "#a8322c", flat: "#8a5a00", better: "#1f6b4a" };
  const dirLabel = { worse: "▼ Worse", flat: "► Flat", better: "▲ Better" };

  return (
    <>
      <SectionTitle color="#002198">THE AUDIT RECORD</SectionTitle>
      <p style={{ fontSize: 13, color: "#555", marginBottom: 24, lineHeight: 1.6 }}>
        Berkeley's City Auditor has issued two comprehensive financial condition reports using the same ICMA methodology —
        in 2022 (covering FY 2012–2021) and 2026 (covering FY 2016–2025). Comparing them side by side shows
        where conditions have improved, held steady, or worsened — and how the City has responded to
        the five specific recommendations made in 2022.
      </p>

      {/* ── Bridge: the full audit record beyond the 2022 five ── */}
      <div style={{ background: "#000d6b", color: "#e4e7f3", padding: "16px 18px", borderRadius: 8, marginBottom: 24 }}>
        <div style={{ fontSize: 10, fontWeight: 800, letterSpacing: "2px", color: "#cfd8ff", fontFamily: "'JetBrains Mono', monospace", marginBottom: 8 }}>
          BEYOND THESE FIVE — THE FULL AUDIT RECORD
        </div>
        <p style={{ fontSize: 13, lineHeight: 1.7, margin: "0 0 8px" }}>
          The five recommendations below come from one report — the 2022 financial-condition audit. Across the City
          Auditor's full record of <strong>54 audits and 384 recommendations</strong>, about <strong>265 (69%) have been
          implemented</strong>, <strong>76 dropped</strong> (many by simply lapsing after five years), and <strong>43 remain
          open</strong> — with the weakest follow-through in the highest-spending departments (Public Works ~33%, City
          Manager ~50%).
        </p>
        <p style={{ fontSize: 12, lineHeight: 1.6, margin: 0, color: "#cfd8ff" }}>
          See <a href="/rational-budgeting-process.html" style={{ color: "#cfd8ff" }}>The Fix</a> for how that record maps
          to specific budget reforms.
        </p>
      </div>

      {/* ── Audit Comparison ── */}
      <SubHead>2022 Audit vs. 2026 Audit: What Changed</SubHead>
      <div style={{ overflowX: "auto", marginBottom: 8 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, minWidth: 560 }}>
          <thead>
            <tr style={{ background: "#0b1540", color: "#fff" }}>
              {["Indicator", "2022 Audit Finding", "2026 Audit Finding", ""].map((h, i) => (
                <th key={i} style={{ padding: "9px 12px", textAlign: "left", fontSize: 10, fontWeight: 700, letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {auditDelta.map((row, i) => (
              <tr key={i} style={{ borderBottom: "1px solid #d3d6db", background: i % 2 === 0 ? "#e4e7f3" : "transparent" }}>
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
        <strong style={{ color: "#7a221d" }}>The OPEB improvement is real</strong> — net OPEB liability fell from $83M to $43M in FY25,
        partly due to favorable actuarial assumptions and benefit restructuring. But it's the one bright spot in an otherwise
        deteriorating picture. Pension liabilities remain at $686M, the structural deficit has arrived, and the capital backlog
        grew another $600M in just three years.
      </Callout>

      {/* ── Recommendations Scorecard ── */}
      <SubHead>2022 Audit Recommendations: Where Things Stand</SubHead>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 14, lineHeight: 1.6 }}>
        The 2022 audit made five specific recommendations. The 2026 audit publishes no status table for them; the ratings below are BeTH's reading of what the 2026 audit reports on each subject.
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
        The FY2025 ACFR notes that the FY26 budget update used one-time measures to close the structural gap.
        These measures addressed the current year but don't resolve the underlying cost trends.
      </p>
      <div style={{ border: "1px solid #bfc4cb", borderRadius: 6, overflow: "hidden", marginBottom: 16 }}>
        <div style={{ background: "#000d6b", color: "#fff", padding: "8px 14px", fontSize: 10, fontWeight: 800, letterSpacing: "1.5px", fontFamily: "'JetBrains Mono', monospace" }}>
          FY26 ONE-TIME BALANCING MEASURES (~$20M)
        </div>
        {patchItems.map((item, i) => (
          <div key={i} style={{
            display: "flex", justifyContent: "space-between", alignItems: "baseline",
            flexWrap: "wrap", gap: 8,
            padding: "9px 14px", borderBottom: i < patchItems.length - 1 ? "1px solid #d3d6db" : "none",
            background: i % 2 === 0 ? "#fbeeed" : "#fff"
          }}>
            <div>
              <span style={{ fontWeight: 700, fontSize: 12 }}>{item.source}</span>
              <span style={{ fontSize: 11, color: "#888", marginLeft: 10 }}>{item.note}</span>
            </div>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 800, fontSize: 13, color: "#a8322c", whiteSpace: "nowrap" }}>{item.amount}</span>
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
          ["Net Pension Liability", "$686.4M", "$723.8M", { v: "▼ $37M", c: "#1f6b4a" }],
          ["Net OPEB Liability", "$43.2M", "$83.4M", { v: "▼ $40M", c: "#1f6b4a" }],
          ["Unrestricted Net Position", "−$415.2M", "−$400.4M", { v: "▲ $14M worse", c: "#a8322c" }],
          ["Health & Welfare Expenses", "$54.8M", "$44.5M", { v: "▲ +23%", c: "#a8322c" }],
          ["Public Safety Expenses", "$162.3M", "$190.0M", { v: "▼ −15%", c: "#1f6b4a" }],
          ["Property Tax (general-purpose levy)", "$148.4M", "$135.7M", { v: "▲ +9.4%", c: "#1f6b4a" }],
          ["Reserves (Stability + Catastrophic)", "$58.3M", "—", { v: "21.3% of GF revenue", c: "#8a5a00" }],
          ["Section 115 Trust balance", "$29.5M", "—", { v: "$3M drawn FY25; $6M more in FY26", c: "#a8322c" }],
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
      <SectionTitle color="#002198">HOW BERKELEY COMPARES</SectionTitle>

      <SubHead>Employee Pension Contributions: Berkeley vs. Everyone</SubHead>
      <div style={{ overflowX: "auto", marginBottom: 8 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, minWidth: 540 }}>
          <thead>
            <tr style={{ background: "#0b1540", color: "#fff" }}>
              {["Entity", "Employee Pays", "Employer Pays", "Notes"].map(h => (
                <th key={h} style={{ padding: "10px 12px", textAlign: h === "Notes" ? "left" : "center", fontSize: 10, fontWeight: 700, letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              ["Berkeley (Classic)", "8% required (9% safety)", "38% misc / 57% fire / 87% police", "Whether the City picks up the 8% under any MOU is unverified"],
              ["Berkeley (PEPRA)", "~50% normal cost", "Remainder + UAL", "Post-2013 hires per state law"],
              ["Escondido", "9% + UAL share", "Remainder", "Cost-sharing since 2018"],
              ["San José", "~11–16%", "Remainder", "Measure B reforms (modified)"],
              ["San Diego (new hires)", "Employee 401(k)", "Match only", "Defined contribution plan"],
              ["CA State (OPEB)", "50% of ADC", "50% of ADC", "Equal split adopted 2015"],
              ["Private Sector (avg)", "6–10% salary", "3–6% match", "Defined contribution (401k)"],
            ].map(([entity, emp, er, note], i) => (
              <tr key={i} style={{ borderBottom: "1px solid #d3d6db", background: i === 0 ? "#fbeeed" : "transparent" }}>
                <td style={{ padding: "9px 12px", fontWeight: 700, fontSize: 12 }}>{entity}</td>
                <td style={{ padding: "9px 12px", textAlign: "center", fontSize: 12, color: i === 0 ? "#a8322c" : "#333", fontWeight: i === 0 ? 700 : 400 }}>{emp}</td>
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
        moved away from it. The cost to Berkeley taxpayers is estimated on the order of <strong>$16–17M/year</strong> —
        though the exact figure requires the MOU terms and CalPERS contribution schedules to confirm.
      </Callout>

      <SubHead>CalPERS Funded Status: Berkeley vs. Benchmarks</SubHead>
      {[
        ["Sonoma County (SCERA)", 93, "#1f6b4a"],
        ["Well-Funded Threshold", 90, "#1f6b4a"],
        ["Berkeley Fire", 72.0, "#a8322c"],
        ["Berkeley Misc", 73.6, "#a8322c"],
        ["CalPERS system-wide (June 2024)", 75, "#8a5a00"],
        ["Berkeley Police", 62.9, "#a8322c"],
      ].map(([name, pct, color]) => (
        <div key={name} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 600, marginBottom: 3 }}>
            <span>{name}</span>
            <span style={{ color, fontFamily: "'JetBrains Mono', monospace" }}>{pct}%</span>
          </div>
          <div style={{ height: 7, background: "#d3d6db", borderRadius: 2, overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 2, transition: "width 0.8s ease" }} />
          </div>
        </div>
      ))}

      <SubHead>What Voters Are Already Being Asked (Nov 2026)</SubHead>
      <div style={{ fontSize: 12, lineHeight: 1.5 }}>
        {[
          ["0.5% City Sales Tax", "~$9–10M/yr", "General Fund deficit"],
          ["$300M GO Bond", "$22.14 per $100k AV / yr", "Infrastructure capital"],
          ["Regional Transit Tax (SB63)", "0.5% sales tax (authorized)", "BART / AC Transit"],
          ["Arts & Creative Economy Parcel Tax", "TBD", "Performing arts orgs"],
        ].map(([name, cost, purpose]) => (
          <div key={name} style={{ display: "flex", gap: 8, borderBottom: "1px dotted #ddd", padding: "7px 0", alignItems: "baseline", flexWrap: "wrap" }}>
            <span style={{ fontWeight: 700, minWidth: 220 }}>{name}</span>
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "#a8322c", minWidth: 120 }}>{cost}</span>
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
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #ecd9a6", fontWeight: 700 }}>
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
  return <h3 style={{ fontSize: 14, fontWeight: 700, margin: "28px 0 14px", fontFamily: "'Jost', 'Helvetica Neue', Arial, sans-serif" }}>{children}</h3>;
}
function GroupHead({ children }) {
  return (
    <h3 style={{
      fontSize: 12, fontWeight: 800, letterSpacing: "1.5px", textTransform: "uppercase",
      margin: "28px 0 12px", paddingBottom: 8, borderBottom: "2px solid #d3d6db",
      fontFamily: "'JetBrains Mono', monospace", color: "#0b1540"
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
          <tr style={{ background: "#0b1540", color: "#fff" }}>
            {headers.map((h, i) => (
              <th key={i} style={{ padding: "8px 12px", textAlign: i === 0 ? "left" : "right", fontSize: 10, fontWeight: 700, letterSpacing: "1px" }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, ri) => (
            <tr key={ri} style={{ borderBottom: "1px solid #d3d6db", background: typeof row[0] === "object" && row[0].bold ? "#fbeeed" : row[0]?.toString().startsWith("  ") ? "#e4e7f3" : "transparent" }}>
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
  const [deepOpen, setDeepOpen] = useState(false);
  const contentRef = useRef(null);

  useEffect(() => {
    contentRef.current?.scrollTo({ top: 0, behavior: "smooth" });
  }, [tab]);

  const sections = [ShellGameSection, NumbersSection, AuditSection, CarryoverTracker, DemandsSection, CompareSection];
  const ActiveSection = sections[tab];

  // Section tabs (rendered inline) vs. deep-dive link pages (grouped in a dropdown)
  const sectionTabs = TABS.filter((t) => !t.href);
  const linkTabs = TABS.filter((t) => t.href);

  return (
    <div style={{ fontFamily: "'Jost', 'Helvetica Neue', Arial, sans-serif", maxWidth: 820, margin: "0 auto", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* ── HEADER ── */}
      <header style={{
        background: "#000d6b", color: "#ebecee",
        padding: "clamp(24px,5vw,40px) clamp(20px,4vw,36px) clamp(20px,4vw,32px)",
        position: "relative", overflow: "hidden"
      }}>
        <div style={{
          position: "absolute", top: 0, right: 0, width: "40%", height: "100%",
          background: "repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(196,30,30,0.06) 10px, rgba(196,30,30,0.06) 20px)"
        }} />
        <div style={{ position: "relative" }}>
          <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "3px", textTransform: "uppercase", color: "#a8322c", marginBottom: 8, fontFamily: "'JetBrains Mono', monospace" }}>
            BERKELEY TRANSPARENCY HUB — FISCAL BRIEF
          </div>
          <h1 style={{
            fontSize: "clamp(28px,5vw,42px)", fontWeight: 900, lineHeight: 1.08, margin: 0,
            fontFamily: "'Copperplate', 'Copperplate Gothic Bold', 'Cinzel', serif"
          }}>
            Berkeley's Budget:<br />What the Data Shows
          </h1>
          <p style={{ fontSize: "clamp(13px,2vw,15px)", color: "#aaa", marginTop: 12, maxWidth: 560, lineHeight: 1.55 }}>
            Berkeley's adopted FY2027 budget is $905M across all funds; about $315M of it is the General Fund. Understanding how those funds are appropriated,
            carried forward, and balanced is essential context for any conversation about new taxes in 2026.
          </p>
          <div style={{ display: "flex", gap: 16, marginTop: 18, flexWrap: "wrap", alignItems: "center" }}>
            <div style={{
              padding: "6px 18px", border: "2px solid #a8322c", color: "#a8322c",
              fontSize: 11, fontWeight: 800, letterSpacing: "2.5px", textTransform: "uppercase",
              fontFamily: "'JetBrains Mono', monospace"
            }}>
              REFORM BEFORE NEW REVENUE
            </div>
            <div style={{ fontSize: 11, color: "#888" }}>
              $33M structural deficit · closeable through internal reform · audit findings unresolved
            </div>
          </div>
          <div style={{ marginTop: 14, fontSize: 12, color: "#888", fontFamily: "'JetBrains Mono', monospace" }}>
            Prefer the neutral, non-advocacy data? See the <a href="https://learn-about-berkeley.vercel.app/" target="_blank" rel="noopener" style={{ color: "#cfd8ff", fontWeight: 700 }}>Berkeley Transparency Hub &#8599;</a>
          </div>
        </div>
      </header>

      {/* ── TAB NAV ── */}
      <nav style={{
        display: "flex", borderBottom: "2px solid #000d6b",
        background: "#e4e7f3", position: "sticky", top: 0, zIndex: 10
      }}>
        {sectionTabs.map((t, i) => (
          <button
            key={t.key}
            onClick={() => setTab(i)}
            style={{
              flex: 1, padding: "12px 8px", border: "none", cursor: "pointer",
              fontSize: 10, fontWeight: 800, letterSpacing: "1.5px",
              background: tab === i ? "#000d6b" : "transparent",
              color: tab === i ? "#ebecee" : "#000d6b",
              transition: "all 0.15s",
              fontFamily: "'JetBrains Mono', monospace",
              borderRight: "1px solid #ddd"
            }}
          >
            {t.label}
          </button>
        ))}

        {/* Deep-dive pages grouped under a dropdown */}
        <div
          style={{ position: "relative", flex: 1 }}
          onMouseLeave={() => setDeepOpen(false)}
        >
          <button
            onClick={() => setDeepOpen((o) => !o)}
            aria-expanded={deepOpen}
            style={{
              width: "100%", padding: "12px 8px", border: "none", cursor: "pointer",
              fontSize: 10, fontWeight: 800, letterSpacing: "1.5px",
              background: deepOpen ? "#000d6b" : "transparent",
              color: deepOpen ? "#ebecee" : "#000d6b",
              transition: "all 0.15s", fontFamily: "'JetBrains Mono', monospace"
            }}
          >
            DEEP DIVES {deepOpen ? "▴" : "▾"}
          </button>
          {deepOpen && (
            <div style={{
              position: "absolute", top: "100%", right: 0, minWidth: 190,
              background: "#000d6b", zIndex: 20,
              boxShadow: "0 8px 20px rgba(0,0,0,0.22)", borderRadius: "0 0 4px 4px", overflow: "hidden"
            }}>
              {linkTabs.map((t) => (
                <button
                  key={t.key}
                  onClick={() => { if (t.external) { window.open(t.href, "_blank", "noopener"); } else { window.location.href = t.href; } }}
                  style={{
                    display: "block", width: "100%", textAlign: "left",
                    padding: "12px 16px", border: "none", cursor: "pointer",
                    fontSize: 10, fontWeight: 800, letterSpacing: "1.5px",
                    background: "transparent", color: "#ebecee",
                    borderBottom: "1px solid rgba(255,255,255,0.1)",
                    fontFamily: "'JetBrains Mono', monospace", transition: "background 0.15s"
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(255,255,255,0.1)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
                >
                  {t.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </nav>

      {/* ── HOW TO READ THIS ── */}
      <section style={{
        padding: "clamp(18px,3vw,24px) clamp(20px,4vw,36px)",
        background: "#e4e7f3",
        borderBottom: "1px solid #d3d6db",
        fontFamily: "'Jost', 'Helvetica Neue', Arial, sans-serif",
        color: "#0b1540"
      }}>
        <div style={{
          fontSize: 10, fontWeight: 700, letterSpacing: "2.5px", textTransform: "uppercase",
          color: "#000d6b", marginBottom: 8, fontFamily: "'JetBrains Mono', monospace"
        }}>
          How to read this
        </div>
        <p style={{ fontSize: 14, lineHeight: 1.65, margin: "0 0 10px 0" }}>
          There is no secret pot of money. Berkeley's structural deficit is real —
          roughly <strong>$32–33M a year</strong> in the General Fund, on top of about <strong>$1.8B</strong> in unfunded
          capital needs and <strong>$730M</strong> in pension and retiree-health liabilities. Closing that gap will require cuts, deferrals, new
          revenue, or some mix of the three.
        </p>
        <p style={{ fontSize: 14, lineHeight: 1.65, margin: "0 0 10px 0" }}>
          This site shows where the current budget actually goes, in enough detail that you can
          weigh the tradeoffs yourself. Highlighting a contract or program here is not a claim that
          it is waste — it is an invitation to see what is on the table before decisions get made
          out of public view.
        </p>
        <p style={{ fontSize: 14, lineHeight: 1.65, margin: 0, color: "#555" }}>
          The Berkeley Transparency Hub does not publish its own list of cuts. Those choices belong
          to residents, councilmembers, and city staff.
        </p>
      </section>

      {/* ── CONTENT ── */}
      <main ref={contentRef} style={{ padding: "clamp(20px,4vw,36px)", flex: 1 }}>
        <ActiveSection />
      </main>

      {/* ── FOOTER ── */}
      <footer style={{
        padding: "20px clamp(20px,4vw,36px)", borderTop: "2px solid #000d6b",
        fontSize: 10, color: "#999", lineHeight: 1.6,
        fontFamily: "'JetBrains Mono', monospace"
      }}>
        <strong style={{ color: "#666" }}>Sources:</strong> City of Berkeley Unfunded Liability Obligations Report (Apr 2023); 
        City of Berkeley FY2025 ACFR (pension schedules, June 30, 2024 measurement date); Foster & Foster Pension &amp; OPEB Funding Study (Feb 2023, personnel projections); 
        City of Berkeley FY2024 Revenue Narratives; Daily Californian (Mar 2026); Berkeleyside; CalPERS Circular Letters.
        <div style={{ marginTop: 8, color: "#bbb" }}>
          Compiled by <strong>Berkeley Transparency Hub</strong> · Data as of Spring 2026 ·
          This is a civic transparency resource, not legal or financial advice.
        </div>
        <div style={{ marginTop: 8 }}>
          See also the neutral data hub: <a href="https://learn-about-berkeley.vercel.app/" target="_blank" rel="noopener" style={{ color: "#cfd8ff" }}>Berkeley Transparency Hub — Budget Basics &#8599;</a>
        </div>
      </footer>
      <Analytics />
    </div>
  );
}
