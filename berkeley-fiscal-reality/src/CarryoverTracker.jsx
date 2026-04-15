import { useState, useMemo } from "react";

/*
  Berkeley Transparency Hub — Carryover Tracker v2
  Three fiscal years of AAO#1 data (FY24, FY25, FY26)
  Tracks zombie appropriations that roll across multiple years
*/

// ── AAO#1 Summary Data (All Funds) ──
const AAO_SUMMARIES = [
  {
    fy: "FY2024", date: "Oct 2023", ordinance: "AAO#1",
    encumbered: 111172378, carryover: 85012551, adjustments: 53672510, total: 249857438,
    gf_encumbered: 16752951, gf_carryover: 13488372, gf_adjustments: 10233450, gf_total: 40474774,
    adopted_gross: 0, note: "First year using 3-AAO cycle"
  },
  {
    fy: "FY2025", date: "Nov 2024", ordinance: "AAO#1",
    encumbered: 111061845, carryover: 137703017, adjustments: 42253338, total: 291018200,
    gf_encumbered: 30334347, gf_carryover: 13233055, gf_adjustments: 4575706, gf_total: 48143108,
    adopted_gross: 793319711, note: "$15M GF shortfall; carryovers constrained"
  },
  {
    fy: "FY2026", date: "Nov 2025", ordinance: "AAO#1",
    encumbered: 145231967, carryover: 93327606, adjustments: 135836181, total: 374395753,
    gf_encumbered: 22721191, gf_carryover: 5446108, gf_adjustments: 20589085, gf_total: 48756384,
    adopted_gross: 829213359, note: "New GF Operating Reserve ($4.2M); $2.8M×3 interest splits"
  },
];

// ── Line Items: FY2024 AAO#1 ──
const FY24_ITEMS = [
  { id: "24-plan-sanpablo", dept: "Planning", item: "San Pablo Specific Plan", amount: 700000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: true, notes: "Part of $2.7M Tier 1 bundle. Appears again in FY2025." },
  { id: "24-plan-bartarea", dept: "Planning", item: "BART Area Specific Plan", amount: 500000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: true, notes: "Part of $2.7M Tier 1 bundle" },
  { id: "24-plan-zorp2", dept: "Planning", item: "ZORP Phase II Revisions", amount: 400000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: false, notes: "" },
  { id: "24-plan-energypol", dept: "Planning", item: "Energy Policy", amount: 300000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: false, notes: "" },
  { id: "24-plan-transimpact", dept: "Planning", item: "Transportation Impact Fee Study", amount: 400000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: false, notes: "" },
  { id: "24-plan-landuseej", dept: "Planning", item: "Land Use & Environmental Justice Element", amount: 400000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: false, notes: "" },
  { id: "24-plan-beso", dept: "Planning", item: "BESO Implementation", amount: 20000, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-plan-pacsteel", dept: "Planning", item: "Pacific Steel CEQA Rezoning", amount: 200000, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "24-pw-evcharge", dept: "Public Works", item: "EV Charging Stations", amount: 1450000, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: true, notes: "ZOMBIE: Carried FY23→FY24→FY25. Three consecutive years." },
  { id: "24-pw-cameras", dept: "Public Works", item: "Cameras in Public Right-of-Way", amount: 1293889, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "partially redirected", zombie: false, notes: "$643,899 reallocated to Measure T1 funding gaps" },
  { id: "24-pw-southside", dept: "Public Works", item: "Southside Complete Streets", amount: 1000000, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "24-pw-facilities", dept: "Public Works", item: "Facilities Capital Projects (various)", amount: 267639, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "24-pw-other", dept: "Public Works", item: "Various PW Capital Projects", amount: 587795, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "24-pw-stair", dept: "Public Works", item: "Stair Center ADA Project", amount: 676807, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: false, notes: "Measure P funded" },
  { id: "24-pw-cleanstreets", dept: "Public Works", item: "Equitable Clean Streets", amount: 202451, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-pw-homeless", dept: "Public Works", item: "Homeless Response Team + Downtown Streets Team", amount: 360176, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "Measure P funded" },
  { id: "24-hhcs-aahrc", dept: "HHCS", item: "African American Holistic Resource Center", amount: 52037, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: true, notes: "ZOMBIE: Reappears in FY2026 AAO#1" },
  { id: "24-hhcs-dataservices", dept: "HHCS", item: "City Data Services / Housing Portal / NextGen", amount: 53838, fy_origin: "FY2023", current_fy: "FY2024", category: "Technology", status: "carried", zombie: true, notes: "ZOMBIE: NextGen invoice still carrying in FY2026" },
  { id: "24-hhcs-fairwork", dept: "HHCS", item: "Fair Work Week / Pref Policy / Harriet Tubman / Social Housing Study", amount: 500000, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "Bundle of policy implementation items" },
  { id: "24-hhcs-gvp", dept: "HHCS", item: "Gender Violence Prevention (CSSII position)", amount: 220000, fy_origin: "FY2023", current_fy: "FY2024", category: "Staffing", status: "carried", zombie: false, notes: "Council referral" },
  { id: "24-hhcs-russell", dept: "HHCS", item: "Russell Street Residence Acquisition", amount: 4500000, fy_origin: "FY2024", current_fy: "FY2024", category: "Capital", status: "new adjustment", zombie: false, notes: "Measure P — largest single new item" },
  { id: "24-cm-langequity", dept: "City Manager", item: "Language Equity (Tier 1)", amount: 15000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: false, notes: "" },
  { id: "24-cm-employer", dept: "City Manager", item: "Employer of Choice – Communication", amount: 200000, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-cm-website", dept: "City Manager", item: "Website Funding", amount: 50000, fy_origin: "FY2023", current_fy: "FY2024", category: "Technology", status: "carried", zombie: false, notes: "" },
  { id: "24-cm-chamber", dept: "City Manager", item: "Berkeley Chamber of Commerce Contract", amount: 43500, fy_origin: "FY2023", current_fy: "FY2024", category: "Contract", status: "carried", zombie: false, notes: "" },
  { id: "24-cm-vet", dept: "City Manager", item: "Relief Veterinarian Services (Animal Shelter)", amount: 65750, fy_origin: "FY2023", current_fy: "FY2024", category: "Contract", status: "carried", zombie: false, notes: "" },
  { id: "24-cm-festival", dept: "City Manager", item: "Festival Grant Budget (Mayor's Office → OED)", amount: 41685, fy_origin: "FY2023", current_fy: "FY2024", category: "Grant", status: "carried", zombie: false, notes: "" },
  { id: "24-nd-ceasefire", dept: "Non-Departmental", item: "Ceasefire Program Staffing (Tier 1)", amount: 1000000, fy_origin: "FY2023", current_fy: "FY2024", category: "Tier 1 Referral", status: "carried", zombie: false, notes: "" },
  { id: "24-nd-jackets", dept: "Non-Departmental", item: "Berkeley Junior Jackets Field Use", amount: 6000, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-pol-retention", dept: "Police", item: "Recruitment & Retention Payments", amount: 84000, fy_origin: "FY2023", current_fy: "FY2024", category: "Staffing", status: "carried", zombie: false, notes: "" },
  { id: "24-pol-bpamou", dept: "Police", item: "Berkeley Police Association MOU", amount: 4300000, fy_origin: "FY2024", current_fy: "FY2024", category: "Staffing", status: "new adjustment", zombie: false, notes: "Resolution No. 71,033-N.S." },
  { id: "24-ca-outside23", dept: "City Attorney", item: "Outside Counsel (FY23 invoices)", amount: 721724, fy_origin: "FY2023", current_fy: "FY2024", category: "Contract", status: "carried", zombie: false, notes: "" },
  { id: "24-ca-outside24", dept: "City Attorney", item: "New Outside Counsel Services", amount: 887600, fy_origin: "FY2024", current_fy: "FY2024", category: "Contract", status: "new adjustment", zombie: false, notes: "" },
  { id: "24-ca-furniture", dept: "City Attorney", item: "Furniture, Travel, Misc Admin", amount: 185167, fy_origin: "FY2023", current_fy: "FY2024", category: "Operations", status: "carried", zombie: false, notes: "" },
  { id: "24-fin-publicbank", dept: "Finance", item: "Public Banking Consultant", amount: 75000, fy_origin: "FY2023", current_fy: "FY2024", category: "Contract", status: "carried", zombie: false, notes: "" },
  { id: "24-fin-erma", dept: "Finance", item: "ERMA Training", amount: 200000, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-fin-taxsoftware", dept: "Finance", item: "Tax Administration Software", amount: 100000, fy_origin: "FY2023", current_fy: "FY2024", category: "Technology", status: "carried", zombie: false, notes: "" },
  { id: "24-hr-contracts", dept: "HR", item: "GovInvest + HR Acuity Contracts", amount: 146000, fy_origin: "FY2023", current_fy: "FY2024", category: "Contract", status: "carried", zombie: false, notes: "" },
  { id: "24-hr-employer", dept: "HR", item: "Employer of Choice – Advertising", amount: 250000, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-council-carry", dept: "Mayor & Council", item: "FY23 Council Carryover", amount: 84893, fy_origin: "FY2023", current_fy: "FY2024", category: "Operations", status: "carried", zombie: false, notes: "" },
  { id: "24-odpa-office", dept: "ODPA", item: "New Office & Move Costs", amount: 67295, fy_origin: "FY2023", current_fy: "FY2024", category: "Operations", status: "carried", zombie: false, notes: "" },
  { id: "24-odpa-casesoft", dept: "ODPA", item: "Case Management Software", amount: 52076, fy_origin: "FY2023", current_fy: "FY2024", category: "Technology", status: "carried", zombie: false, notes: "" },
  { id: "24-odpa-virtra", dept: "ODPA", item: "VIRTRA Virtual Training Simulator", amount: 58118, fy_origin: "FY2023", current_fy: "FY2024", category: "Technology", status: "carried", zombie: false, notes: "" },
  { id: "24-prw-pool", dept: "PRW", item: "West Campus Pool & Solano Peralta Park", amount: 90276, fy_origin: "FY2023", current_fy: "FY2024", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "24-prw-camps", dept: "PRW", item: "Camp Scholarships + DEI Programs", amount: 152711, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-prw-adeline", dept: "PRW", item: "Adeline Median Landscaping", amount: 75000, fy_origin: "FY2024", current_fy: "FY2024", category: "Capital", status: "new adjustment", zombie: false, notes: "" },
  { id: "24-rsb-eviction", dept: "Rent Board", item: "Eviction Moratorium Outreach", amount: 101588, fy_origin: "FY2023", current_fy: "FY2024", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "24-fire-emt", dept: "Fire", item: "Ground EMT Methodology Audit", amount: 125337, fy_origin: "FY2024", current_fy: "FY2024", category: "Contract", status: "new adjustment", zombie: false, notes: "" },
  { id: "24-hhcs-opioid", dept: "HHCS", item: "Social Services Specialist – Opioid Settlement", amount: 86313, fy_origin: "FY2024", current_fy: "FY2024", category: "Staffing", status: "new adjustment", zombie: false, notes: "" },
  { id: "24-oed-visitberk", dept: "City Manager", item: "Visit Berkeley TOT Revenue Contract", amount: 196114, fy_origin: "FY2024", current_fy: "FY2024", category: "Contract", status: "new adjustment", zombie: false, notes: "" },
  { id: "24-odpa-reclass", dept: "ODPA", item: "Reclassification OSIII → Assoc Mgmt Analyst", amount: 63086, fy_origin: "FY2024", current_fy: "FY2024", category: "Staffing", status: "new adjustment", zombie: false, notes: "" },
];

// ── FY2025 AAO#1 ──
const FY25_ITEMS = [
  { id: "25-pw-evcharge", dept: "Public Works", item: "EV Charging Stations", amount: 1200000, fy_origin: "FY2023", current_fy: "FY2025", category: "Capital", status: "carried", zombie: true, notes: "ZOMBIE (3rd year): FY2023→FY2024→FY2025" },
  { id: "25-pw-retaining", dept: "Public Works", item: "Retaining Wall & Storm Drain Repair", amount: 450000, fy_origin: "FY2024", current_fy: "FY2025", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "25-pw-bart", dept: "Public Works", item: "Past Due Payments to BART", amount: 380000, fy_origin: "FY2024", current_fy: "FY2025", category: "Operations", status: "carried", zombie: false, notes: "" },
  { id: "25-pw-hopkins", dept: "Public Works", item: "Hopkins St. Corridor", amount: 500000, fy_origin: "FY2024", current_fy: "FY2025", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "25-pw-urbangreen", dept: "Public Works", item: "Urban Greening Tree Planting", amount: 350000, fy_origin: "FY2024", current_fy: "FY2025", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "25-pw-trees", dept: "Public Works", item: "Trees Make Life Better Grant", amount: 200000, fy_origin: "FY2024", current_fy: "FY2025", category: "Grant", status: "carried", zombie: false, notes: "" },
  { id: "25-hhcs-opioid2", dept: "HHCS", item: "Opioid Settlement Programs (expanded)", amount: 500000, fy_origin: "FY2024", current_fy: "FY2025", category: "Program", status: "carried", zombie: false, notes: "" },
  { id: "25-ca-outside25", dept: "City Attorney", item: "Outside Counsel Services", amount: 900000, fy_origin: "FY2025", current_fy: "FY2025", category: "Contract", status: "new adjustment", zombie: true, notes: "PATTERN: Outside counsel appropriated every year" },
];

// ── FY2026 AAO#1 ──
const FY26_ITEMS = [
  { id: "26-pw-mlkvz", dept: "Public Works", item: "MLK Jr. Vision Zero Quick Build", amount: 600000, fy_origin: "FY2025", current_fy: "FY2026", category: "Capital", status: "carried", zombie: false, notes: "Complete before mid-year" },
  { id: "26-pw-univbus", dept: "Public Works", item: "University Ave. Bus Stop", amount: 450000, fy_origin: "FY2025", current_fy: "FY2026", category: "Capital", status: "carried", zombie: false, notes: "Now in construction" },
  { id: "26-pw-shelter", dept: "Public Works", item: "Animal Shelter Landscape Repair", amount: 150000, fy_origin: "FY2025", current_fy: "FY2026", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "26-pw-uud48", dept: "Public Works", item: "UUD #48 Undergrounding", amount: 800000, fy_origin: "FY2025", current_fy: "FY2026", category: "Capital", status: "carried", zombie: false, notes: "" },
  { id: "26-hhcs-aahrc2", dept: "HHCS", item: "AAHRC Program Development", amount: 75000, fy_origin: "FY2024", current_fy: "FY2026", category: "Program", status: "carried", zombie: true, notes: "ZOMBIE (3rd year): FY2023→FY2024→FY2026" },
  { id: "26-hhcs-nextgen", dept: "HHCS", item: "NextGen Invoice (FY25)", amount: 40000, fy_origin: "FY2025", current_fy: "FY2026", category: "Technology", status: "carried", zombie: true, notes: "ZOMBIE: Data Services/NextGen every AAO since FY2024" },
  { id: "26-hhcs-opioid-mlk", dept: "HHCS", item: "Opioid Settlement – 2636 MLK Jr. MH Services", amount: 350000, fy_origin: "FY2026", current_fy: "FY2026", category: "Program", status: "new adjustment", zombie: false, notes: "New program" },
  { id: "26-hhcs-opioid-ctr", dept: "HHCS", item: "Opioid Settlement – Additional Programs", amount: 250000, fy_origin: "FY2026", current_fy: "FY2026", category: "Program", status: "new adjustment", zombie: false, notes: "" },
  { id: "26-cm-carebridge", dept: "City Manager", item: "Berkeley CareBridge (Options Recovery)", amount: 7510842, fy_origin: "FY2026", current_fy: "FY2026", category: "Contract", status: "new adjustment", zombie: false, notes: "3-year post-arrest diversion & reentry" },
  { id: "26-cm-admin", dept: "City Manager", item: "CareBridge Admin & Evaluation (0.5 FTE)", amount: 409158, fy_origin: "FY2026", current_fy: "FY2026", category: "Staffing", status: "new adjustment", zombie: false, notes: "" },
  { id: "26-allied", dept: "Non-Departmental", item: "Allied Universal Security (amendment)", amount: 1000000, fy_origin: "FY2026", current_fy: "FY2026", category: "Contract", status: "new adjustment", zombie: false, notes: "NTE $5.45M through June 2026" },
  { id: "26-gf-opreserve", dept: "Finance", item: "New GF Operating Reserves Fund", amount: 4177541, fy_origin: "FY2026", current_fy: "FY2026", category: "Reserves", status: "new adjustment", zombie: false, notes: "For FY2027-28 budget balancing" },
  { id: "26-gf-sec115", dept: "Finance", item: "Investment Interest → Section 115 Trust", amount: 2822392, fy_origin: "FY2026", current_fy: "FY2026", category: "Reserves", status: "new adjustment", zombie: false, notes: "Fiscal policy: interest above $6M baseline" },
  { id: "26-gf-reserves", dept: "Finance", item: "Investment Interest → GF Reserves", amount: 2822392, fy_origin: "FY2026", current_fy: "FY2026", category: "Reserves", status: "new adjustment", zombie: false, notes: "55% Stabilization / 45% Catastrophic" },
  { id: "26-gf-capital", dept: "Finance", item: "Investment Interest → Capital", amount: 2822392, fy_origin: "FY2026", current_fy: "FY2026", category: "Reserves", status: "new adjustment", zombie: false, notes: "" },
  { id: "26-gf-excesseq", dept: "Finance", item: "Excess Equity → Reserves", amount: 3177541, fy_origin: "FY2026", current_fy: "FY2026", category: "Reserves", status: "new adjustment", zombie: false, notes: "" },
  { id: "26-prop47", dept: "HHCS", item: "Prop 47 Cohort 5 Grant (BSCC)", amount: 500000, fy_origin: "FY2026", current_fy: "FY2026", category: "Grant", status: "new adjustment", zombie: false, notes: "Reso 71,963-N.S." },
  { id: "26-prw-bench", dept: "PRW", item: "Memorial Benches (donated funds)", amount: 25000, fy_origin: "FY2026", current_fy: "FY2026", category: "Capital", status: "new adjustment", zombie: false, notes: "" },
  { id: "26-tregub1", dept: "Non-Departmental", item: "Addison Catenary Lighting (Tregub)", amount: 500000, fy_origin: "FY2026", current_fy: "FY2026", category: "Tier 1 Referral", status: "new adjustment", zombie: false, notes: "SOSIP/LRDP. Downtown revitalization." },
  { id: "26-tregub2", dept: "Non-Departmental", item: "Oxford for All (Tregub)", amount: 400000, fy_origin: "FY2026", current_fy: "FY2026", category: "Tier 1 Referral", status: "new adjustment", zombie: false, notes: "SOSIP/LRDP. Downtown revitalization." },
  { id: "26-tregub3", dept: "Non-Departmental", item: "Harold Way Placemaking (Tregub)", amount: 300000, fy_origin: "FY2026", current_fy: "FY2026", category: "Tier 1 Referral", status: "new adjustment", zombie: false, notes: "Schematic design." },
  { id: "26-2321tenth", dept: "HHCS", item: "2321 Tenth Street Loan (Reso 71,087)", amount: 800000, fy_origin: "FY2024", current_fy: "FY2026", category: "Capital", status: "carried", zombie: true, notes: "ZOMBIE: Not fully encumbered originally" },
  { id: "26-stpaul", dept: "HHCS", item: "St. Paul Terrace Development Loan", amount: 1200000, fy_origin: "FY2025", current_fy: "FY2026", category: "Capital", status: "carried", zombie: false, notes: "Loan closing est. Nov 2025" },
];

const ALL_ITEMS = [...FY24_ITEMS, ...FY25_ITEMS, ...FY26_ITEMS];
const FISCAL_YEARS = ["All", "FY2024", "FY2025", "FY2026"];
const CATEGORIES = ["All", "Tier 1 Referral", "Capital", "Program", "Contract", "Staffing", "Technology", "Reserves", "Grant", "Operations"];
const fmt = (n) => n >= 1000000 ? "$" + (n/1000000).toFixed(1) + "M" : n >= 1000 ? "$" + (n/1000).toFixed(0) + "K" : "$" + n.toLocaleString();
const fmtFull = (n) => "$" + n.toLocaleString();

function Pill({ label, active, onClick, color }) {
  return (
    <button onClick={onClick} style={{
      padding: "4px 11px", fontSize: "10px", fontWeight: 700, letterSpacing: "0.5px",
      textTransform: "uppercase", border: active ? "none" : "1px solid #d5d0c8",
      borderRadius: 2, background: active ? (color || "#1a1a1a") : "transparent",
      color: active ? "#fffdf9" : "#666", cursor: "pointer",
      fontFamily: "'Source Serif 4', Georgia, serif", transition: "all 0.15s ease",
    }}>{label}</button>
  );
}

const stStyle = (s) => {
  if (s === "carried") return { text: "CARRIED", color: "#c41e1e", bg: "#fdf0f0" };
  if (s === "new adjustment") return { text: "NEW", color: "#2a7d4f", bg: "#f0faf4" };
  if (s === "partially redirected") return { text: "REDIRECT", color: "#d4860b", bg: "#fdf6e8" };
  return { text: s, color: "#666", bg: "#f5f5f5" };
};

export default function CarryoverTracker() {
  const [filterFY, setFilterFY] = useState("All");
  const [filterCat, setFilterCat] = useState("All");
  const [zombieOnly, setZombieOnly] = useState(false);
  const [view, setView] = useState("trend");
  const [expandedId, setExpandedId] = useState(null);
  const [sortBy, setSortBy] = useState("amount");

  const filtered = useMemo(() => {
    let f = ALL_ITEMS;
    if (filterFY !== "All") f = f.filter(i => i.current_fy === filterFY);
    if (filterCat !== "All") f = f.filter(i => i.category === filterCat);
    if (zombieOnly) f = f.filter(i => i.zombie);
    if (sortBy === "amount") f = [...f].sort((a, b) => b.amount - a.amount);
    if (sortBy === "dept") f = [...f].sort((a, b) => a.dept.localeCompare(b.dept));
    if (sortBy === "fy") f = [...f].sort((a, b) => a.current_fy.localeCompare(b.current_fy));
    return f;
  }, [filterFY, filterCat, zombieOnly, sortBy]);

  const zombieCount = ALL_ITEMS.filter(i => i.zombie).length;
  const zombieTotal = ALL_ITEMS.filter(i => i.zombie).reduce((s, i) => s + i.amount, 0);

  const deptTotals = useMemo(() => {
    const map = {};
    filtered.forEach(i => {
      if (!map[i.dept]) map[i.dept] = { total: 0, carried: 0, newAdj: 0, zombie: 0, count: 0 };
      map[i.dept].total += i.amount;
      map[i.dept].count += 1;
      if (i.zombie) map[i.dept].zombie += i.amount;
      if (i.status === "carried" || i.status === "partially redirected") map[i.dept].carried += i.amount;
      else map[i.dept].newAdj += i.amount;
    });
    return Object.entries(map).sort((a, b) => b[1].total - a[1].total);
  }, [filtered]);
  const maxDeptTotal = deptTotals.length > 0 ? deptTotals[0][1].total : 1;

  return (
    <div style={{ fontFamily: "'Source Serif 4', Georgia, serif", maxWidth: 840, margin: "0 auto", background: "#fffdf9", minHeight: "100vh" }}>
      {/* HEADER */}
      <div style={{ background: "#1a1a1a", color: "#fffdf9", padding: "22px 28px 18px", position: "relative", overflow: "hidden" }}>
        <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", background: "repeating-linear-gradient(-45deg, transparent, transparent 12px, rgba(196,30,30,0.04) 12px, rgba(196,30,30,0.04) 24px)" }} />
        <div style={{ position: "relative" }}>
          <div style={{ fontSize: "9px", fontWeight: 700, letterSpacing: "3px", textTransform: "uppercase", color: "#c41e1e", marginBottom: 4 }}>BERKELEY TRANSPARENCY HUB — ACCOUNTABILITY TOOL</div>
          <h1 style={{ fontSize: "26px", fontWeight: 900, lineHeight: 1.1, margin: 0, fontFamily: "'Playfair Display', Georgia, serif" }}>Carryover Tracker</h1>
          <div style={{ fontSize: "12px", color: "#999", marginTop: 5, maxWidth: 560, lineHeight: 1.5 }}>Three years of mid-cycle budget amendments. Tracking the money that was budgeted, never spent, and carried forward through the AAO process.</div>
        </div>
      </div>

      {/* TREND BARS */}
      <div style={{ padding: "16px 28px", background: "#f5f3ee", borderBottom: "1px solid #e0dbd2" }}>
        <div style={{ fontSize: "10px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1.5px", color: "#888", marginBottom: 10 }}>AAO#1 Amendment Size — All Funds (3-Year Trend)</div>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {AAO_SUMMARIES.map(s => (
            <div key={s.fy} style={{ flex: 1, minWidth: 200 }}>
              <div style={{ fontSize: "13px", fontWeight: 800, marginBottom: 4 }}>{s.fy} <span style={{ fontSize: "10px", fontWeight: 400, color: "#999" }}>{s.date}</span></div>
              <div style={{ display: "flex", height: 18, borderRadius: 2, overflow: "hidden", marginBottom: 6 }}>
                <div style={{ width: (s.encumbered / s.total * 100) + "%", background: "#888", height: "100%" }} title="Encumbrances" />
                <div style={{ width: (s.carryover / s.total * 100) + "%", background: "#c41e1e", height: "100%" }} title="Carryovers" />
                <div style={{ width: (s.adjustments / s.total * 100) + "%", background: "#2a7d4f", height: "100%" }} title="Adjustments" />
              </div>
              <div style={{ fontSize: "10px", color: "#666", lineHeight: 1.6 }}>
                <div><strong>Total:</strong> {fmt(s.total)}</div>
                <div>GF: {fmt(s.gf_total)} <span style={{ color: "#c41e1e" }}>(carry: {fmt(s.gf_carryover)})</span></div>
              </div>
              {s.note && <div style={{ fontSize: "9px", color: "#b08020", marginTop: 3, fontStyle: "italic" }}>{s.note}</div>}
            </div>
          ))}
        </div>
        <div style={{ display: "flex", gap: 16, fontSize: "9px", color: "#999", marginTop: 8, justifyContent: "center" }}>
          <span><span style={{ display: "inline-block", width: 10, height: 10, background: "#888", borderRadius: 1, verticalAlign: "middle", marginRight: 4 }} />Encumbered</span>
          <span><span style={{ display: "inline-block", width: 10, height: 10, background: "#c41e1e", borderRadius: 1, verticalAlign: "middle", marginRight: 4 }} />Carryover</span>
          <span><span style={{ display: "inline-block", width: 10, height: 10, background: "#2a7d4f", borderRadius: 1, verticalAlign: "middle", marginRight: 4 }} />Adjustments</span>
        </div>
      </div>

      {/* ZOMBIE CALLOUT */}
      <div style={{ margin: "16px 28px", padding: "14px 18px", background: "#1a1a1a", color: "#fffdf9", borderRadius: 4, display: "flex", gap: 20, alignItems: "center", flexWrap: "wrap" }}>
        <div>
          <div style={{ fontSize: "9px", fontWeight: 700, letterSpacing: "2px", color: "#c41e1e", marginBottom: 2 }}>ZOMBIE APPROPRIATIONS</div>
          <div style={{ fontSize: "12px", lineHeight: 1.5, maxWidth: 460 }}>Items appearing in multiple consecutive AAOs — budgeted, never fully spent, carried forward year after year.</div>
        </div>
        <div style={{ display: "flex", gap: 16, marginLeft: "auto" }}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "24px", fontWeight: 900, color: "#c41e1e" }}>{zombieCount}</div>
            <div style={{ fontSize: "9px", textTransform: "uppercase", letterSpacing: "1px", color: "#888" }}>Identified</div>
          </div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "24px", fontWeight: 900, color: "#c41e1e" }}>{fmt(zombieTotal)}</div>
            <div style={{ fontSize: "9px", textTransform: "uppercase", letterSpacing: "1px", color: "#888" }}>Cumulative $</div>
          </div>
        </div>
      </div>

      {/* FILTERS */}
      <div style={{ padding: "8px 28px" }}>
        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 8 }}>
          <div>
            <div style={{ fontSize: "9px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1.5px", color: "#999", marginBottom: 4 }}>Fiscal Year</div>
            <div style={{ display: "flex", gap: 3 }}>{FISCAL_YEARS.map(f => <Pill key={f} label={f} active={filterFY === f} onClick={() => setFilterFY(f)} />)}</div>
          </div>
          <div>
            <div style={{ fontSize: "9px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1.5px", color: "#999", marginBottom: 4 }}>Category</div>
            <div style={{ display: "flex", gap: 3, flexWrap: "wrap" }}>{CATEGORIES.map(c => <Pill key={c} label={c} active={filterCat === c} onClick={() => setFilterCat(c)} />)}</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
          <Pill label={"Zombies Only (" + zombieCount + ")"} active={zombieOnly} onClick={() => setZombieOnly(!zombieOnly)} color="#c41e1e" />
          <div style={{ marginLeft: "auto", display: "flex", gap: 3 }}>
            <Pill label="Trend" active={view === "trend"} onClick={() => setView("trend")} />
            <Pill label="List" active={view === "list"} onClick={() => setView("list")} />
            <Pill label="Depts" active={view === "dept"} onClick={() => setView("dept")} />
          </div>
        </div>
      </div>

      {/* CONTENT */}
      <div style={{ padding: "8px 28px 32px" }}>
        {view === "trend" && (
          <div>
            <div style={{ fontSize: "11px", fontWeight: 700, marginBottom: 12 }}>General Fund AAO#1 — Year-over-Year</div>
            <div style={{ overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px" }}>
                <thead>
                  <tr style={{ background: "#1a1a1a", color: "#fff" }}>
                    <th style={{ padding: "7px 10px", textAlign: "left" }}>Component</th>
                    {AAO_SUMMARIES.map(s => <th key={s.fy} style={{ padding: "7px 10px", textAlign: "right" }}>{s.fy}</th>)}
                    <th style={{ padding: "7px 10px", textAlign: "right" }}>Δ FY24→26</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { label: "Encumbrances", key: "gf_encumbered" },
                    { label: "Unencumbered Carryover", key: "gf_carryover" },
                    { label: "New Adjustments", key: "gf_adjustments" },
                    { label: "Total GF Amendment", key: "gf_total" },
                  ].map(row => {
                    const vals = AAO_SUMMARIES.map(s => s[row.key]);
                    const delta = vals[2] - vals[0];
                    const isTotal = row.key === "gf_total";
                    return (
                      <tr key={row.key} style={{ borderBottom: "1px solid #e8e4df", background: isTotal ? "#faf8f5" : "transparent" }}>
                        <td style={{ padding: "7px 10px", fontWeight: isTotal ? 700 : 400 }}>{row.label}</td>
                        {vals.map((v, i) => <td key={i} style={{ padding: "7px 10px", textAlign: "right", fontVariantNumeric: "tabular-nums", fontWeight: isTotal ? 700 : 400 }}>{fmt(v)}</td>)}
                        <td style={{ padding: "7px 10px", textAlign: "right", fontWeight: 700, color: delta > 0 ? "#c41e1e" : delta < 0 ? "#2a7d4f" : "#666" }}>{delta > 0 ? "+" : ""}{fmt(delta)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <div style={{ marginTop: 20, fontSize: "11px", fontWeight: 700, marginBottom: 10 }}>All Funds AAO#1 Total</div>
            {AAO_SUMMARIES.map(s => {
              const max = Math.max(...AAO_SUMMARIES.map(x => x.total));
              return (
                <div key={s.fy} style={{ marginBottom: 10 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", marginBottom: 3 }}>
                    <span style={{ fontWeight: 600 }}>{s.fy}</span>
                    <span style={{ color: "#888" }}>{fmt(s.total)}</span>
                  </div>
                  <div style={{ height: 10, background: "#e8e4df", borderRadius: 2, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: (s.total/max*100) + "%", background: "#1a1a1a", borderRadius: 2, transition: "width 0.5s ease" }} />
                  </div>
                </div>
              );
            })}
            <div style={{ marginTop: 16, padding: "12px 16px", background: "#fdf6e8", border: "1px solid #e8d6a8", borderRadius: 4, fontSize: "11px", lineHeight: 1.6 }}>
              <strong>The pattern:</strong> AAO#1 grew from $250M to $374M in three years (+50%). GF carryover dropped from $13.5M to $5.4M (the $15M FY2024 shortfall forced tighter controls), but new GF adjustments exploded from $4.6M to $20.6M — including $15.8M in reserve transfers and a $7.5M CareBridge contract. The money finds a way.
            </div>
          </div>
        )}

        {view === "list" && (
          <div>
            <div style={{ display: "flex", gap: 8, marginBottom: 8, fontSize: "9px", fontWeight: 700, textTransform: "uppercase", letterSpacing: "1px", color: "#999" }}>
              <span>Sort:</span>
              {["amount", "dept", "fy"].map(s => <span key={s} onClick={() => setSortBy(s)} style={{ cursor: "pointer", color: sortBy === s ? "#1a1a1a" : "#bbb", borderBottom: sortBy === s ? "1px solid #1a1a1a" : "none" }}>{s}</span>)}
            </div>
            <div style={{ fontSize: "10px", color: "#999", marginBottom: 8 }}>{filtered.length} items · {fmtFull(filtered.reduce((s, i) => s + i.amount, 0))} total</div>
            {filtered.map(item => {
              const sl = stStyle(item.status);
              const isExp = expandedId === item.id;
              return (
                <div key={item.id} onClick={() => setExpandedId(isExp ? null : item.id)} style={{
                  padding: "9px 14px", marginBottom: 3, background: item.zombie ? "#fdf0f0" : isExp ? "#faf8f5" : "transparent",
                  borderLeft: "3px solid " + (item.zombie ? "#c41e1e" : sl.color), borderRadius: "0 3px 3px 0", cursor: "pointer",
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 8 }}>
                    <div style={{ flex: 1 }}>
                      {item.zombie && <span style={{ fontSize: "10px", marginRight: 4 }}>🧟</span>}
                      <span style={{ fontWeight: 700, fontSize: "12px" }}>{item.item}</span>
                      <span style={{ fontSize: "10px", color: "#999", marginLeft: 6 }}>{item.dept} · {item.current_fy}</span>
                    </div>
                    <div style={{ display: "flex", gap: 6, alignItems: "baseline", flexShrink: 0 }}>
                      <span style={{ fontSize: "8px", fontWeight: 800, padding: "2px 5px", borderRadius: 1, background: sl.bg, color: sl.color }}>{sl.text}</span>
                      <span style={{ fontWeight: 800, fontSize: "13px", fontVariantNumeric: "tabular-nums" }}>{fmt(item.amount)}</span>
                    </div>
                  </div>
                  {isExp && (
                    <div style={{ marginTop: 8, paddingTop: 8, borderTop: "1px solid #e8e4df", fontSize: "11px", color: "#555", lineHeight: 1.6 }}>
                      <div><strong>Origin:</strong> {item.fy_origin} → {item.current_fy}</div>
                      <div><strong>Category:</strong> {item.category}</div>
                      {item.notes && <div><strong>Notes:</strong> {item.notes}</div>}
                      {item.zombie && <div style={{ marginTop: 6, padding: "6px 10px", background: "#c41e1e", color: "#fff", borderRadius: 2, fontSize: "10px", fontWeight: 700 }}>⚠ ZOMBIE — This item has appeared in multiple consecutive AAO amendments without being fully spent.</div>}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {view === "dept" && (
          <div>
            <div style={{ fontSize: "10px", color: "#999", marginBottom: 12 }}>Department totals · <span style={{ color: "#c41e1e", fontWeight: 700 }}>carried</span> vs <span style={{ color: "#2a7d4f", fontWeight: 700 }}>new</span></div>
            {deptTotals.map(([dept, data]) => (
              <div key={dept} style={{ marginBottom: 14 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", fontWeight: 700, marginBottom: 4 }}>
                  <span>{dept}</span>
                  <span style={{ fontVariantNumeric: "tabular-nums" }}>{fmt(data.total)} <span style={{ fontSize: "10px", color: "#999", fontWeight: 400 }}>({data.count})</span></span>
                </div>
                <div style={{ height: 10, background: "#e8e4df", borderRadius: 2, overflow: "hidden", display: "flex" }}>
                  {data.carried > 0 && <div style={{ height: "100%", width: (data.carried/maxDeptTotal*100) + "%", background: "#c41e1e" }} />}
                  {data.newAdj > 0 && <div style={{ height: "100%", width: (data.newAdj/maxDeptTotal*100) + "%", background: "#2a7d4f" }} />}
                </div>
                <div style={{ display: "flex", gap: 12, fontSize: "10px", color: "#888", marginTop: 3 }}>
                  {data.carried > 0 && <span>Carried: {fmt(data.carried)}</span>}
                  {data.newAdj > 0 && <span>New: {fmt(data.newAdj)}</span>}
                  {data.zombie > 0 && <span style={{ color: "#d4860b" }}>Zombie: {fmt(data.zombie)}</span>}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ACCOUNTABILITY */}
        <div style={{ marginTop: 24, padding: "16px 20px", background: "#1a1a1a", color: "#fffdf9", borderRadius: 4, fontSize: "12px", lineHeight: 1.7 }}>
          <div style={{ fontWeight: 800, fontSize: "13px", marginBottom: 6, color: "#c41e1e" }}>The counterfactual question</div>
          What if unspent appropriations simply lapsed at year-end? In three years, Berkeley processed <strong>{fmt(AAO_SUMMARIES.reduce((s, a) => s + a.total, 0))}</strong> in mid-cycle amendments — nearly as much as two full adopted budgets — with a fraction of the scrutiny.
        </div>

        <div style={{ marginTop: 16, paddingTop: 12, borderTop: "1px solid #e0dbd2", fontSize: "9px", color: "#bbb", lineHeight: 1.5 }}>
          <strong>Sources:</strong> City of Berkeley Budget Committee FY24 AAO#1 (Oct 2023); FY25 AAO#1 Council Report (Nov 2024); FY26 AAO#1 Revised Supplemental (Nov 2025). Compiled by Berkeley Transparency Hub.
        </div>
      </div>
    </div>
  );
}
