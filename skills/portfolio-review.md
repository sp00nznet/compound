# Portfolio Management: From "Researching Companies" to "Managing a Portfolio"

Run a portfolio review and optimization on $ARGUMENTS.

**Supported input formats**:
- A holdings list, e.g.: `Tencent 30%, Meituan 20%, Moutai 20%, NVIDIA 15%, Cash 15%`
- Or: `Tencent 500 shares @HKD480, Meituan 1000 shares @HKD130, ...`
- Or: `my portfolio` (if a saved portfolio file `reports/portfolio-latest.md` already exists)

> "Diversification is protection against ignorance. It makes little sense if you know what you are doing." —— Buffett
>
> "In my whole life, the truly great investment opportunities I've seen can be counted on ten fingers." —— Li Lu

## Design Philosophy

Researching companies is only half of investing. The other half is **portfolio-level decisions**:
- How much to buy? (position sizing)
- With what money? (source of funds — new cash or rotating out of an existing position)
- Does it conflict with existing holdings? (correlation)
- What does the optimal portfolio look like? (opportunity cost)

Buffett never looks at a single stock in isolation — he is always asking, "Is this the best thing I can do?"

## Execution Flow

### Step 1: Parse Holdings

Parse the current holdings from the input and standardize them into the following format:

| Name | Ticker | Quantity | Cost Basis | Current Price | Market Value | Weight | P/L |
|------|------|--------|-------|------|------|------|------|

If the input only has percentages and no amounts, analyze by percentage.

At the same time, check whether an existing portfolio file (`reports/portfolio-latest.md`) exists; if so, read and update it.

### Step 2: Pull the Latest Data

Use the Task tool to launch background Agents and, via WebSearch, fetch the following for each holding in parallel:
1. Current stock price and valuation metrics (PE, PB, dividend yield)
2. Key financial changes in the most recent quarter
3. Recent material events
4. Analyst consensus (forward PE, target price)

For each holding, use `tools/financial_rigor.py verify-valuation` to validate the valuation data. Tag each holding by information richness (grade A/B/C); for grade-C holdings, mark the analytical conclusions as low confidence.

### Step 3: Single-Position Checkup

Run a quick health check on each holding:

| Name | Current PE | Has the Buy Thesis Changed | Thesis Health | Position Recommendation |
|------|:------:|:--------------:|:---------:|---------|
| Tencent | 18x | Unchanged | 8/10 | Reasonable |
| Meituan | 25x | Competition intensifying | 6/10 | Overweight, consider trimming |

For each holding, answer:
- [ ] **If you held none today, would you still buy at the current price?**
- [ ] **If you couldn't trade starting tomorrow, would you be comfortable holding for 5 years?**
- [ ] **Is the buy thesis still intact?**

**Duan Yongping**: "If you wouldn't hold a stock for 10 years, don't hold it for even a day."

### Step 4: Portfolio-Level Analysis

#### 4.1 Concentration Analysis

| Metric | Current Value | Recommended Range | Verdict |
|------|-------|---------|------|
| Largest holding weight | | <40% | |
| Top-three holdings weight | | 50-80% | |
| Total number of holdings | | 5-15 | |
| Cash weight | | 10-30% (depending on market conditions) | |

**Li Lu's standard**: 3-5 core holdings, with the top 3 making up 80%+. **But this requires that every one of them be researched thoroughly.**

**Buffett's standard**: no more than 10 core holdings, but more satellite positions are allowed.

#### 4.2 Correlation Check

Identify the hidden linkages between holdings:

| Holding A | Holding B | Correlation Type | Risk |
|-------|-------|---------|------|
| Tencent | Kuaishou | Both China internet | Resonant regulatory risk |
| NVIDIA | TSMC | Upstream/downstream of the AI supply chain | AI Capex moves in the same direction |
| Meituan | Pinduoduo | Both China consumption | Macro consumption moves in the same direction |

**Checklist**:
- [ ] Is more than 50% of the portfolio exposed to the same theme/industry?
- [ ] Is more than 50% of the portfolio exposed to the same country/currency?
- [ ] If US-China relations deteriorate, how much would the portfolio lose?
- [ ] If the global economy enters a recession, how much would the portfolio lose?

#### 4.3 Opportunity Cost Analysis

This is Buffett's most central way of thinking — **every dollar should sit where it earns the highest return**.

Rank all holdings by "expected annualized return":

| Rank | Name | Current Weight | Expected Annualized Return | Certainty | Expected Return × Certainty |
|:----:|------|:-------:|:----------:|:------:|:--------------:|
| 1 | | | | | |
| 2 | | | | | |
| ... | | | | | |

Methods for estimating expected return (compute with `tools/financial_rigor.py three-scenario`):
- **Simplified formula**: expected annualized ≈ FCF Yield + expected growth rate (primary method)
- **Value cross-check**: margin-of-safety mean reversion + earnings growth + dividend yield
- **Growth cross-check**: earnings growth × change in a fair PE

**Key question**: For the lowest-ranked holding, is the expected return higher than cash (risk-free rate ~4%)? If not, it should be sold and switched into cash.

#### 4.4 Stress Test

| Scenario | Assumption | Estimated Portfolio Impact | Max Drawdown |
|------|------|-----------|---------|
| Global recession | Corporate earnings fall 20-30% | | |
| US-China conflict escalates | China-concept stocks discounted 50% | | |
| Rate spike | 10-year Treasury → 6% | | |
| Tech bubble bursts | Tech-stock PE compresses 40% | | |

For each scenario, do a qualitative + rough quantitative assessment (based on each holding's industry characteristics and historical valuation swing ranges):
- Which holdings get hit hardest? Rough direction and magnitude range of the impact
- Can the portfolio as a whole withstand it?
- Is a hedge needed?

### Step 5: Optimization Recommendations

#### 5.1 Rebalancing Recommendations

Based on the analysis above, give concrete rebalancing recommendations:

| Action | Name | Current Weight | Recommended Weight | Rationale |
|------|------|:-------:|:-------:|------|
| Add | | | | |
| Trim | | | | |
| Liquidate | | | | |
| New position | | | | |
| Hold | | | | |

#### 5.2 Finding Alternative Candidates

If the portfolio holds positions that are "worse than cash," or if the cash weight is too high, use `/industry-research` or `/investment-checklist` to systematically screen the industries/companies of interest, rather than recommending individual stocks directly within this Skill.

#### 5.3 Cash Management

| Current Cash Weight | Recommended Cash Weight | Rationale |
|:----------:|:----------:|------|

**Buffett**: Currently holds $382B in cash, over 25% of total assets — when no good opportunities can be found, cash is the best position.

### Step 6: Output the Portfolio Report

#### Report Structure

```
1. Portfolio Overview (holdings table + pie-chart description)
2. Single-Position Checkup (health status of each holding)
3. Portfolio Analysis
   - Concentration: over-diversified / over-concentrated?
   - Correlation: hidden linkages and resonant risk
   - Opportunity cost: is the lowest-ranked position worth holding?
   - Stress test: drawdown estimates under extreme scenarios
4. Rebalancing Recommendations (concrete actions + rationale)
5. Next review date and focus areas
```

#### The Conclusion Must Clearly Answer

1. **Overall portfolio health**: Excellent / Good / Needs adjustment / Serious problems
2. **What is the single most important thing to do?** (add X / trim Y / do nothing)
3. **What is the biggest risk right now?**

### Step 7: Save the Portfolio File

Write the portfolio information to `reports/portfolio-latest.md`, including:
- The latest holdings table
- This review's date and conclusions
- Rebalancing log (appended)
- Next review reminder

---

## Key Principles

- **Every dollar has an opportunity cost** — the cost of holding a mediocre stock is missing out on an outstanding one
- **Concentration isn't the risk; ignorance is** — holding 3 stocks you understand deeply is safer than holding 30 you half-understand
- **Cash is a position** — when no good opportunity exists, there's no shame in holding cash
- **Portfolio level > single-stock level** — even a great stock will drag you down at the wrong position size
- **Review regularly, but don't over-trade** — reviewing once a quarter is enough; don't watch the screen and rebalance every day
