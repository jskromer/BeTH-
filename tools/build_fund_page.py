#!/usr/bin/env python3
"""Render a fund ledger JSON file as a Learn About Berkeley page.

Usage:  python3 tools/build_fund_page.py data/funds/608.json docs/fund-608-marina.html

The page is generated; edit the JSON (and, for prose, the NARRATIVE block
in this file keyed by fund number), then re-run. Flows marked
reviewer "agent:proposed" are not rendered.
"""
import html
import json
import shutil
import sys
from pathlib import Path

CONF_CLASS = {"High": "hi", "Moderate": "mod", "Low": "low", "Unknown": "unk"}
KIND_LABEL = {
    "transfer_in": "Transfer in", "transfer_out": "Transfer out", "cost_shift": "Cost shift",
    "loan_in": "Loan to the fund", "loan_repayment": "Loan repayment", "grant": "Grant",
    "holiday": "Charge holiday", "indirect_reduction": "Indirect-cost reduction / holiday",
    "fee_change": "Fee change", "reduction": "Spending reduction", "write_off": "Revenue at risk",
    "appropriation": "Appropriation",
}
RESCUE_KINDS = {"transfer_in", "cost_shift", "loan_in", "grant", "indirect_reduction", "holiday"}


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def money(n, short=False):
    if n is None:
        return "—"
    neg = n < 0
    n = abs(n)
    if short:
        s = f"${n/1e6:.2f}M" if n >= 1e6 else f"${n/1e3:.0f}K"
    else:
        s = f"${n:,.0f}"
    return f"−{s}" if neg else s


def chip(c):
    return f'<span class="c {CONF_CLASS.get(c, "unk")}">{esc(c)}</span>'


# Prose that is not derivable from the data. Keyed by fund number.
NARRATIVE = {
    "011": {
        "eyebrow": "Fund ledger · 011",
        "title": "The General Fund: <span class=\"q\">where the surplus went</span>",
        "dek": "The one fund the Council controls. It has under-spent its budget and run a 'structural deficit' at the same time for seven years. The ledger shows how: money moved out to capital, reserves and the pension trust, then moved back in from internal-service balances to close the gap.",
        "verdict_title": "Swept out one year, <em>borrowed back the next.</em>",
        "verdict": "In FY2024 the General Fund transferred $41.1M out, more than budgeted, into capital, the pension trust and reserves, and its balance fell for the first time since 2018. In FY2025 it moved $33.9M out and $9.0M in. The FY2026 budget then draws $23.5M back in, including $5.2M from the Workers' Compensation fund and $6.5M from the IT cost-allocation fund, to close a gap the City calls structural. The surplus was real; the deficit is a forward projection; the transfers are the bridge between them.",
        "setup": "The General Fund receives the taxes and fees that are not earmarked: property tax, sales tax, business license, transfer tax, and the City's share of fines and charges. It is about a third of the all-funds budget and the only fund the Council can redirect without a vote of the people. Its balance was $154.9M at June 30, 2025, of which $31.7M was unassigned.",
        "flow_lead": "FY2025 as the audit reports it. Transfers in and out are shown in the ledger below rather than the diagram; in FY2025 they were $9.0M in and $33.9M out.",
        "chart_cap": "Governmental funds statement: total revenues vs total expenditures, excluding transfers. FY2024 from the FY2024 ACFR; FY2025 from the FY2025 ACFR.",
        "findings": [
            ("The fund under-spends and transfers out the difference.", "FY2024 transfers out were $41.1M against revenue of $261.8M and spending of $241.8M; FY2025 transfers out were $33.9M. The destinations are capital projects ($14.1M in FY2025), the catastrophic and public-liability insurance funds ($10.0M), the PERS savings fund ($4.8M) and reserves. The unassigned balance fell from $70M (2023) to $29.6M (2024) by reclassification, not spending.", "High"),
            ("The FY2026 fix reverses the direction.", "The FY2026 AAO schedules $23.5M of transfers into the General Fund: $6.5M from the IT cost-allocation fund, $6.0M from the payroll deduction trust, $5.2M from the Workers' Compensation fund, $2.6M from health realignment, $2.5M of Measure U1 housing money, $1.0M from parking meters. Three of those are internal-service balances that exist to pay future claims and replacements.", "High"),
            ("Seven years, seven one-time closes.", "The budget's own deficit history: $10M (FY2019), $40M, $27M, $22M, $12M, $17M, $29M (FY2026), each closed with reserves, ARPA, fund balance, vacancy savings, the Section 115 trust, or a Workers' Comp holiday. FY2027 adds $12.1M of one-time money (operating reserve and the dissolved Successor Agency) pending the November 2026 sales tax.", "High"),
            ("The General Fund is the Marina's lender and its landlord.", "It lent the Marina Fund $2.48M in FY2025 (recorded as due from), transferred $1.3M plus $226K in FY2026, collects the Marina's indirect charges, and under Resolution 70,997 forgoes $1.0-1.5M a year of Waterfront hotel tax to repay the Workers' Compensation loan.", "High"),
        ],
        "counter": "Transferring surplus to capital, reserves and the pension trust is what prudent cities do; the Auditor criticized Berkeley for under-funding exactly those things. A structural deficit measured on the operating base is real even when fund balance is high, because the balance is one-time and the costs recur. And drawing internal-service balances in a crisis year is a recognized bridge, provided the charges resume. The ledger shows the sweep and the draw-back; whether that is discipline or circularity depends on whether the charges resume in FY2027.",
        "what_next": ["Add the FY2026 audited transfers when the ACFR is published (early 2027) and compare them to the AAO schedule.", "Read the FY2024 ACFR transfers note for the full destination list.", "Track whether Workers' Compensation and IT cost-allocation charges resume in the FY2027-28 budget."],
    },
    "ACFR-park-tax": {
        "eyebrow": "Fund ledger · Parks Tax",
        "title": "The Parks Tax: <span class=\"q\">what Measure Y bought</span>",
        "dek": "A parcel tax for parks, trees and landscaping, raised 20% by voters in November 2024. Its first-year effect includes $1.58M a year of Waterfront costs moved off the Marina Fund.",
        "verdict_title": "A parks tax that now <em>carries the Waterfront.</em>",
        "verdict": "Measure Y raised the Parks Tax by about $3.8M a year. From July 2025, $1.58M a year of Waterfront park and landscape maintenance moved from the failing Marina Fund onto this one, and in FY2027 5% of the Waterfront Deputy Director follows. The ballot question named parks generally; the Council's September 2024 intent resolution named the Waterfront. The shift was disclosed, in a resolution rather than on the ballot.",
        "setup": "The Parks Tax is a special parcel tax, first approved in 1997 and raised in 2000, 2008, 2014 and 2024, charged per square foot of building improvements and indexed annually. By law it can be spent only on parks, trees and landscaping. It is the second-largest source of parks money after the General Fund.",
        "flow_lead": "FY2025, the last year before Measure Y took effect. Revenue is almost entirely the parcel tax; spending is culture-recreation (park maintenance) with a small capital outlay.",
        "chart_cap": "Nonmajor governmental combining statements: total revenues vs total expenditures, excluding transfers. FY2024 from the FY2024 ACFR; FY2025 from the FY2025 ACFR.",
        "findings": [
            ("Revenue up $1.3M, spending up $2.6M, before Measure Y.", "FY2024 to FY2025: revenue $18.1M to $19.4M; spending $15.1M to $17.7M. The balance still rose, to $12.3M, because the fund ran a surplus both years.", "High"),
            ("The Marina shift is a third of the Measure Y uplift.", "Measure Y adds about $3.8M a year; the Waterfront cost shift takes $1.58M of it. Whether the rest raised park maintenance capacity or absorbed other cost growth is not visible until the FY2026 audit.", "High on the figures; Moderate on the reading"),
        ],
        "counter": "Cesar Chavez, Shorebird and Horseshoe are parks, and the Parks Tax is for parks; charging their upkeep to the parks tax rather than to boat-slip fees corrects a 60-year anomaly rather than creating one. The Council said so in a public resolution before the vote, and 75% of voters approved. The ledger records the shift; it does not say it was wrong.",
        "what_next": ["Load FY2026 when audited and compare park maintenance spending to FY2025.", "Read the Measure Y expenditure plan in the FY2026 budget for the split between maintenance, trees and capital."],
    },
    "ACFR-equipment-maintenance-replacement": {
        "eyebrow": "Fund ledger · 671 / 672",
        "title": "Equipment Maintenance & Replacement: <span class=\"q\">the fund that gets raided</span>",
        "dek": "Two internal-service funds, reported as one: departments pay 672 to maintain vehicles and 671 to replace them. The 2021 audit titled its report 'Fleet Replacement Fund Short Millions.' Since then $2.5M has moved from the replacement fund to pay maintenance.",
        "verdict_title": "Replacement money, <em>spent on repairs.</em>",
        "verdict": "In FY2024 $500,000 and in FY2025 $2,000,000 moved out of the replacement fund (671) to cover the maintenance fund's (672) operating costs. The 2021 audit asked for an Administrative Regulation requiring written justification before any such transfer; in October 2025 it was still 'partly implemented.' The combined fund's balance is healthy on paper, $39.8M, because it includes vehicles not yet bought.",
        "setup": "Departments pay an annual charge per vehicle into fund 672 for maintenance and into fund 671 to accumulate the vehicle's replacement cost. When the vehicle ages out, 671 buys the replacement. The ACFR reports the two as one internal service fund. The City Auditor's 2021 report found the replacement charges too low to replace the fleet on schedule.",
        "flow_lead": "FY2025 as the audit reports it. Revenue is almost entirely the equipment rental charge departments pay; spending is maintenance labor, parts and depreciation. Transfers in are the General Fund's and the CIP's contributions.",
        "chart_cap": "Internal service combining statements: operating revenues vs operating expenses, including depreciation. FY2024 from the FY2024 ACFR; FY2025 from the FY2025 ACFR.",
        "findings": [
            ("$2.5M moved from replacement to maintenance in two years.", "Per the February 27, 2025 fleet audit presentation: $500,000 in FY2024 and $2,000,000 in FY2025 from fund 671 to fund 672 for operating expenses. The audit's recommendation 1.6 (an A.R. requiring documented justification before raiding the fund) was still partly implemented in October 2025.", "High"),
            ("The fund replaces about 7% of the fleet a year.", "FY2020-24 average: 46 units a year, 7.4% of the fleet, implying a 13-14 year replacement cycle. $50.3M was spent or encumbered on replacement from FY2019 to FY2025, and the 671 balance rose from $7.4M to $19.7M.", "High"),
            ("Electrification is an unfunded step change.", "Staff estimate about $9.0M of extra vehicle cost plus $6.5M of chargers for the Zero Waste fleet alone (October 2025). A new maintenance rate model is promised for the FY2027-28 mid-biennial update.", "Moderate"),
        ],
        "counter": "Moving replacement money to maintenance keeps vehicles running when the maintenance charge is set too low, and the combined fund still ran a surplus both years with a $39.8M net position. The audit's complaint is about documentation and rate-setting, not insolvency. A fund with rising balances and 11 of 12 recommendations partly implemented is a slow fix, not a raid.",
        "what_next": ["Identify the source of the remaining $2.0M of FY2025 transfers in.", "Read the FY2027-28 mid-biennial rate model when published.", "Load FY2019-2023 from earlier ACFRs to show the balance build-up the audit describes."],
    },
    "ACFR-workers-compensation": {
        "eyebrow": "Fund ledger · Workers' Compensation",
        "title": "Workers' Compensation: <span class=\"q\">two years of zero revenue</span>",
        "dek": "An internal-service fund that is supposed to bill departments for self-insured injury claims. In FY2024 and FY2025 it billed nothing, lent $5.5M to the Marina docks, and ended FY2025 $9.75M in the hole. The FY2026 budget then moves another $5.2M out of it to the General Fund.",
        "verdict_title": "A claims fund used as <em>a piggy bank.</em>",
        "verdict": "Operating revenue: $0 in FY2024, $0 in FY2025. Claims and expenses: $7.8M then $12.0M. Transfers out: $5.5M to the Marina dock project in FY2024, $5.2M to the General Fund budgeted for FY2026. Net position went from +$1.9M to −$9.75M in one year. The 'holidays' the Marina decks mention are this: departments, the General Fund among them, stopped paying their workers' compensation charge, and the fund paid claims out of its balance.",
        "setup": "The Workers' Compensation Fund is one of eight internal service funds. Departments are charged a premium set in the budget; the fund pays injured-worker claims and administration. Its balance is the cushion against claims that take years to settle. The ACFR's self-insurance note carries the actuarial claims liability.",
        "flow_lead": "FY2025 as the audit reports it: no revenue at all, $12.0M of claims and administration paid from the balance.",
        "chart_cap": "Internal service combining statements: operating revenues vs operating expenses. FY2024 from the FY2024 ACFR; FY2025 from the FY2025 ACFR.",
        "findings": [
            ("Zero charges, two years running.", "The FY2024 and FY2025 statements both show operating revenue of $0 for this fund. The FY2025 deficit history calls FY2025 a 'Workers Comp holiday'; the Marina decks describe the same holiday as Marina relief. Every department that pays into this fund, including General Fund departments, got the relief.", "High"),
            ("The $5.5M Marina loan was booked as a transfer out.", "Resolution 70,997 (July 25, 2023) called it an internal loan repayable from Waterfront hotel tax. The FY2024 ACFR shows it as a $5,500,000 transfer out, with no receivable, and the Marina Operations Fund shows no loan in. Where the money went on the books, and whether any TOT has come back, are open questions.", "High on the records; Unknown on the reconciliation"),
            ("The General Fund is next.", "The FY2026 AAO budgets a $5,187,019 transfer from this fund to the General Fund, from a fund whose audited net position was already −$9.75M.", "High"),
        ],
        "counter": "A self-insurance fund can carry a negative net position for a time because claims are paid over years, and an actuary, not the balance sheet, says whether it is adequately funded. Suspending charges when a fund is over-reserved is a legitimate way to return money to departments; the City Auditor has in the past criticized over-accumulation in internal-service funds. If charges resume in FY2027 at an actuarially set rate, two holiday years are a timing choice, not a loss.",
        "what_next": ["Read the ACFR self-insurance note for the claims liability and the actuarial target.", "Confirm in the FY2027-28 budget whether and at what rate charges resume.", "Request the accounting for the $5.5M dock transfer and any TOT repayments."],
    },
    "ACFR-zero-waste": {
        "eyebrow": "Fund ledger · Zero Waste",
        "title": "Zero Waste: <span class=\"q\">rates up, still losing</span>",
        "dek": "The refuse enterprise. A five-year rate increase adopted in 2023 was supposed to keep the fund positive while its balance fell from $24.5M to $3.3M. Two years in, it has lost $4.0M and $1.3M and sits near zero.",
        "verdict_title": "The rate plan's cushion <em>is already gone.</em>",
        "verdict": "Council raised refuse, recycling and organics rates in June 2023 for FY2024 through FY2028, on a staff projection that the fund's balance would decline but stay positive. The audited result: an operating loss of $5.4M in FY2024 and $1.5M in FY2025, net position $349,593 at the start of FY2025. The 2014 and 2016 audits' efficiency recommendations, 18 of 27 of them, were dropped, including one sized at $496,000 a year.",
        "setup": "The Zero Waste Fund collects refuse, recycling and organics rates from residents and businesses and pays for collection, the transfer station, street sweeping and illegal-dumping cleanup. Under Proposition 218 rates can rise only after a noticed hearing without a majority protest. The current schedule is Resolution 70,932 (June 27, 2023).",
        "flow_lead": "FY2025 as the audit reports it. Revenue is refuse service fees; spending is dominated by personnel and contracted services. Transfers out went to capital project support and catastrophic insurance.",
        "chart_cap": "Proprietary funds statement: operating revenues vs operating expenses, including depreciation. FY2024 from the FY2024 ACFR; FY2025 from the FY2025 ACFR.",
        "findings": [
            ("Two losing years after a rate increase.", "Operating loss $5.4M (FY2024) and $1.5M (FY2025). Net position $769,103 at June 30, 2024, restated to $349,593, and the fund is heading for the General Fund's door the way the Marina did.", "High"),
            ("The efficiency list was dropped, not rejected.", "18 of 27 recommendations from the Zero Waste audits lapsed: a route audit to align billing with service, franchise-fee recovery on recyclables, mobile route technology, a strategic plan with performance measures, and biweekly collection (about $496K a year, needing a state waiver).", "High"),
            ("The next costs are capital.", "The transfer station replacement and an electric fleet (about $15.5M for vehicles and chargers, staff estimate) are not in the 2023 rate schedule's assumptions.", "Moderate"),
        ],
        "counter": "The 2023 rate plan was designed to spend down a $24.5M balance; losses in its first years are the plan working, not failing, and FY2024's loss was inflated by one-time costs. Proposition 218 limits how fast rates can move. Dropped audit recommendations include some that needed state waivers the City cannot grant itself. The fund's problem is cost growth in a labor-heavy service, which no efficiency list fully offsets.",
        "what_next": ["Compare the 2023 projection to audited results year by year as each ACFR is published.", "Load the rate schedule's FY2026-2028 steps and the Transfer Station budget.", "Track which dropped recommendations return in the FY2027-28 budget."],
    },
    "608": {
        "eyebrow": "Fund ledger · 608",
        "title": "The Marina Fund: <span class=\"q\">one enterprise, six rescues</span>",
        "dek": "Berkeley set the Marina Fund up in 1964 to pay for the whole Waterfront out of berth rents and hotel and restaurant leases. It has run a structural deficit for 25 years. This page is the fund's ledger: every audited year, every dollar moved in from somewhere else, and what it owes.",
        "verdict_title": "Six pockets, one fund, <em>no fix.</em>",
        "verdict": "Since FY2022 the Marina Fund has been kept solvent with federal ARPA money, a State grant, a loan from the Workers' Compensation fund repaid out of hotel tax, a General Fund loan, General Fund transfers, and a cost shift to the Parks Tax. Every one went through Council. Every one was one-time, or shifted the cost to another fund. Staff's own forecast has the fund negative by FY2028, with $163 million of unfunded capital and no reserve.",
        "setup": "Staff's words, September 2026: the fund was \"established in 1964 to receive a $1.8M State loan to build the Waterfront,\" and \"revenue from slips and hotel/restaurant leases was expected to cover the costs of debt service, maintenance and operations of the entire Waterfront.\" The entire Waterfront means 1.8 miles of streets, 11 parking lots, 5 miles of pathways, three parks including Cesar Chavez, 1,000 berths, the public docks and launch ramp, the office buildings, the restrooms, the Nature Center, Adventure Playground, 13 leases, and all the utilities. A berth-fee enterprise was asked to maintain a public park system.",
        "findings": [
            ("Six different pockets in five years.", "Federal ARPA (FY22–23), the Workers' Compensation internal-service fund (loan authorized 2023), a State capital grant (FY25), the General Fund (loan FY25; transfers FY26), the Parks Tax (cost shift from FY26), and waived indirect charges and Workers' Comp 'holidays' (FY25–26). None was the fund's own revenue.", "High"),
            ("The fixes were one-time; the deficit is recurring.", "The FY26 budget staff report says of its own fix: 'not sustainable long-term solutions.' Staff's September 2026 forecast shows the fund negative by FY28 and names a $1.045M gap with 'No General Fund available to bail out the Marina Fund.'", "High"),
            ("The largest permanent fix came from a voter measure for parks.", "Measure Y (Nov 2024) raised the Parks Tax; its first-year effect includes $1.579M of Waterfront park and landscape costs moved off the Marina Fund. The ballot question named parks, trees and landscaping generally. The Council's September 24, 2024 resolution, adopted before the vote, stated the intent to cover 'park and landscape maintenance in the Waterfront including Cesar Chavez.' The shift was disclosed, in a Council resolution rather than on the ballot.", "High"),
            ("The 2023 loan is repaid by the General Fund, not the Marina.", "Council's resolution of July 25, 2023 directs the $5.5M Workers' Compensation loan to be repaid from the Waterfront's Transient Occupancy Tax, which is General Fund revenue, plus a one-time $500,000. Staff estimated the General Fund loses $1.0–1.5M a year until it is paid. That subsidy does not appear on any Marina Fund slide.", "High"),
            ("The two audits do not show the loan the way staff describe it.", "Staff's May 2025 deck lists '$5.5M from Workers Comp fund for capital projects' under FY24. The FY2024 ACFR records no interfund loan receipt by the Marina fund and nothing due from it at June 30, 2024. The FY2025 ACFR records a $2,477,099 interfund loan receipt, shown as due to the General Fund. How the $5.5M was booked is an open question.", "High"),
            ("The problem is the charter, not the year.", "Every rescue restates the same mismatch: an enterprise fund that must cover streets, parks and a seawall for the general public out of boat slips and a hotel lease. Until the Waterfront's public-park costs are carried by the funds that carry every other park, the next rescue is already scheduled.", "Moderate"),
        ],
        "counter": "An enterprise fund with a 25-year structural deficit has two honest outcomes: subsidize it openly or close the service. Berkeley has chosen to subsidize, and every transfer on this page went through a public vote of the Council. Measure Y's park-maintenance purpose does cover Waterfront parks, which are parks, and the Council said so before the election. The Doubletree collapse is a Bay Area hotel-market event the City did not cause. Replacing a State loan with an internal one saved the fund up to $10M in interest. And letting the Waterfront fail would cost more than any of this. The ledger does not settle that argument; it makes it visible.",
        "flow_lead": "One audited year. In a normal year the fund's own revenue of about $7M runs close to its operating cost of about $7.3M, so the structural gap is roughly $1M. FY2025 looks worse because dock-project spending ran through operations, and a State grant and a General Fund loan covered it. The General Fund sits on both sides: it collects the central charges and it lends the money in.",
        "chart_cap": "FY2015–2023 from the government-wide ten-year schedule (charges for services vs expenses, FY2024 ACFR); FY2024–25 from the proprietary fund statements (operating revenue vs operating expenses, which include depreciation); FY2026–28 staff cash forecast. FY2025 expenses include dock-project spending; a $7.69M State grant that year is not in the revenue bar.",
        "tot_lead": "The Waterfront's hotel generates Transient Occupancy Tax, and the question comes up every time the Marina Fund is discussed: why not just give the Marina its own hotel tax? It is about the right size for the operating gap. It is not a fix, for three reasons.",
        "tot_points": [
            ("It is already pledged.", "Council's July 25, 2023 resolution directs the entire Waterfront TOT, from FY2025 until paid off, to repay the $5.5M Workers' Compensation loan plus $500,000. At $1.0–1.5M a year that runs four to six years, into roughly FY2029–2031. Whether any TOT has actually flowed to that repayment is an open question; the audits do not show it.", "High"),
            ("It comes from the same hotel.", "TOT is a percentage of room revenue at the Doubletree, which has lost money every year since 2020, is in special servicing, and has paid no rent since December 2025. When a hotel's lease income fails its tax yield is falling too; if the lender takes it or closes it, TOT goes to zero. Pledging TOT to the Marina swaps one bet on this hotel for a larger bet on the same hotel.", "High"),
            ("It is General Fund money.", "TOT is a general tax. Sending it to the Marina needs no vote, only a budget line, but it is a $1.0–1.5M annual General Fund subsidy with a label, in a year the General Fund is cutting $29M. It makes the sixth pocket permanent; it does not make the fund self-supporting. And at $1.5M a year, a capital reserve would reach the $163M need in about a century.", "High"),
        ],
        "tot_close": "Where the idea is strongest: 'revenue the Waterfront generates should stay at the Waterfront' is the charter fix this page points at, done properly. Waterfront parks to the Parks Tax (done, via Measure Y), Waterfront streets to the street funds, and Waterfront TOT to a Marina capital reserve once the loan is repaid, with the operating fund sized to berths and leases only. That would be a re-chartering, which is what the fund has needed for 25 years. It would still not be 'everything.'",
        "what_next": [
            "Ask Finance how the July 2023 $5.5M authorization was booked, how much has been drawn, and how much Waterfront TOT has gone to repay it since FY2025.",
            "Ask which 'other funds' absorbed the FY2024 $800K cost shift.",
            "Add the FY2026 audited year when the ACFR is published (early 2027).",
            "Log every FY27–28 balancing action the PRW Commission and Council take against staff's $1.045M target.",
        ],
    }
}


def generic_narrative(d):
    aud = [y for y in d["annual"] if y["basis"] == "audited"]
    y = aud[-1] if aud else d["annual"][-1]
    rev, exp = y.get("revenue") or 0, y.get("expenditure") or 0
    res = rev - exp
    ti = y.get("transfers_in") or 0
    kind = {"general": "the City's one discretionary fund", "special_revenue": "a special revenue fund: money earmarked by a tax measure, a grant or a fee for one purpose",
            "capital_project": "a capital project fund", "debt_service": "a debt service fund, which exists to pay one bond issue",
            "enterprise": "an enterprise fund, run like a business on its own charges", "internal_service": "an internal service fund that bills City departments"}.get(d["type"], "a City fund")
    verdict = (f"In FY{y['fy']} it took in {money(rev, True)} and spent {money(exp, True)}, "
               + (f"a {money(res, True)} surplus" if res >= 0 else f"a {money(-res, True)} shortfall")
               + (f", with {money(ti, True)} transferred in from other funds" if ti else "")
               + f". Year-end balance {money(y.get('ending_balance'), True)}.")
    return {
        "eyebrow": f"Fund ledger · {d['fund_number']}",
        "title": esc(d["name"]),
        "dek": f"{esc(d['name'])} is {kind}. This page is its ledger: the audited figures, where the money came from and went, and the dated events once they have been read from Council records.",
        "verdict_title": "One year loaded, <em>events not yet read.</em>",
        "verdict": verdict + " Only the FY2025 audit is loaded for this fund; prior years and the flow ledger are added as the agendas are read. Figures are the City's; the reading is ours.",
        "setup": f"{esc(d['name'])}: {kind}. Establishment, legal basis and purpose have not yet been researched for this fund; the ACFR fund description pages are the next source.",
        "findings": [], "what_next": ["Load FY2015–FY2024 from the earlier ACFRs.", "Read the fund's description page in the ACFR for its legal basis.", "Scan Council budget adoptions and AAO amendments for transfers, loans and cost shifts affecting this fund."],
    }


def build(json_path: Path, out_path: Path):
    d = json.loads(json_path.read_text())
    n = NARRATIVE.get(d["fund_number"]) or generic_narrative(d)
    src = d["sources"]
    flows = [f for f in d["flows"] if not str(f.get("reviewer", "")).startswith("agent:")]

    # ---- chart: revenue vs expenditure by FY (inline SVG, no scripts) ----
    years = [y for y in d["annual"] if y.get("revenue") is not None and y.get("expenditure") is not None]
    vmax = max((max(y["revenue"], y["expenditure"]) for y in years), default=1) or 1
    W, H, L, B, T = 860, 300, 70, 40, 16
    plot_h = H - B - T
    bw = (W - L - 10) / len(years)
    bars = []
    for i, y in enumerate(years):
        x0 = L + i * bw
        for j, (k, cls) in enumerate((("revenue", "rev"), ("expenditure", "exp"))):
            h = y[k] / vmax * plot_h
            bars.append(f'<rect class="{cls}{" proj" if y["basis"]=="projected" else ""}" x="{x0 + 4 + j*(bw/2-4):.1f}" y="{T + plot_h - h:.1f}" width="{bw/2-6:.1f}" height="{h:.1f}"><title>FY{y["fy"]} {k}: {money(y[k])} ({y["basis"]})</title></rect>')
        bars.append(f'<text class="xl" x="{x0 + bw/2:.1f}" y="{H-14}" text-anchor="middle">{str(y["fy"])[2:]}</text>')
    grid = []
    for g in range(0, 5):
        v = vmax * g / 4
        yy = T + plot_h - v / vmax * plot_h
        grid.append(f'<line class="g" x1="{L}" x2="{W-10}" y1="{yy:.1f}" y2="{yy:.1f}"/><text class="yl" x="{L-8}" y="{yy+4:.1f}" text-anchor="end">{money(v, True)}</text>')
    chart = f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="Revenue and expenses by fiscal year">
<style>.g{{stroke:#d8dce6;stroke-width:1}} .yl,.xl{{font:11px Jost,sans-serif;fill:#4b5577}} .rev{{fill:#002198}} .exp{{fill:#a8322c}} .proj{{opacity:.45}}</style>
{''.join(grid)}{''.join(bars)}
</svg>
<div class="cap"><span class="sw rev"></span> Revenue &nbsp; <span class="sw exp"></span> Expenses &nbsp; faded = staff projection. {esc(n.get("chart_cap", "Revenue and spending as the ACFR statement reports them; transfers in and out are not included in either bar."))}</div>'''

    # ---- annual table ----
    arows = []
    for y in d["annual"]:
        arows.append(f'<tr><td>FY{y["fy"]}</td><td>{esc(y["basis"])}</td><td class="n">{money(y.get("revenue"))}</td><td class="n">{money(y.get("expenditure"))}</td><td class="n">{money((y.get("revenue") or 0)-(y.get("expenditure") or 0)) if y.get("revenue") is not None else "—"}</td><td class="n">{money(y.get("ending_balance"))}</td><td>{chip(y["confidence"])}</td><td class="note">{esc(y.get("note",""))}</td></tr>')

    # ---- flow ledger ----
    frows = []
    rescue_total = 0
    for f in sorted(flows, key=lambda f: (f["fy"], f["date"])):
        if f["kind"] in RESCUE_KINDS and f.get("amount") and f["fy"] >= 2022:
            rescue_total += f["amount"]
        path = f'{esc(f.get("from_fund",""))} → {esc(f.get("to_fund",""))}' if f.get("from_fund") else ""
        detail = esc(f.get("stated_reason", ""))
        if f.get("terms"):
            detail += f'<div class="terms">{esc(f["terms"])}</div>'
        if f.get("note"):
            detail += f'<div class="terms">{esc(f["note"])}</div>'
        s = src[f["source"]]
        frows.append(f'<tr><td>FY{f["fy"]}<div class="sub">{esc(f["date"])}</div></td><td>{esc(KIND_LABEL.get(f["kind"], f["kind"]))}{"<div class=sub>recurring</div>" if f.get("recurring") else ""}</td><td class="n">{money(f.get("amount"))}</td><td>{path}</td><td>{detail}</td><td><a href="{esc(s["url"])}">{esc(f["instrument"])}</a></td><td>{chip(f["confidence"])}</td></tr>')

    # ---- assets: physical inventory and balance sheet ----
    assets_html = ""
    A = d.get("assets")
    if A:
        rows = "".join(f'<tr><td>{esc(c["name"])}</td><td>{esc(c["what"])}</td><td class="n">{money(c["unfunded_need"]) if c["unfunded_need"] is not None else "—"}</td></tr>' for c in A["classes"])
        tot_need = sum(c["unfunded_need"] or 0 for c in A["classes"])
        assets_html += f'<h3>What the fund has to maintain</h3><div class="tw"><table><thead><tr><th>Asset class</th><th>What it is</th><th>Unfunded need</th></tr></thead><tbody>{rows}<tr class="sub"><td>Total</td><td>{esc(A.get("also",""))}</td><td class="n">{money(tot_need)}</td></tr></tbody></table></div><div class="cap">Inventory from the May 2025 and September 2026 staff decks; unfunded need as of {esc(A["as_of"])}. {chip(A["confidence"])}</div>'
    B = d.get("balance_sheet")
    if B:
        ar = "".join(f'<tr><td>{esc(a["line"])}</td><td class="n">{money(a["amount"])}</td><td class="note">{esc(a.get("note",""))}</td></tr>' for a in B["assets"])
        lr = "".join(f'<tr><td>{esc(a["line"])}</td><td class="n">{money(a["amount"])}</td><td class="note">{esc(a.get("note",""))}</td></tr>' for a in B["liabilities"])
        assets_html += f'<h3>What the fund owns on paper, {esc(B["as_of"])}</h3><div class="tw"><table><thead><tr><th>Assets</th><th>Amount</th><th>Note</th></tr></thead><tbody>{ar}</tbody><thead><tr><th>Liabilities</th><th>Amount</th><th>Note</th></tr></thead><tbody>{lr}<tr class="sub"><td>Net position</td><td class="n">{money(B["net_position"])}</td><td></td></tr></tbody></table></div><div class="cap">{esc(B.get("note",""))} {chip(B["confidence"])}</div>'

    # ---- flow diagram: one audited year, inline SVG ----
    flow_html = ""
    F = d.get("flow_detail")
    if F and not (F.get("inflows") or F.get("outflows")):
        flow_html = '<div class="cap">The statement shows no revenue and no spending for this fund in FY%d; only a balance.</div>' % F["fy"]
        F = None
    if F:
        ins = sorted(F["inflows"], key=lambda x: -x["amount"])
        outs = sorted(F["outflows"], key=lambda x: -x["amount"])
        vmax = max(x["amount"] for x in ins + outs)
        rowh = 46
        n_rows = max(len(ins), len(outs))
        H = 60 + rowh * n_rows + 30
        W = 900
        cx = W / 2
        bal_year = next((y for y in d["annual"] if y["fy"] == F["fy"] and y["basis"] == "audited"), None)
        centre_sub = (f"balance June 30, {F['fy']}: {money(bal_year.get('ending_balance'), True)}" if bal_year and bal_year.get("ending_balance") is not None else f"FY{F['fy']}")
        parts = []
        parts.append(f'<rect x="{cx-80}" y="{60 + rowh*n_rows/2 - 40}" width="160" height="80" rx="10" fill="#002198"/><text x="{cx}" y="{60 + rowh*n_rows/2 - 8}" text-anchor="middle" class="fl fw">{esc(d["name"][:26])}</text><text x="{cx}" y="{60 + rowh*n_rows/2 + 14}" text-anchor="middle" class="fs fw">{esc(centre_sub)}</text>')
        for i, x in enumerate(ins):
            y = 60 + i * rowh + rowh / 2
            w = 1 + 7 * x["amount"] / vmax
            col = "#1f6b4a" if x["kind"] == "own" else "#a8322c"
            parts.append(f'<line x1="300" y1="{y}" x2="{cx-82}" y2="{60 + rowh*n_rows/2}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round" opacity=".85"/>')
            parts.append(f'<text x="292" y="{y+4}" text-anchor="end" class="fl">{esc(x["line"])}</text><text x="292" y="{y+18}" text-anchor="end" class="fs">{money(x["amount"], True)}</text>')
        for i, x in enumerate(outs):
            y = 60 + i * rowh + rowh / 2
            w = 1 + 7 * x["amount"] / vmax
            parts.append(f'<line x1="{cx+82}" y1="{60 + rowh*n_rows/2}" x2="600" y2="{y}" stroke="#4b5577" stroke-width="{w:.1f}" stroke-linecap="round" opacity=".8"/>')
            parts.append(f'<text x="608" y="{y+4}" class="fl">{esc(x["line"])}</text><text x="608" y="{y+18}" class="fs">{money(x["amount"], True)}{(" · " + esc(x["note"])) if x.get("note") else ""}</text>')
        parts.append(f'<text x="20" y="34" class="fl">Money in, FY{F["fy"]}</text><text x="608" y="34" class="fl">Money out, FY{F["fy"]}</text>')
        own = sum(x["amount"] for x in ins if x["kind"] == "own"); rescue = sum(x["amount"] for x in ins if x["kind"] != "own")
        flow_html = f'''<div class="chartwrap"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Money in and out of the Marina Fund, FY{F["fy"]}"><style>.fl{{font:13px Jost,sans-serif;fill:#0b1540}} .fs{{font:11px Jost,sans-serif;fill:#4b5577}} .fw{{fill:#fff}}</style>{''.join(parts)}</svg>
<div class="cap"><span class="sw" style="background:#1f6b4a"></span> own revenue {money(own, True)} &nbsp; <span class="sw" style="background:#a8322c"></span> rescue money {money(rescue, True)} &nbsp; line width = amount. Outflows are operating expenses plus debt service and transfers; depreciation is non-cash. {chip(F["confidence"])}</div></div>'''

    # ---- obligations ----
    orows = [f'<tr><td>{esc(o["kind"].replace("_"," "))}</td><td class="n">{money(o["amount"])}</td><td>{esc(o["as_of"])}</td><td>{esc(o["note"])}</td><td>{chip(o["confidence"])}</td></tr>' for o in d.get("obligations", [])]

    findings = "".join(f'<div class="prob"><div class="pn">Finding {i+1}</div><h3>{esc(t)}</h3><p>{esc(b)} {chip(c)}</p></div>' for i, (t, b, c) in enumerate(n.get("findings", [])))
    tot_points = "".join(f'<div class="prob"><div class="pn">Reason {i+1}</div><h3>{esc(t)}</h3><p>{esc(b)} {chip(c)}</p></div>' for i, (t, b, c) in enumerate(n.get("tot_points", [])))
    T = d.get("tot", {"waterfront_tot_per_year": [0, 0], "citywide_tot": {"fy2027_proposed": 0}, "pledge": "", "confidence": "Unknown"})
    openq = "".join(f"<li>{esc(q)}</li>" for q in d["status"].get("open_questions", []))
    nextq = "".join(f"<li>{esc(q)}</li>" for q in n.get("what_next", []))
    sources = "".join(f'<li><a href="{esc(s["url"])}">{esc(s["title"])}</a> <span class="tag">{esc(sid)}</span></li>' for sid, s in src.items())
    audited = [y for y in d["annual"] if y["basis"] == "audited"]
    latest = audited[-1]
    covered = sum(1 for y in audited if y["revenue"] >= y["expenditure"])
    unf = [o for o in d.get("obligations", []) if o["kind"] == "unfunded_capital"]
    unfunded = max(unf, key=lambda o: o["as_of"]) if unf else None

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(d["name"])} — Fund Ledger — Learn About Berkeley</title>
<meta name="description" content="{esc(n.get("dek",""))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root{{ --navy:#2a3340; --slate:#3f4f63; --slate-2:#34414f; --steel:#43698f; --steel-deep:#33567a; --red:#a8322c; --paper:#f5f7f9; --card:#ffffff; --rule:#dde3ea; --rule-strong:#c3ccd6; --muted:#5d6b7a; --hi:#2f6f57; --mod:#956613; --low:#a8322c; --unk:#6b7280; --maxw:960px; }}
  *{{box-sizing:border-box}} body{{ margin:0; background:var(--paper); color:var(--navy); font-family:"Source Serif 4",Georgia,serif; font-size:18px; line-height:1.6; }}
  .wrap{{ max-width:var(--maxw); margin:0 auto; padding:0 26px; }} a{{ color:var(--steel-deep); }}
  .hubbar{{ background:var(--slate); color:#eef1f5; }} .hubbar-in{{ max-width:var(--maxw); margin:0 auto; padding:11px 26px; display:flex; justify-content:space-between; gap:14px; }}
  .hubbar a.back{{ font-family:"JetBrains Mono",monospace; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#cdd6e0; text-decoration:none; }} .hubbar .stamp{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:#9fb0c1; }}
  .masthead{{ padding:48px 0 26px; border-bottom:2px solid var(--navy); }} .eyebrow{{ font-family:"JetBrains Mono",monospace; font-size:11.5px; letter-spacing:.16em; text-transform:uppercase; color:var(--steel-deep); margin-bottom:20px; display:flex; align-items:center; gap:10px; }} .eyebrow .tick{{ width:22px; height:2px; background:var(--steel); display:inline-block; }}
  h1{{ font-family:"Playfair Display",serif; font-weight:700; font-size:clamp(2rem,6vw,3.1rem); line-height:1.02; margin:.05em 0 .3em; }} h1 .q{{ font-style:italic; font-weight:600; color:var(--steel-deep); }}
  .dek{{ font-size:clamp(1.04rem,2.2vw,1.22rem); line-height:1.45; color:var(--muted); max-width:66ch; margin:0 0 26px; }} .meta-row{{ font-family:"JetBrains Mono",monospace; font-size:11.5px; color:var(--muted); display:flex; flex-wrap:wrap; gap:6px 24px; }} .meta-row b{{ color:var(--navy); }}
  .legend{{ margin:24px 0 0; padding:14px 16px; background:var(--card); border:1px solid var(--rule-strong); }} .legend .lt{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); margin-bottom:9px; }} .chips{{ display:flex; flex-wrap:wrap; gap:8px; }}
  .chip{{ font-family:"JetBrains Mono",monospace; font-size:11px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; padding:3px 9px; color:#fff; }} .chip.hi{{background:var(--hi)}} .chip.mod{{background:var(--mod)}} .chip.low{{background:var(--low)}} .chip.unk{{background:var(--unk)}}
  .c{{ font-family:"JetBrains Mono",monospace; font-size:10px; font-weight:700; letter-spacing:.03em; text-transform:uppercase; padding:1px 6px; color:#fff; vertical-align:.12em; white-space:nowrap; }} .c.hi{{background:var(--hi)}} .c.mod{{background:var(--mod)}} .c.low{{background:var(--low)}} .c.unk{{background:var(--unk)}}
  .verdict{{ margin:32px 0 8px; padding:24px 26px; background:var(--slate); color:#eef1f5; }} .verdict .vk{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; letter-spacing:.18em; text-transform:uppercase; color:#9fb6c9; margin-bottom:9px; }} .verdict .vt{{ font-family:"Playfair Display",serif; font-weight:700; font-size:1.55rem; line-height:1.12; margin:0 0 .4em; color:#fff; }} .verdict .vt em{{ color:#8fbede; font-style:italic; }} .verdict p{{ margin:0; font-size:1rem; color:#d4dbe3; }}
  section{{ padding:36px 0; border-bottom:1px solid var(--rule); }} .sec-no{{ font-family:"JetBrains Mono",monospace; font-size:11.5px; font-weight:700; letter-spacing:.1em; color:var(--steel); margin-bottom:9px; display:block; }}
  h2{{ font-family:"Playfair Display",serif; font-weight:700; font-size:clamp(1.4rem,3.4vw,1.9rem); line-height:1.1; margin:0 0 .5em; }} h3{{ font-family:"Playfair Display",serif; font-weight:700; font-size:1.18rem; margin:.3em 0 .4em; }}
  p{{ margin:0 0 1.05em; }} p:last-child{{ margin-bottom:0; }} .lead{{ font-size:1.05rem; }} ul.clean{{ padding-left:1.15em; margin:.3em 0 1.05em; }} ul.clean li{{ margin:0 0 .55em; }}
  .statrow{{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin:22px 0 6px; }} @media(min-width:620px){{ .statrow{{ grid-template-columns:repeat(4,1fr); }} }}
  .stat{{ background:var(--card); border:1px solid var(--rule-strong); padding:14px 15px; }} .stat .v{{ font-family:"Playfair Display",serif; font-weight:700; font-size:1.45rem; line-height:1; }} .stat .l{{ font-family:"JetBrains Mono",monospace; font-size:10px; letter-spacing:.03em; text-transform:uppercase; color:var(--muted); margin-top:7px; line-height:1.4; }}
  .prob{{ background:var(--card); border:1px solid var(--rule-strong); padding:20px 22px; margin:14px 0; }} .prob .pn{{ font-family:"JetBrains Mono",monospace; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--steel-deep); }}
  .panel{{ margin:8px 0 0; padding:22px 26px; background:#eef2f6; border:1px solid #cdd9e4; border-left:4px solid var(--steel); }} .panel .pk{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--steel-deep); margin-bottom:10px; }}
  .chartwrap{{ background:var(--card); border:1px solid var(--rule-strong); padding:16px 16px 10px; margin:14px 0; }} .chartwrap svg{{ width:100%; height:auto; display:block; }}
  .sw{{ display:inline-block; width:12px; height:12px; vertical-align:-1px; margin-right:3px; }} .sw.rev{{ background:#002198 }} .sw.exp{{ background:#a8322c }}
  .cap{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; color:var(--muted); margin:8px 0 0; line-height:1.5; }}
  .tw{{ overflow-x:auto; margin:14px 0 6px; background:var(--card); border:1px solid var(--rule-strong); }} table{{ width:100%; border-collapse:collapse; font-size:.9rem; }}
  th,td{{ text-align:left; padding:9px 11px; border-bottom:1px solid var(--rule); vertical-align:top; }} th{{ font-family:"JetBrains Mono",monospace; font-size:10px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); background:#f3f6f9; white-space:nowrap; }}
  td.n{{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }} td .sub{{ font-family:"JetBrains Mono",monospace; font-size:10px; color:var(--muted); }} td .terms{{ font-size:.84rem; color:var(--muted); margin-top:4px; }} td.note{{ font-size:.84rem; color:var(--muted); min-width:220px; }}
  .sources ol{{ font-size:.93rem; color:var(--muted); padding-left:1.4em; }} .sources li{{ margin:0 0 .55em; }} .sources .tag{{ font-family:"JetBrains Mono",monospace; font-size:9.5px; letter-spacing:.05em; text-transform:uppercase; color:var(--steel-deep); border:1px solid var(--rule-strong); padding:1px 5px; margin-left:7px; }}
  footer{{ padding:28px 0 64px; font-family:"JetBrains Mono",monospace; font-size:11px; color:var(--muted); line-height:1.7; }} footer .bar{{ height:3px; background:var(--navy); margin:0 0 16px; width:48px; }}
</style>
<link rel="stylesheet" href="assets/kromer-theme.css">
</head>
<body>
<div class="hubbar"><div class="hubbar-in"><a class="back" href="index.html">&larr; Learn About Berkeley</a><span class="stamp">{esc(n.get("eyebrow","Fund ledger"))}</span></div></div>
<main class="wrap">
  <header class="masthead">
    <div class="eyebrow"><span class="tick"></span> Following the money</div>
    <h1>{n.get("title", esc(d["name"]))}</h1>
    <p class="dek">{esc(n.get("dek",""))}</p>
    <div class="meta-row"><span><b>Fund</b> {esc(d["fund_number"])} · {esc(d["type"].replace("_"," "))}</span><span><b>Department</b> {esc(d["department"])}</span><span><b>Ledger updated</b> {esc(d["status"]["last_update"])}</span><span><b>Data</b> <a href="data/funds/{esc(d["fund_number"])}.json">{esc(d["fund_number"])}.json</a></span></div>
    <div class="legend"><div class="lt">How to read the confidence labels</div><div class="chips"><span class="chip hi">High</span><span class="chip mod">Moderate</span><span class="chip low">Low</span><span class="chip unk">Unknown</span></div></div>
  </header>

  <div class="verdict" role="note" aria-label="Bottom line"><div class="vk">Bottom line</div><p class="vt">{n.get("verdict_title","")}</p><p>{esc(n.get("verdict",""))}</p></div>

  <section>
    <span class="sec-no">01</span><h2>How the fund was set up</h2>
    <p class="lead">{esc(n.get("setup",""))} {chip("High")}</p>
    <div class="statrow">
      <div class="stat"><div class="v">{d["established"]["year"] or "—"}</div><div class="l">{"Established, to receive a $1.8M State loan" if d["established"]["year"] else "Year established: not yet researched"}</div></div>
      <div class="stat"><div class="v">{money((latest.get("revenue") or 0)-(latest.get("expenditure") or 0), True)}</div><div class="l">FY{latest["fy"]} result, audited</div></div>
      <div class="stat"><div class="v">{money(rescue_total, True) if flows else money(latest.get("transfers_in") or 0, True)}</div><div class="l">{"Moved in from other pockets since FY2022 (ledger, section 05)" if flows else f"Transfers in, FY{latest['fy']}"}</div></div>
      <div class="stat"><div class="v">{money(unfunded["amount"], True) if unfunded else money(latest.get("ending_balance"), True)}</div><div class="l">{("Unfunded capital need, " + esc(unfunded["as_of"][:7]) + "; no reserve") if unfunded else f"Balance, June 30, {latest['fy']}"}</div></div>
    </div>
  </section>

  <section>
    <span class="sec-no">02</span><h2>Every year, audited</h2>
    <p class="lead">{"Revenue against expenses, FY2015 to the staff forecast for FY2028. The fund covered its costs in " + str(covered) + " of the " + str(len(audited)) + " audited years shown" + (", and in none of the last three." if len(audited) >= 3 and not any(y["revenue"] >= y["expenditure"] for y in audited[-3:]) else ".") if len(audited) > 1 else "Revenue against expenses for the one audited year loaded so far."}</p>
    <div class="chartwrap">{chart}</div>
    <div class="tw"><table><thead><tr><th>Year</th><th>Basis</th><th>Revenue</th><th>Expenses</th><th>Result</th><th>Balance / net position</th><th>Conf.</th><th>Note</th></tr></thead><tbody>{''.join(arows)}</tbody></table></div>
  </section>

  {'' if not assets_html else f"""<section>
    <span class="sec-no">03</span><h2>The assets</h2>
    <p class="lead">Two views: the physical system the fund is charged with maintaining, with staff's unfunded need by class, and what the audited balance sheet says the fund owns.</p>
    {assets_html}
  </section>"""}

  <section>
    <span class="sec-no">04</span><h2>Where the money comes from and goes, FY{(F or d.get("flow_detail") or {}).get("fy", "")}</h2>
    <p class="lead">{esc(n.get("flow_lead", "One audited year, as the statement reports it: the fund's own revenue sources on the left, its spending by line on the right, and any transfers or loans in shown as rescue money."))}</p>
    {flow_html}
  </section>

  {'' if not flows else f"""<section>
    <span class="sec-no">05</span><h2>The flow ledger: every dollar moved in or out</h2>
    <p class="lead">Each row is one action that is not the fund's own revenue or ordinary spending, with the document that authorized it. Rows are recorded only against a primary source.</p>
    <div class="tw"><table><thead><tr><th>FY</th><th>Kind</th><th>Amount</th><th>From → to</th><th>What and why</th><th>Instrument</th><th>Conf.</th></tr></thead><tbody>{''.join(frows)}</tbody></table></div>
    <div class="cap">Kinds: transfer in, cost shift, loan, grant, indirect-cost reduction and charge holiday count as rescues (the {money(rescue_total, True)} in section 01). Fee changes, reductions and revenue at risk are the fund's own measures and are listed for completeness.</div>
  </section>"""}

  {'' if not orows else f"""<section>
    <span class="sec-no">06</span><h2>What the fund owes</h2>
    <div class="tw"><table><thead><tr><th>Obligation</th><th>Amount</th><th>As of</th><th>Note</th><th>Conf.</th></tr></thead><tbody>{''.join(orows)}</tbody></table></div>
  </section>"""}

  {'' if "tot" not in d else f"""<section>
    <span class="sec-no">07</span><h2>What about the hotel tax?</h2>
    <p class="lead">{esc(n.get("tot_lead",""))}</p>
    <div class="statrow">
      <div class="stat"><div class="v">{money(T["waterfront_tot_per_year"][0], True)}–{money(T["waterfront_tot_per_year"][1], True)}</div><div class="l">Waterfront TOT per year (staff, 2023)</div></div>
      <div class="stat"><div class="v">{money(T["citywide_tot"]["fy2027_proposed"], True)}</div><div class="l">Citywide TOT, FY2027 budget</div></div>
      <div class="stat"><div class="v">~$1.0M</div><div class="l">Operating gap, staff forecast FY27–28</div></div>
      <div class="stat"><div class="v">{money(unfunded["amount"], True)}</div><div class="l">Capital need the TOT would not touch</div></div>
    </div>
    {tot_points}
    <div class="panel"><div class="pk">Where the idea is strongest</div><p>{esc(n.get("tot_close",""))} {chip("Moderate")}</p></div>
    <div class="cap">Pledge: {esc(T["pledge"])}. Sources: Council Item 19, July 25, 2023; FY2027–28 proposed budget, General Fund revenue by category. {chip(T["confidence"])}</div>
  </section>"""}

  {'' if not findings else f"""<section>
    <span class="sec-no">08</span><h2>What the ledger shows</h2>
    {findings}
  </section>"""}

  {'' if not n.get("counter") else f"""<section>
    <span class="sec-no">09</span><h2>The counterargument</h2>
    <div class="panel"><div class="pk">Strongest case against this page</div><p>{esc(n.get("counter",""))} {chip("Moderate")}</p></div>
  </section>"""}

  <section>
    <span class="sec-no">10</span><h2>Open questions and next entries</h2>
    <h3>Open questions</h3><ul class="clean">{openq}</ul>
    <h3>Next entries</h3><ul class="clean">{nextq}</ul>
  </section>

  <section class="sources">
    <span class="sec-no">Sources</span><ol>{sources}</ol>
    <p class="cap">This page is generated from <a href="data/funds/{esc(d["fund_number"])}.json">the fund's ledger file</a> by <code>tools/build_fund_page.py</code>. The schema is in <code>data/funds/SCHEMA.md</code>. Flows proposed by an agent and not yet reviewed are not shown.</p>
  </section>

  <footer><div class="bar"></div>Learn About Berkeley &middot; built from public documents &middot; residents decide. Maintained by Steve Kromer, candidate for Berkeley City Council District 1. The page records what the City's own documents say about one fund; the findings are labeled, and the counterargument is published alongside.</footer>
</main>
</body>
</html>
'''
    out_path.write_text(page)
    data_dir = out_path.parent / "data" / "funds"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(json_path, data_dir / json_path.name)
    print(f"wrote {out_path} ({len(page):,} bytes); copied {json_path.name} to {data_dir}")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--all":
        data_dir, docs = Path(sys.argv[2]), Path("docs")
        for jp in sorted(data_dir.glob("*.json")):
            fid = jp.stem
            out = docs / ("fund-608-marina.html" if fid == "608" else f"fund-{fid}.html")
            build(jp, out)
        sys.exit(0)
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    build(Path(sys.argv[1]), Path(sys.argv[2]))
