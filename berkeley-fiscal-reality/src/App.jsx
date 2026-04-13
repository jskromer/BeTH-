import { useState, useEffect, useRef } from "react";

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
  { key: "problem", label: "THE PROBLEM" },
  { key: "costs", label: "WHERE IT GOES" },
  { key: "solutions", label: "SOLUTIONS" },
  { key: "compare", label: "COMPARISONS" },
];

function ProblemSection() {
  return (
    <>
      <SectionTitle color="#c41e1e">THE SCALE OF THE PROBLEM</SectionTitle>

      <div style={{
        display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        border: "2px solid #1a1a1a", borderRadius: 8, overflow: "hidden", marginBottom: 28
      }}>
        {[
          { value: "$3.1B", label: "Total Unfunded", sub: "Pension + OPEB + Infrastructure" },
          { value: "$614M", label: "Pension & OPEB", sub: "72% funded overall" },
          { value: "$2.5B", label: "Infrastructure", sub: "FY24–FY28 deferred needs" },
        ].map((s, i) => (
          <div key={i} style={{ padding: "16px 12px", background: "#faf8f5", borderRight: i < 2 ? "1px solid #e0dcd6" : "none", textAlign: "center" }}>
            <StatBlock {...s} />
          </div>
        ))}
      </div>

      <SubHead>CalPERS Pension — % of Commitment Funded</SubHead>
      <FundingBar label="Miscellaneous Employees" funded={80.1} unfundedDollars={234.9} color="#d4860b" />
      <FundingBar label="Police Safety" funded={68.7} unfundedDollars={151.3} color="#8b2020" />
      <FundingBar label="Fire Safety" funded={80.9} unfundedDollars={58.6} color="#d4860b" />

      <SubHead>Retiree Healthcare (OPEB) — % of Commitment Funded</SubHead>
      <FundingBar label="Police Retiree Income (closed)" funded={7.1} unfundedDollars={60.2} color="#8b0000" />
      <FundingBar label="Police Health Premium (new)" funded={6.9} unfundedDollars={34.7} color="#8b0000" />
      <FundingBar label="Fire Retiree Health" funded={38.6} unfundedDollars={20.1} color="#d4860b" />
      <FundingBar label="Non-Safety Retiree Health" funded={51.2} unfundedDollars={30.0} color="#d4860b" />

      <Callout type="danger">
        <strong style={{ color: "#8b0000" }}>Critical:</strong> Police retiree plans are less than 7% funded — 
        essentially pay-as-you-go. The city's actuary recommends an additional <strong>$8.8M/year for 20 years</strong> to 
        fully pre-fund OPEB liabilities. Without action, these costs will consume an ever-larger share of the General Fund.
      </Callout>

      <SubHead>Top Infrastructure Gaps (FY24–FY28)</SubHead>
      <div style={{ fontSize: 12, lineHeight: 1.4 }}>
        {[
          ["Storm Water & Green Infrastructure", 362],
          ["City Buildings (56 facilities)", 314.5],
          ["Fire Facilities", 288],
          ["Streets & Roads (215 mi, PCI 56)", 248.8],
          ["Sewers (255 mi mains)", 183.5],
          ["Bike, Pedestrian & Transit Plans", 182],
          ["Waterfront (docks, pilings, bldgs)", 161],
          ["Parks, Pools & Camps", 145],
          ["Undergrounding (15 mi evac routes)", 109],
          ["Vets & Old City Hall Seismic", 110],
          ["Transfer Station Replacement", 76],
          ["Sidewalks & Pathways (400 mi)", 60],
        ].map(([name, val]) => (
          <div key={name} style={{ display: "flex", justifyContent: "space-between", borderBottom: "1px dotted #ddd", padding: "6px 0" }}>
            <span>{name}</span>
            <span style={{ fontWeight: 700, fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>${val}M</span>
          </div>
        ))}
      </div>
    </>
  );
}

function CostsSection() {
  return (
    <>
      <SectionTitle color="#c41e1e">WHERE THE MONEY GOES</SectionTitle>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16, marginBottom: 28 }}>
        {[
          { label: "Annual CalPERS Payment", value: "$72M", sub: "→ Growing to $108M by FY2034", color: "#c41e1e" },
          { label: "General Fund Deficit", value: "$27M", sub: "Structural, recurring annually", color: "#c41e1e" },
          { label: "Budgeted FTEs", value: "1,792", sub: "Personnel = 57% of General Fund", color: "#1a1a1a" },
        ].map((d, i) => (
          <div key={i} style={{ padding: 18, background: "#faf8f5", border: "1px solid #e0dcd6", borderRadius: 8 }}>
            <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: "1.5px", color: "#888", textTransform: "uppercase" }}>{d.label}</div>
            <div style={{ fontSize: 34, fontWeight: 900, color: d.color, fontFamily: "'JetBrains Mono', monospace", marginTop: 4 }}>{d.value}</div>
            <div style={{ fontSize: 11, color: "#666", marginTop: 4 }}>{d.sub}</div>
          </div>
        ))}
      </div>

      <SubHead>The Personnel Cost Spiral (Zero COLA Scenario)</SubHead>
      <p style={{ fontSize: 13, lineHeight: 1.7, marginBottom: 16, color: "#444" }}>
        Even with <strong>no raises at all</strong>, total personnel costs are projected to rise from $342M to <strong>$487M</strong> over 
        a decade — a $145M increase driven entirely by benefit cost growth. The fringe rate balloons from 65% to <strong>134%</strong> of payroll.
      </p>

      <DataTable
        headers={["Cost Driver", "FY2024", "FY2034", "Δ Change"]}
        rows={[
          ["Base Payroll", "$208M", "$208M", { v: "$0 (held flat)", c: "#333" }],
          ["Total Benefits", "$134M", "$279M", { v: "+$145M", c: "#c41e1e" }],
          ["  ↳ Health Premiums", "$31M", "$96M", { v: "+$65M", c: "#c41e1e" }],
          ["  ↳ CalPERS Employer", "$78M", "$130M", { v: "+$52M", c: "#c41e1e" }],
          ["Total Personnel", "$342M", "$487M", { v: "+$145M", c: "#c41e1e" }],
          ["Fringe Rate", "65%", "134%", { v: "+69 pts", c: "#c41e1e" }],
        ]}
      />

      <Callout type="warning">
        <strong>Key insight:</strong> The deficit is not a revenue problem — General Fund revenue has been essentially flat,
        and actually declined from $273M in FY23 to $262M in FY24. It is a <em>cost structure problem</em> driven by pension
        obligations, retiree healthcare, and negotiated benefits that outpace revenue every single year.
      </Callout>

      <SubHead>Revenue vs. Expenditure Projection</SubHead>
      <DataTable
        headers={["", "FY23", "FY24", "FY25", "FY26", "FY27"]}
        rows={[
          ["GF Revenue", "$273M", "$262M", "$262M", "$268M", "$273M"],
          ["GF Expenditure", "$276M", "$274M", "$294M", "$295M", "$300M"],
          [{ v: "Gap", bold: true }, { v: "−$3M", c: "#c41e1e" }, { v: "−$12M", c: "#c41e1e" }, { v: "−$32M", c: "#c41e1e" }, { v: "−$27M", c: "#c41e1e" }, { v: "−$27M", c: "#c41e1e" }],
        ]}
      />
    </>
  );
}

function SolutionsSection() {
  return (
    <>
      <SectionTitle color="#2a7d4f">CLOSING THE GAP WITHOUT NEW TAXES</SectionTitle>
      <p style={{ fontSize: 13, color: "#666", marginBottom: 24, lineHeight: 1.6 }}>
        The $27M structural deficit can be closed through spending reform alone. These measures total <strong>$30–48M</strong> in annual savings — 
        more than enough without asking residents for a single additional dollar.
      </p>

      <GroupHead>① Employee Pension & Benefits Cost-Sharing</GroupHead>
      <SolutionRow
        title="Stop paying employee's 8% pension share"
        savings="~$16–17M/yr"
        detail="Berkeley pays the employee's own statutory 8% CalPERS contribution on their behalf — a negotiated perk, not a legal requirement. Most peer cities stopped this years ago. Eliminating it alone closes more than half the deficit."
        urgency="high"
      />
      <SolutionRow
        title="Negotiate 1–3% UAL cost-sharing"
        savings="~$4–6M/yr"
        detail="Require employees to contribute 1–3% of salary specifically toward the unfunded accrued liability, as Escondido, San José, and other California cities have done through MOU negotiations."
        urgency="high"
      />
      <SolutionRow
        title="50/50 OPEB pre-funding (follow state model)"
        savings="~$4–6M/yr"
        detail="The State of California itself splits OPEB costs equally between employer and employees (adopted 2015–16). Berkeley should follow suit rather than funding retiree healthcare almost entirely on the taxpayer's dime."
        urgency="high"
      />

      <GroupHead>② Workforce Right-Sizing</GroupHead>
      <SolutionRow
        title="5% FTE reduction through attrition"
        savings="~$6–9M/yr"
        detail="Freeze ~90 of 1,792 positions as they vacate through retirement and attrition. No layoffs required. Average fully-loaded cost per FTE is approximately $190K. Prioritize non-public-safety, non-essential administrative roles."
        urgency="medium"
      />
      <SolutionRow
        title="Targeted layoffs in redundant functions"
        savings="Variable"
        detail="Conduct a zero-based staffing analysis. Identify positions where workload has declined, functions have been automated, or roles duplicate county/regional services. Difficult but necessary if attrition alone is insufficient."
        urgency="low"
      />

      <GroupHead>③ Program Review & Reduction</GroupHead>
      <SolutionRow
        title="Sunset review of all discretionary programs"
        savings="~$3–5M/yr"
        detail="Require every non-mandated program to justify continued funding on a 3-year cycle. Eliminate or consolidate programs with low utilization, overlap with county services, or no measurable outcomes."
        urgency="medium"
      />
      <SolutionRow
        title="Audit & renegotiate community agency contracts"
        savings="~$1–3M/yr"
        detail="The city funds ~$22.6M in homeless services across 33 programs. Audit contracts for effectiveness and redirect funding from underperforming programs to those with demonstrated outcomes per dollar."
        urgency="medium"
      />
      <SolutionRow
        title="Marina Fund — make it self-sustaining"
        savings="Cost avoidance"
        detail="The Marina Fund has a structural deficit and draws General Fund subsidies. Either adjust waterfront fees to cover operations or right-size services to match revenue. Stop using park tax revenue to backfill marina shortfalls."
        urgency="low"
      />

      <GroupHead>④ Structural Reforms</GroupHead>
      <SolutionRow
        title="Cap retiree health at Medicare rates (new hires)"
        savings="Long-term"
        detail="Stop pegging city contributions to Kaiser premiums. Fix a dollar cap tied to Medicare rates for all future hires. Doesn't affect current retirees but dramatically bends the 20-year OPEB cost curve."
        urgency="medium"
      />
      <SolutionRow
        title="Accelerate Section 115 Trust to $50M"
        savings="Rate stabilization"
        detail="The pension trust held only $14.8M against a $25–50M recommended target. Dedicate windfall revenues (one-time transfer tax spikes, unexpected surpluses) to the trust instead of new spending programs."
        urgency="medium"
      />

      <Callout type="dark">
        <div style={{ fontWeight: 800, fontSize: 16, marginBottom: 8, color: "#6fc97f", fontFamily: "'JetBrains Mono', monospace" }}>
          Combined Savings: $30–48M/year
        </div>
        The $27M deficit is closeable without a single new tax. Employee cost-sharing alone ($24–29M) 
        more than covers the gap. Workforce and program reforms provide additional margin for 
        infrastructure investment — without bonding, and without asking residents to pay more.
      </Callout>
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

  const sections = [ProblemSection, CostsSection, SolutionsSection, CompareSection];
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
            The Case for<br />Tax Relief
          </h1>
          <p style={{ fontSize: "clamp(13px,2vw,15px)", color: "#aaa", marginTop: 12, maxWidth: 520, lineHeight: 1.55 }}>
            Berkeley's fiscal crisis is a spending crisis — driven by personnel costs that outpace revenue. 
            Before asking residents for more, the city must reform what it already spends.
          </p>
          <div style={{ display: "flex", gap: 16, marginTop: 18, flexWrap: "wrap", alignItems: "center" }}>
            <div style={{
              padding: "6px 18px", border: "2px solid #c41e1e", color: "#c41e1e",
              fontSize: 11, fontWeight: 800, letterSpacing: "2.5px", textTransform: "uppercase",
              fontFamily: "'JetBrains Mono', monospace"
            }}>
              NO NEW TAXES
            </div>
            <div style={{ fontSize: 11, color: "#666" }}>
              $3.1B unfunded · $27M deficit · Closeable through reform
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
