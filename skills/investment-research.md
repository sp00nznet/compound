# Investment Research: Buffett-Munger-Duan Yongping-Li Lu Four-Master Integrated Analysis Framework

Conduct systematic investment research analysis on $ARGUMENTS.

## Research Framework

Based on the methodologies of four investment masters — Buffett, Munger, Duan Yongping, and Li Lu — execute the research in the following seven modules in order:

### Preliminary Step: AI Research Bias Awareness (mandatory)

Before starting research, assess the company's "AI researchability" and identify potential data bias:

**Information Richness Rating**:
| Tier | Characteristics | AI Research Trap | Countermeasure |
|------|------|-----------|---------|
| Tier A (information-rich) | Listed for many years, heavy broker coverage, dense media reporting | Consensus too strong; AI output converges with market pricing, limited alpha | Focus on contrarian checks: why aren't smart people buying? What risk is being overlooked? |
| Tier B (moderate information) | Listed 1-3 years, limited coverage, some data must be estimated | AI may fill gaps with "reasonable guesses" — looks complete but is actually false certainty | Tag each estimated data point with a confidence level; distinguish "evidence-based estimate" from "fabricated filler" |
| Tier C (information-scarce) | Just listed / obscure stock / emerging market, almost no coverage | AI turns overly conservative due to insufficient material, misjudging "can't see clearly = bad" | Use first-principles questioning (see below) to extract the business essence from limited information |

**First-Principles Research Method for Tier C Companies**:
When public information is insufficient, don't try to cobble together a report that "looks complete." Instead, focus on these underlying questions:
1. Who is the customer? Why do they pay? Are there alternatives?
2. What drives repeat purchases? Habit, lock-in, or continuously created new value?
3. Could a competitor replicate this business with 10 billion in hand?
4. What key decisions has management made? What judgment and values do those decisions reflect?

**Bias Self-Check List** (stay vigilant throughout the research):
- [ ] Does my sense of "certainty" come from the nature of the business, or from the quantity of material?
- [ ] If I halved the amount of material on this company, would my conclusion change?
- [ ] Is the AI's analysis highly similar to market consensus? If so, where is my informational edge?
- [ ] Is the possibility of "very little public material but an excellent business" being underestimated?

Write the information richness rating result at the start of the report, and in the final conclusion note the difference between "AI research confidence" and "actual investment certainty."

### Step 1: Data Collection

> **Data source standard**: see `skills/financial-data.md`. All financial data must come from two independent sources; discrepancies >1% must be flagged.
> - US stocks: macrotrends (primary) + stockanalysis (secondary)
> - HK stocks: aastocks (primary) + macrotrends ADR (secondary)
> - A-shares: East Money (primary) + CNINFO (secondary)

Use the Task tool to launch a background Agent to collect the following data from the web:

1. Revenue structure: most recent fiscal year and last 4 quarters of segment revenue, growth rate, gross margin
2. Financial metrics: last 5 years of revenue, net income, gross margin, operating margin, free cash flow, cash reserves
3. Competitive landscape: market share, comparison with main competitors
4. Business model and moat: source of core competitive advantage
5. Technical capability: core tech stack, R&D investment
6. Management: founder/CEO background, ownership stake, record of key decisions
7. Industry outlook: TAM (total addressable market), growth forecasts
8. Risk factors: geopolitics, regulation, supply chain, etc.
9. Current valuation: market cap, PE, PS, PEG, EV/Revenue
10. Core arguments from both bulls and bears

#### Data Cross-Validation (mandatory, use the financial rigor tool)

After data collection is complete, **you must call `tools/financial_rigor.py` to programmatically verify the key data**, eliminating LLM mental-math errors.

**Data points that must be verified**:
- Total shares outstanding (confirm from at least 2 sources such as the exchange, Yahoo Finance, StockAnalysis)
- Current price and market cap (**manually compute price × shares and compare against reported market cap to prevent unit errors**)
- Most recent fiscal year revenue and net income (confirm from the company's annual report + at least 1 third-party source)
- Cash reserves and net cash (cash + short-term investments − total debt; mind the differences in definition)
- Management ownership stake (distinguish economic interest from voting rights; mind dual-class share structures)

**Mandatory verification steps (call the tool via Bash)**:

Step 1 — Market cap recalculation (precise decimal, not floating point):
```bash
python3 ~/compound/tools/financial_rigor.py verify-market-cap \
  --price {price} --shares {shares} --reported {reported_market_cap} --currency {currency}
```

Step 2 — Multi-source cross-validation of key data:
```bash
python3 ~/compound/tools/financial_rigor.py cross-validate \
  --field {field} --values '{"source1": value, "source2": value}' --unit {unit}
```
Execute separately for revenue, net income, and cash reserves.

Step 3 — Precise recalculation of valuation metrics (PE/PB/ROE/FCF Yield, etc.):
```bash
python3 ~/compound/tools/financial_rigor.py verify-valuation \
  --price {price} --eps {EPS} --bvps {bvps} --fcf-per-share {fcf_per_share} --dividend {dividend}
```

**Verification rules**:
1. Each key data point needs at least 2 independent sources
2. When sources differ, prefer the company's annual report / exchange data, and note the reason for the discrepancy
3. **All data involving calculation must be verified through the tool; LLM mental math is forbidden**
4. Embed the tool output directly into the report appendix "Key Data Cross-Validation Record"
5. If the tool reports ❌ excessive deviation, you must investigate the cause before continuing the analysis

**Common Error Prevention**:
- Market cap units: HKD 100M vs RMB 100M vs USD 100M — easy to drop or add a zero
- FCF definition: different sources may define capex differently (whether it includes leases, acquisitions, etc.)
- Debt definition: whether operating lease liabilities are included
- Ownership stake: a dual-class company's economic interest ≠ voting rights

### Step 2: Business Essence Analysis — Duan Yongping's "Right Business"

Analysis points:
- Define the essence of this business in one sentence
- Revenue structure breakdown (chart)
- 5-year profitability trend (chart)
- Business model canvas: one-time sale vs subscription/repeat purchase? Hardware vs software vs platform?
- Ecosystem stickiness / customer lock-in strength
- Gross margin level and comparison with peers; explain why it's high/low
- Operating leverage analysis
- **Duan Yongping-style probe**: What's good about this business? If you could describe it in only one sentence, what would it be?

### Step 3: Moat Assessment — Buffett's "Economic Moat"

Verify each of the five moat types one by one:

| Moat Type | Verification Method |
|-----------|---------|
| Brand / pricing power | Can it raise prices without losing sales volume? |
| Switching costs | How high is the cost for customers to migrate to a competitor? |
| Network effects | Does the product get better as more users join? |
| Economies of scale | How large is the cost advantage that scale brings? |
| Technology / patent barriers | How many years ahead is the technology? Can it be replicated? |

Analyze the moat trend: did it widen or narrow over the past 5 years? Forecast for the next 5 years.

**Buffett-style probe**: Will this moat still be here in 10 years? What could destroy it?

### Step 4: Inversion and Risk Checklist — Munger's "Invert, Always Invert"

- List "all the paths by which this company could fail" (table: path / probability / severity)
- Historical analogy: find companies that were historically in a similar position — how did they end up?
- Cross-disciplinary analysis: cross-validate using models such as network effect theory, technology adoption curves, competitive game theory
- Bias self-check: narrative bias, anchoring effect, survivorship bias
- Collect the bears' core arguments

**Munger-style probe**: Where am I most likely to be wrong? Why would smart people not buy / short this company?

### Step 5: Management Assessment — Duan Yongping's "Right People" + Buffett's "Management Integrity"

- Review of the CEO/founder's key decisions (table: time / decision / outcome / score)
- Capital allocation ability: R&D return on investment, M&A success rate, buyback timing
- Shareholder interest alignment: management ownership, compensation structure, sell-down record
- Organizational capability: team stability, key-person risk
- Corporate culture characteristics

**Duan Yongping-style probe**: If the CEO retired, could this company maintain its competitiveness?

### Step 6: Industry and Civilizational Trend — Li Lu's "Civilizational Evolution Framework"

- Judge whether the industry is in a "civilization-level paradigm shift"
- Historical technological revolution analogies (steam engine / electricity / internet / AI)
- TAM growth curve and ceiling analysis
- The company's position in the industry value chain
- Technology roadmap risk
- Customer/supplier concentration analysis

**Li Lu-style probe**: Looking back 20 years from now, is this company "the Standard Oil of this era" or "a flash-in-the-pan 3Com"?

### Step 7: Valuation and Margin of Safety — Buffett's "Intrinsic Value" + Duan Yongping's "Right Price"

- Current market pricing (key valuation metrics table) — **must be verified through the tool**
- Reverse DCF: what growth expectation does the current price imply?
- Three-scenario valuation — **must be precisely computed through the tool; mental math forbidden**:
```bash
python3 ~/compound/tools/financial_rigor.py three-scenario \
  --price {price} --eps {EPS} --shares {shares_in_100M} \
  --growth {bull_growth} {base_growth} {bear_growth} \
  --pe {bull_pe} {base_pe} {bear_pe} --years 3 --currency {currency}
```
- Compare with the company's own historical valuation
- Compare with peer valuation

**Duan Yongping-style probe**: If the stock market closed for 5 years starting tomorrow, would you be willing to hold at this price?

### Step 8: Integrated Decision Memo

Summary table:

| Dimension | Conclusion | Confidence |
|------|------|--------|
| Business quality (Duan Yongping) | | |
| Moat (Buffett) | | |
| Management (Duan Yongping + Buffett) | | |
| Biggest risk (Munger) | | |
| Civilizational trend (Li Lu) | | |
| Valuation (Buffett + Duan Yongping) | | |

Final decision table:

| Strategy | Recommendation |
|------|------|
| No position | |
| Holding | |
| Sell signal | |
| Add signal | |

Simulated commentary from the four masters (use blockquote format).

## Output Requirements

1. All analysis must be backed by data, with sources attached
2. Use Markdown tables to present key data
3. Each module must end with the corresponding master's "probe"
4. Finally, write the complete report to `~/[company_name]InvestmentResearchReport.md`
5. Conclusions must be clear — do not shy away from giving a buy / wait / avoid recommendation
6. The valuation section must give a specific price range
7. **The start of the report** must include an "Information Richness Rating" (A/B/C) and an "AI Research Limitations Statement"
8. **The end of the report** must distinguish "AI analysis confidence" from "investment certainty" — the former depends on the amount of material, the latter on the nature of the business. Clearly tell the reader which conclusions in this report are based on sufficient data and which are based on reasoning from limited information
9. If the company is Tier C (information-scarce), the end of the report must list a "checklist of questions requiring firsthand verification" — advising the reader to supplement the AI's blind spots through field investigation, product experience, supply chain interviews, etc.

## Data Spot-Check (release gate)

After the report is written to file, you **must** run a data spot-check; only after it passes may the report be published:

**Step 1 — Extract the spot-check list (15% random sample):**
```bash
python3 ~/compound/tools/report_audit.py extract \
  --report <report_file_path>
```
Outputs a JSON template, each item containing `fetched_value` (to be filled).

**Step 2 — Fetch and verify:**
For each data point in the list, fetch data from reliable sources per the `skills/financial-data.md` standard
(US stocks: macrotrends+stockanalysis; HK stocks: aastocks+macrotrends; A-shares: East Money+CNINFO),
and fill in `fetched_value` / `fetched_source` / `fetched_value2` / `fetched_source2`.

**Step 3 — Output the verdict:**
```bash
python3 ~/compound/tools/report_audit.py verdict \
  --results '<filled JSON>' \
  --report <report_file_name>
```

- **[PASS]**: all spot-check points deviate ≤ 1% → report may be published
- **[REJECT]**: any point deviates > 1% → fix the corresponding data and re-run the spot-check until it passes
