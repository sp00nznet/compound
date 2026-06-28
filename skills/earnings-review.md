# Close Reading of Earnings: A Deep Read of Primary Sources

Run a close-reading earnings analysis on $ARGUMENTS.

**Supported input format**: `company quarter`, e.g. `腾讯 2025Q4`, `PDD 2025年报`, `美团 最新` (defaults to the most recent period).

> "I never read sell-side reports — only the raw filings." — Li Lu
>
> "I read 500 pages a day. That's how knowledge builds up, like compound interest." — Buffett

## Design Philosophy

Most AI research tools rely on secondhand information (news, report summaries, data sites). But Buffett's and Li Lu's core ability is **reading primary sources** — annual reports, quarterly reports, earnings-call transcripts.

The problems with secondhand information:
- It's filtered — analysts selectively present data favorable to their view
- It lags — by the time others have digested it, the alpha is gone
- It lacks context — "revenue grew 15%" stripped of management's discussion of growth quality

This skill reads primary sources directly, focused on what Buffett and Li Lu actually look at.

## Execution Flow

### Pre-step: Rate source availability

| Grade | Trait | Impact |
|------|------|------|
| Grade A | Obtained the full original text (10-K / annual report / call transcript) | Run all steps normally |
| Grade B | Only partial original text or third-party summaries | Flag "non-primary source", lower the weight of footnote analysis |
| Grade C | Only news coverage and data-site summaries | Focus on core financial-data changes, skip footnote mining, flag "insufficient primary sources" |

### Step 1: Obtain primary sources

Use the Task tool to launch multiple background agents to fetch the following raw materials **in parallel**:

1. **Original filing**: from the company IR page, SEC EDGAR (US 10-K/10-Q), HKEX Disclosure (HK), cninfo (A-shares)
2. **Earnings-call transcript/audio**: from Seeking Alpha, the company IR page, Xueqiu, etc.
3. **Letter to shareholders** (if annual report): read in full
4. **Investor-day / analyst-day materials** (if recent)

If the full original text can't be obtained, piece it together from standard data sources per the `skills/financial-data.md` spec (US: macrotrends+stockanalysis; HK: aastocks+macrotrends; A-shares: Eastmoney+cninfo), but you must flag "not the original filing, from third-party summaries", and mark any key data where two sources differ by >1%.

### Step 2: Extract and verify core financial data

#### 2.1 Income statement

| Metric | This period | Prior period | YoY change | Guidance | Met? |
|------|------|------|---------|-----------|---------|

Must cover:
- Total revenue and the breakdown by business/region
- Gross profit, gross-margin change
- Operating profit, operating-margin change (distinguish GAAP and Non-GAAP)
- Net profit (watch the impact of non-recurring items)
- EPS (basic vs diluted)

#### 2.2 Cash-flow statement (Buffett's top priority)

| Metric | This period | Prior period | Change | What to watch |
|------|------|------|------|--------|

Must cover:
- Operating cash flow vs net profit ratio (>100% is good, <80% warrants caution)
- Capex and its composition (maintenance vs expansion)
- Free cash flow = operating cash flow − capex
- Buyback amount, dividend amount
- Cash and equivalents, period-end balance

#### 2.3 Balance-sheet health

Must cover:
- Cash + short-term investments vs interest-bearing debt
- Net-cash / net-debt trend
- Days receivable change (loosening credit terms to juice revenue?)
- Days inventory change (building up stock?)
- Goodwill and intangibles as a share (any impairment risk?)

**Data verification**: use `tools/financial_rigor.py` to verify key data:

```bash
# Cross-validate revenue and net profit (at least 2 sources)
python3 tools/financial_rigor.py cross-validate \
  --metric "revenue" --values 108.3e9 107.9e9 --sources "公司财报" "Yahoo Finance"

# Verify market cap
python3 tools/financial_rigor.py verify-market-cap \
  --price 101 --shares 1.488e9 --reported 1.44e11 --currency USD

# Verify valuation metrics
python3 tools/financial_rigor.py verify-valuation \
  --price 101 --eps 9.6 --bvps 26.5 --fcf-per-share 10.2
```

### Step 3: Close read of management discussion (MD&A)

This is where Buffett and Li Lu spend the most time. Not reading the numbers — **listening to how management talks.**

#### 3.1 Management-tone analysis

Read the management discussion / call remarks paragraph by paragraph, flagging the following signals:

| Signal type | Concrete sign | Example |
|---------|---------|------|
| 🟢 **Candor signal** | Proactively admits problems, gives specific causes | "Margin fell this quarter mainly because our investment in X exceeded expectations" |
| 🟢 **Clarity signal** | Specific strategy statements, quantified targets | "We plan to raise X's market share from 15% to 20% over the next 12 months" |
| 🔴 **Vagueness signal** | Heavy use of empty phrases like "we believe", "over the long term" | "We're confident about the future" |
| 🔴 **Deflection signal** | Dodges direct questions, changes the subject | Asked about margin, pivots to revenue growth |
| 🔴 **Externalizing blame** | Pins all problems on macro/industry/competitors | "Due to the macro environment..." |

#### 3.2 Promise tracking

Extract management's specific promises from the prior period's earnings/call, and compare against this period's actuals:

| Prior promise | This-period delivery | Verdict |
|---------|------------|------|
| "Margin will recover to X% in H2" | Actual Y% | ✅ met / ❌ missed / ⚠️ partly met |

**Duan Yongping**: "The simplest way to tell whether a management team is reliable is to check whether they did what they said before."

#### 3.3 Identifying the key questions

From the call Q&A, extract the sharpest analyst questions and the quality of management's answers:

| Analyst question | Management answer | Answer quality (1-5) | Dodged? |
|-----------|-----------|:------------:|:-------:|

### Step 4: Footnote and hidden-information mining

The footnotes hide information management doesn't want you to find easily:

#### 4.1 Mandatory footnote items

- [ ] **Related-party transactions**: are the terms with major/related parties fair?
- [ ] **Stock-based compensation**: how big is the dilution from options/RSUs? What's the strike price?
- [ ] **Contingent liabilities**: off-balance-sheet risks — litigation, guarantees, commitments
- [ ] **Accounting-policy changes**: did they change revenue recognition, depreciation life, etc.?
- [ ] **Segment information**: margin differences across businesses — any "good business subsidizing bad business"?
- [ ] **Customer/supplier concentration**: top-five customer/supplier share

#### 4.2 Anomaly detection

- [ ] Receivables growth > revenue growth (possibly channel stuffing)
- [ ] Inventory growth > revenue growth (possibly piling up)
- [ ] Operating cash flow < net profit and the gap is widening (profit quality questionable)
- [ ] Capitalized spending suddenly rising (possibly dressing up profit)
- [ ] Non-recurring gains' share suddenly rising

### Step 5: Compare against historical data

#### 5.1 Trend analysis

Place this period's key metrics into a time series of at least 4 quarters (or 3 years of annual reports):

| Metric | Q-4 | Q-3 | Q-2 | Q-1 | This period | Trend call |
|------|-----|-----|-----|-----|------|---------|

Focus on:
- Is margin improving or deteriorating?
- Is revenue growth accelerating or decelerating?
- Is cash-flow quality rising or falling?
- Is capex intensity increasing or decreasing?

#### 5.2 Compare against management guidance

| Metric | Prior guidance | Actual result | Variance | Interpretation |
|------|--------------|---------|------|------|

### Step 6: Output the close-reading report

#### Report structure

```
1. Core data snapshot (one-page table)
2. The 3 most important changes this period (under 500 characters)
3. Management tone and promise tracking
4. Hidden information in the footnotes
5. Key questions (selected call Q&A)
6. Relationship to the investment thesis (if holding)
7. Conclusion: what did this report change?
```

#### The conclusion must clearly answer

1. **Was this report a beat, in line, or a miss?** (no "broadly in line" followed by a pile of two-handed waffle)
2. **Impact on the investment thesis**: strengthened / no impact / weakened / broken
3. **What's the next catalyst to watch?**
4. **If you already hold, add / hold / trim?**

### Step 7: Save the report

Write the report to `reports/{company_name}-earnings-{period}.md`, e.g. `reports/tencent-earnings-2025Q4.md`.

### Step 8: Data spot-check (release gate)

After the report is written, run a data spot-check; only pass it to release:

```bash
# Step 1 — extract the spot-check list
python3 ~/compound/tools/report_audit.py extract \
  --report reports/{company_name}-earnings-{period}.md

# Step 2 — pull each item from a reliable source (see skills/financial-data.md)

# Step 3 — output the pass/reject verdict
python3 ~/compound/tools/report_audit.py verdict \
  --results '<filled-in JSON>' \
  --report {report filename}
```

**[Pass]** all checks pass → release; **[Reject]** any check fails → fix and re-review.

## Key Principles

- **Read the original, not the summary**: do everything possible to get primary sources
- **Watch changes, not absolute levels**: the trend matters more than the number itself
- **Listen to tone, not just content**: how management says it matters as much as what they say
- **Read the footnotes, not just the body**: the devil is in the details
- **Give a conclusion, don't just summarize**: the point of close reading is to form a judgment, not to recite the filing
