# Buffett Value-Investing Pre-Buy Checklist

Run a Buffett value-investing pre-buy checklist analysis on $ARGUMENTS.

**Supported input format**: one or more companies, separated by comma / Chinese comma / space. E.g. `腾讯, 茅台, 英伟达` or `NVDA AAPL MSFT`.

## Execution Flow

### Step 1: Parse the input, identify all companies to analyze

Parse all company names/tickers from $ARGUMENTS. For each company, determine:
- Full name, ticker, exchange
- If unlisted, mark it "unlisted" with a brief note (whether there's an indirect investment route), and skip the full checklist

### Step 1.5: AI research-bias warning

Give each company a quick "information richness" grade (A/B/C) and note it in the report:

| Grade | Criteria | Impact on the checklist |
|------|---------|-----------------|
| Grade A | Listed for years, abundant data | Run normally, but beware the "consensus trap" — all metrics looking clear doesn't mean it's truly certain |
| Grade B | Limited data, needs estimation | Flag a confidence level for each estimated metric; weight data reliability into the "good business" judgment |
| Grade C | Extremely scarce information | Don't force-fill the six-gate table; honestly flag "insufficient data to judge", focus on the verifiable core questions |

**Core principle**: the checklist's goal is to **exclude bad choices**. For Grade C companies, "insufficient data" means neither "fail" nor "pass" — it should be honestly flagged "gray zone, needs more primary information", rather than rejected just because AI couldn't fill the table.

Duan Yongping once said: "can't understand" comes in two forms — one is the business is genuinely too complex, the other is you simply haven't put in the time. A limitation of AI research is that it easily conflates "scarce material" with "can't understand".

### Step 2: Parallel data collection

Use the Task tool to launch an independent background agent for **each company** (all companies launched in parallel). Each agent collects:

1. **Profitability**: ROE (5-10 year trend), gross margin, net margin, free cash flow
2. **Valuation data**: current price, market cap, PE (TTM), forward PE, PB, dividend yield
3. **Growth trend**: last-3-year revenue/profit growth
4. **Financial health**: debt level, capex needs, cash reserves, net cash/net debt
5. **Competitive landscape**: market share, main competitors, share-change trend
6. **Moat evidence**: concrete evidence for brand/switching cost/network effect/scale effect/tech barrier
7. **Management record**: CEO background, key decisions, stake, capital-allocation record
8. **Latest developments**: major events in the last 6 months (earnings, M&A, regulation, management changes, etc.)

### Step 3: Run the six-gate checklist per company

For each listed company, pass through the six gates in order:

---

#### Gate 1: Can I understand this business? (circle of competence)

Must answer:
- [ ] Can you explain in one sentence how this company makes money?
- [ ] What business will it most likely still be in 10 years from now?
- [ ] Which key variables decide success or failure?
- [ ] Does your understanding of this industry come from deep research or hearsay?

**Scoring (★1-5)**:
- ★★★★★: business model extremely simple and clear, high 10-year certainty (e.g. Moutai: brew liquor, sell liquor)
- ★★★★☆: model clear but with a technical barrier, needs some expertise to understand
- ★★★☆☆: model understandable but 10-year certainty low, industry changes fast
- ★★☆☆☆: business lines complex or industry in upheaval, hard to predict the future
- ★☆☆☆☆: entirely outside the circle of competence

**Hard rejection**: if you can't even explain how it makes money, mark it "outside circle of competence, no analysis".

---

#### Gate 2: Is this a good business? (economic characteristics)

Let the data speak; **key metrics must be computed precisely with the tool**:

```bash
python3 ~/compound/tools/financial_rigor.py verify-valuation \
  --price {price} --eps {EPS} --bvps {bvps} --fcf-per-share {fcf_per_share} --dividend {dividend_per_share}
```

| Metric | This company's value | Reference standard | Verdict |
|------|-----------|---------|------|
| ROE (5-year avg) | | >15% excellent, >20% outstanding | |
| Gross margin | | >40% implies pricing power | |
| Free cash flow | | consistently positive, ≈ net profit | |
| Capex intensity | | asset-light beats asset-heavy | |
| Debt level | | interest-bearing debt / net profit < 3 years | |

**Scoring (★1-5)**:
- ★★★★★: ROE>25%, high margin, strong FCF, asset-light, low debt (all met)
- ★★★★☆: 4 met
- ★★★☆☆: 3 met
- ★★☆☆☆: 2 met or trend deteriorating
- ★☆☆☆☆: most not met, or FCF persistently negative

---

#### Gate 3: Is the moat deep enough? (competitive advantage)

Check item by item:

| Moat type | Present? | Concrete evidence | Widening or narrowing? |
|-----------|---------|---------|--------------|
| Brand / pricing power | | | |
| Switching cost | | | |
| Network effect | | | |
| Cost / scale advantage | | | |
| Tech / patent barrier | | | |

Additional test: given a competitor ¥10B, could they replicate this business?

**Scoring (★1-5)**:
- ★★★★★: multiple moats stacked and widening
- ★★★★☆: at least one strong moat and stable
- ★★★☆☆: has a moat but not deep enough, or trend unclear
- ★★☆☆☆: moat being eroded
- ★☆☆☆☆: no obvious moat

---

#### Gate 4: Is management trustworthy? (the human factor)

| Check item | Assessment |
|--------|------|
| Honesty (promise vs delivery) | |
| Capital-allocation ability (buyback/dividend/M&A record) | |
| Shareholder orientation (stake, compensation) | |
| Owner mindset (founder vs professional manager) | |
| Corporate governance (related-party transactions, goodwill, audit) | |
| Can it run normally after the CEO leaves? | |

**Scoring (★1-5)**:
- ★★★★★: founder at the helm, outstanding capital allocation, fully aligned interests
- ★★★★☆: excellent management with minor flaws
- ★★★☆☆: competent management but with governance concerns
- ★★☆☆☆: has integrity or governance problems
- ★☆☆☆☆: serious integrity problem (→ hard rejection)

---

#### Gate 5: Is the price cheap enough? (margin of safety)

| Metric | Value | Historical percentile | Verdict |
|------|------|---------|------|
| PE (TTM) | | | |
| Forward PE | | | |
| PB | | | |
| Dividend yield | | | |
| FCF Yield | | | |

Additional test (**must be computed precisely with the tool, no mental math allowed**):
```bash
python3 ~/compound/tools/financial_rigor.py three-scenario \
  --price {price} --eps {EPS} --shares {shares_100m} \
  --growth {optimistic} {neutral} {pessimistic} --pe {optimistic_pe} {neutral_pe} {pessimistic_pe} --currency {currency}
```
- Valuation range under three scenarios (use the tool output)
- If your judgment is wrong, how much can you lose at most buying at the current price?
- If the stock halves, do you dare to add?

**Scoring (★1-5)**:
- ★★★★★: below 50% of intrinsic value, extreme margin of safety
- ★★★★☆: 70% of value, good margin of safety
- ★★★☆☆: fair valuation, average margin of safety
- ★★☆☆☆: a bit expensive, insufficient margin of safety
- ★☆☆☆☆: severely overvalued

---

#### Gate 6: Position sizing and decision discipline (preventing emotional loss of control)

Check for these emotional signals:
- Do you want to buy because of FOMO?
- Do you want to buy only because someone recommended it?
- If it were suspended from trading for 5 years, could you accept it?
- Can you write the buy thesis clearly in under 200 characters?

---

### Step 4: The mirror test

For each company, write out the mirror-test statement:

> "I buy ___ shares of ___ at ¥___ because:
> 1. The essence of this business is ___, and I understand it;
> 2. Its moat is ___, and it's widening/narrowing;
> 3. Management ___, worthy/unworthy of trust;
> 4. The current price equals a ___ discount to intrinsic value, with/without sufficient margin of safety;
> 5. Even if I'm wrong, the downside is controllable/uncontrollable, because ___."

**Can't complete the 5 sentences = don't buy.** Clearly mark "pass" or "fail".

---

### Step 5: Quick-rejection checklist

Check each item per company; triggering any one means mark it "rejected":

- [ ] Can't explain how this company makes money
- [ ] Negative free cash flow for 3 consecutive years with no improvement in sight
- [ ] Management has an integrity blemish
- [ ] Competitive advantage being irreversibly eroded
- [ ] Relies on "the next buyer paying more" to make money (greater-fool)
- [ ] Can't bear the consequences of this investment going to zero
- [ ] The buy reason is mainly "everyone's buying" or "it's been rising lately"
- [ ] Can't write the buy reason clearly in under 200 characters

---

### Step 6: Output the overview comparison table (mandatory for multiple companies)

When analyzing multiple companies, you must generate a comparison overview table:

| Company | Checklist passed? | Circle | Good business | Moat | Management | Margin of safety | Core conclusion |
|------|----------------|--------|--------|--------|--------|---------|---------|
| | | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | |

---

### Step 7: Final conclusion and write to file

Give a clear conclusion per company (don't dodge):
- ✅ **Passed the checklist** (X/6 gates) — can move to the deep-research stage
- ❌ **Failed the checklist** — explain which red line was triggered
- ❓ **Gray zone** — explain the key point of contention and what the investor must judge for themselves
- N/A — unlisted / cannot be bought

Write the complete report to `~/buffett-checklist-[company_name or "multi-company"].md`.

## Output-Format Requirements

1. Each company is its own chapter, containing: six-gate scorecard + core-data table + key risks (3-5) + mirror test + clear conclusion
2. For multiple companies, append an overview comparison table at the end
3. All scores must use ★ symbols (★1-5), no half-stars
4. Data must cite the source date; estimates must be marked "estimate"
5. End with a closing note echoing Buffett's saying: "The first rule of investing is don't lose money"
6. Language style: direct, sharp, no fluff. Weave in Buffett/Munger/Duan Yongping quotes as commentary

## Key Principles

- **Better to miss than to err**: the checklist's goal is to exclude bad choices, not to find the best one
- **Be honest about the circle of competence**: if you don't understand it, say so; don't force the analysis
- **Margin of safety is the lifeline**: even a great company will lose money if bought too expensively
- **The mirror test can't be skipped**: if you can't explain the reason clearly, don't buy — no exceptions
