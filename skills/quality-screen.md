# Quality Screen: 7 Metrics to Quickly Rule Out Non-Tier-1 Companies

Run a quality-elimination screen on $ARGUMENTS to quickly rule out names that don't meet the standard of a tier-1 company.

**Supported input formats**:

| Input type | Example | Notes |
|---------|------|------|
| Single stock | `Tencent, Meituan, Nvidia` | Screen one by one |
| Industry | `China beer industry` `Global cloud computing` `HK sportswear brands` | First search for the industry's major listed companies (10-20), then screen each |
| Market/Index | `Hang Seng Index constituents` `CSI 300` `Nasdaq 100` | Pull the constituent list, then screen each |
| Theme | `China's top 50 high-dividend stocks` `Global AI compute chain` | First search for theme-related companies, then screen each |

In industry/market/theme mode, output additionally includes: pass-rate statistics, in-industry ranking, and a sector comparison summary.

## Design Principles

- **Goal**: Don't wrongly kill any tier-1 great company, but reliably rule out the ones that are definitely not tier-1
- **Logic**: 7 hard metrics + 2 exemption rules; better to let one slip through than to kill one by mistake
- **Scope**: All listed companies (banks/insurers are exempt from metric 3, interest coverage)

---

## The 7 Elimination Metrics

| # | Metric | Exclusion condition | What it measures |
|---|------|---------|-------------|
| 1 | 10-year average ROE | < 8% | Capital efficiency — can shareholders' money beat the opportunity cost |
| 2 | 5-year cumulative free cash flow | Negative | Hard cash — is profit just "paper wealth" |
| 3 | Interest coverage (EBIT/interest) | < 2x | Solvency — ability to service interest |
| 4 | Long-term gross margin | < 15% | Pricing power — is the product/service differentiated |
| 5 | Operating cash flow / net income (5-yr avg) | < 0.7 | Earnings quality — can reported profit be collected as cash |
| 6 | Long-term net margin | < 5% | Risk resilience — does profit go to zero when revenue wobbles |
| 7 | 5-year share count inflation | > 20% (not from M&A) | Shareholder interest — is management diluting your stake |

## The 3 Exemption Rules

### Exemption A: Strategic Investment Phase (applies to metric 1)

If all 3 of the following hold, metric 1 (ROE shortfall) can be waived:
1. Listed for less than 10 years
2. Gross margin > 30% (proves the business model itself has pricing power)
3. Operating cash flow positive for the last 2 years (proves cash-generating ability is in place)

**Logic**: High gross margin + cash flow turning positive shows the business model is sound; low ROE is just because the company is still in its investment phase. Classic case: Meituan.

### Exemption B: Deliberately Low Margin (applies to metric 6)

If both of the following hold, metric 6 (net margin shortfall) can be waived:
1. Gross margin > 30% (able to make money but choosing not to)
2. Net margin has recovered to above 5% in the last 2 years, or shows a clear upward trend

**Logic**: A high gross margin shows pricing power; low net margin is a strategic choice (reinvestment), not a lack of ability. Classic case: Amazon.

### Exemption C: High-Turnover, Thin-Margin Model (applies to metrics 4 and 6)

If all 3 of the following hold, metric 4 (gross margin) and metric 6 (net margin) shortfalls can be waived:
1. ROE > 20% (proves that despite low margins, return on capital is extremely high)
2. Operating cash flow / net income > 1.0 (no earnings-quality problem)
3. The business model is a "membership / platform commission / high-turnover thin-margin" type (profit doesn't show up in product markup)

**Logic**: For some tier-1 companies, profit isn't hidden in the gross margin — it's hidden in membership fees, turnover efficiency, or platform take rates. Their gross and net margins are naturally very low, but an extremely high ROE shows first-class capital efficiency. Classic case: Costco (12% gross margin, 2.5% net margin, but ROE 25%+ and membership renewal rate 90%+).

---

## Execution Flow

### Step 1: Parse input, determine screening scope

**Mode detection**:
- If the input is a specific company name/ticker → **single-stock mode**, go straight to Step 2
- If the input is an industry/market/theme → **batch mode**, first do the following:
  1. Use WebSearch to find the major listed companies in that industry/market/theme
  2. Industry mode: cover the top 15-20 companies by market cap in that industry
  3. Index mode: pull the full constituent list
  4. Theme mode: search for related companies, cover 15-30
  5. List the full company roster for confirmation (if >30 companies, process in parallel batches)

For each company, determine its full name, ticker, and exchange.

### Step 2: Parallel data collection

Launch an independent background Agent for each company, using WebSearch to find the following data:

1. **ROE**: year-by-year ROE for the last 10 years (or since listing), compute the average
2. **Free cash flow**: operating cash flow and capex for the last 5 years, compute 5-year cumulative FCF
3. **Interest coverage**: latest annual EBIT and interest expense, compute the ratio
4. **Gross margin**: gross margin trend over the last 5 years
5. **Operating cash flow / net income**: the ratio over the last 5 years, compute the average
6. **Net margin**: net margin trend over the last 10 years, compute the average
7. **Share count change**: total shares 5 years ago vs. now, compute the inflation ratio

Data source priority: company annual reports > broker research > financial data platforms

### Step 3: Check metric by metric

For each company, check all 7 metrics one by one:
- ✅ Pass
- ❌ Fail
- ⚠️ Borderline (attach the figure and explanation)

If a metric is breached, check whether the corresponding exemption condition is met.

### Step 4: Output results

#### Output format

```markdown
# Quality Screen Results

**Screening date**: {date}
**Number of companies**: {N}

## Summary Table

| Company | ①ROE | ②FCF | ③Int. Cov. | ④Gross Margin | ⑤OCF/NI | ⑥Net Margin | ⑦Dilution | Result |
|------|------|------|----------|---------|---------|---------|-------|------|
| xxx | ✅ 24% | ✅ | ✅ | ✅ 56% | ✅ | ✅ 30% | ✅ | **Pass** |
| yyy | ❌ 3% | ❌ | ❌ | ✅ 20% | ✅ | ❌ 2% | ✅ | **Excluded** |
| zzz | ⚠️→✅ | ✅ | ✅ | ✅ 35% | ✅ | ⚠️→✅ | ✅ | **Pass (exempted)** |

## Companies That Passed (N)
[list]

## Companies Excluded (N)
| Company | Metrics breached | Specific data | Reason for exclusion |
|------|---------|---------|---------|

## Companies Passed via Exemption (N)
| Company | Exemption clause | Specific data | Reason for exemption |
|------|---------|---------|---------|

## Borderline Cases (if any)
[supplementary notes on companies sitting near a threshold]

## Sector Summary (industry/market mode only)

**Pass rate**: {passed}/{total} = {percentage}
**Industry quality assessment**: [overall quality verdict on the industry based on pass rate]

| Quality tier | Companies | Common traits |
|---------|------|---------|
| Tier-1 (all pass + high ROE) | xxx, yyy | ... |
| Acceptable (all pass but mediocre metrics) | aaa, bbb | ... |
| Eliminated | ccc, ddd | ... |

**Industry stock-picking conclusion**: [one-line verdict on whether the industry is worth digging into, and which 2-3 names most deserve attention]
```

---

## Notes

1. **Banks/insurers**: metric 3 (interest coverage) does not apply; their business model is fundamentally spread-based
2. **REITs**: ROE can swing wildly due to property revaluation; use "core operating profit ROE" instead
3. **Insufficient data**: if a data point can't be obtained, mark it as "insufficient data" rather than declaring an automatic pass/fail
4. **Cyclical industries**: use averages over a full cycle (covering at least one peak and one trough), not a single year
5. **Short listing history**: for companies listed less than 5 years, use all available data but flag "insufficient data window" in the results

## Limitations Statement

These metrics can rule out companies that are "definitely bad," but passing the screen does not mean a company is "definitely good." A company that passes still needs further research:
- Whether the business model is sustainable
- Whether management is trustworthy
- Whether the current valuation is reasonable
- Whether the competitive landscape is deteriorating

Quality screening is the first step, not the last.
