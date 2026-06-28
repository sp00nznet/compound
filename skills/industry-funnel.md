# Industry Funnel Screen: A Value-Investing Selection Process from the Whole Market to 3 Names

Run a funnel-style value-investing screen on the $ARGUMENTS industry/theme, going from a whole-market scan to a final shortlist of 3 names, layer by layer.

## When to Use

When you name an industry or investment theme (e.g. "AI compute", "innovative drugs", "robotics") and want to:
1. Miss no important target (incl. A-shares, HK, US, unlisted candidates)
2. Use a single standard to filter out "story stocks" and quality-deficient companies
3. Focus your energy on the 3 leaders truly worth deep research
4. Have a clear keep/drop standard at each layer, reviewable and traceable

Difference from `industry-research`:
- `industry-research` emphasizes supply-chain structure and the full panorama, slicing by link
- `industry-funnel` emphasizes a single-stock selection funnel, refining the whole market layer by layer down to 3 names

The two complement each other: first use `industry-research` to see the supply-chain landscape clearly, then use `industry-funnel` to pick targets.

---

## Funnel Structure Overview

```
Layer 1: whole-market scan       30-60 names   (union of activity + gainers + top-30 market cap)
        ↓ 5 hard value-investing metrics
Layer 2: rough screen            ≤ 10 names    (all 5 pass + moat ★★★ or above)
        ↓ detailed analysis
Layer 3: detailed analysis       ≤ 10 names    (300-500 chars structured analysis each)
        ↓ final selection
Layer 4: four-master deep dive   3 names       (800-1,200 chars each, Buffett/Munger/Duan/Li views)
        ↓
Output: investment recommendation + action signals + position sizing
```

Every layer's "dropped targets" must leave behind a reason for elimination — no black box.

---

## Step 1: Whole-Market Scan Entry

### 1.1 Active-stock definition (union of three classes)

**Class A - trading activity**:
- Top of the industry by avg daily turnover over the last 30 days (top 30 each for A-shares/HK/US)

**Class B - gainers**:
- Top 20 by 30-day gain
- Top 20 by 90-day gain
- Union of the two

**Class C - market-cap anchor**:
- Top 30 by market cap within the industry (regardless of price move)

Final scan pool = A ∪ B ∪ C, expect 30-60 names.

### 1.2 Markets that must be searched

| Market | Suggested source |
|------|---------|
| A-shares (Shanghai/Shenzhen) | THS/Eastmoney industry boards, TDX |
| HK | Futu/THS HK, HKEX industry classification |
| US | NASDAQ/NYSE industry-ETF holdings, Yahoo Finance |
| International | Don't miss relevant JP/KR/TW/EU companies (especially semis, electronics) |
| Unlisted | A separate "future IPO candidates" subsection, noting latest valuation and potential IPO timing |

### 1.3 Output format

| Company | Ticker | Market | Mkt cap | One-line core business | Industry share | Class (A/B/C) |
|-------|------|-----|------|----------|-----------|----------------|

**Key self-check**:
- Be wary of "tangentially related" stocks with industry share < 30%; flag "not a pure-play target"
- Don't miss Chinese/Asian markets just because there's less English material
- Don't miss small caps just because AI favors leaders

---

## Step 2: Rough Screen on 5 Hard Value-Investing Metrics → ≤ 10 names

Apply the 5 hard metrics one company at a time to the 30-60 from Step 1.

### 2.1 The 5 hard metrics

| # | Metric | Pass standard | Relaxation | Data source |
|---|------|---------|---------|---------|
| 1 | PE valuation | Reasonable (vs historical range, peers) | High growth can relax to PEG < 1.5 | Filings + Wind/THS |
| 2 | ROE | > 15% or improving 3-year trend | Asset-heavy industries can relax | Filings |
| 3 | Operating cash flow | Positive and > 70% of net profit | — | Filings |
| 4 | Debt ratio | < 60% | Utilities/power can relax to 70% | Filings |
| 5 | Quick moat assessment | ★★★ or above | — | Qualitative judgment |

**5 moat types**:
- Brand / pricing power
- Switching cost / user stickiness
- Network effect
- Scale effect
- Technology / license / resource barrier

### 2.2 Output format

| Company | PE | ROE | CF/net profit | Debt ratio | Moat | Overall | Keep/drop | Elimination reason |
|------|----|----|-----------|-------|-------|------|------|---------|

**Keep rules**:
- All 5 pass → keep directly
- 4 pass + 1 close → keep but flag yellow
- Fewer than 4 → drop, note the reason

**Target**: keep ≤ 10. If too many are kept (> 12), raise the moat bar to ★★★★ and screen again.

---

## Step 3: Detailed Analysis (≤ 10 names, 300-500 chars each)

For the companies kept in the rough screen, do a structured analysis one by one.

### 3.1 Per-company analysis template

```
## {company_name} ({ticker})

**One-line business model**:
(what it sells, to whom, how it gets paid)

**Financial quality**:
- Revenue growth / profit growth / gross margin / ROE / cash flow
- Key change (the most important financial inflection of the last 1-2 years)

**Moat depth**:
- Main moat type + concrete evidence
- Brief call on whether the moat will still be there in 5 years

**Top 3 risks**:
1.
2.
3.

**Quick valuation**:
- Current PE/PS/EV/EBITDA + position in the historical range
- Peer comparison
- One-line conclusion: expensive / fair / cheap

**Into the final 3?**: yes / no (reason)
```

### 3.2 Selection standard for the final 3

Not picking the top 3 by score, but by "portfolio complementarity":
- At least 1 "high-certainty, low-elasticity" (Buffett type)
- At least 1 "medium-certainty, medium-elasticity" (growth type)
- Optionally 1 "high-elasticity, high-risk" (option type)

If a sub-track can't yield 3 good enough names, write "2 finalists + 1 to watch" rather than padding the count.

---

## Step 4: Four-Master Deep Dive (3 names, 800-1,200 chars each)

Run a four-master deep dive on the 3 finalists.

### 4.1 Duan Yongping's view: business essence

- Define in one sentence what business this company is in
- Is this a good business? Why?
- What is its "本分 (propriety)"? Has management strayed from it?
- Where's the "durability" of the business model?

### 4.2 Buffett's view: moat depth

- Score the five moat types (★1-5), list concrete evidence
- Will the moat still be there in 10 years?
- Where's the "margin of safety" buying now?

| Moat | Strength | Concrete evidence |
|-------|------|---------|
| Brand / pricing power | | |
| Switching cost | | |
| Network effect | | |
| Scale effect | | |
| Tech / license barrier | | |

### 4.3 Munger's view: risks and failure modes

- How is this company most likely to fail? (list the top 3 failure paths)
- What's it worth in the worst case? (bare-bones valuation)
- Why won't smart people buy it? (inversion)
- Any moral / compliance / management risk?

### 4.4 Li Lu's view: civilization-scale trend positioning

- Is the track this company is on a "civilization-scale paradigm shift" or a "phase-driven craze"?
- The closest historical analogy in tech revolutions?
- The endgame for this company in 10-20 years?
- Is it a winner-take-all structure?

### 4.5 Overall recommendation level

```
Recommendation: ★★★★☆
Position type: core / satellite / option / watch
Suggested buy range: current price / pullback N% / patient wait
Suggested position size: X% of this theme's allocation
Key monitoring metric: (what signal would flip this company's thesis)
```

---

## Step 5: Consolidated Output

Consolidate at the end of the report:

### 5.1 Final 3 portfolio table

| Company | Type | Recommendation | Suggested position | Core thesis | Key risk |
|------|------|-------|---------|---------|---------|
| A | Core | ★★★★★ | 50-60% | | |
| B | Satellite | ★★★★☆ | 25-35% | | |
| C | Option | ★★★☆☆ | 5-15% | | |

### 5.2 Industry-level ETF alternative

If you'd rather not pick stocks, list 1-3 relevant ETFs (A-shares/HK/US).

### 5.3 Overall industry-position call

- Industry PE/PB historical percentile
- Fund flows (northbound, ETF creation/redemption, sell-side coverage density)
- Whether the industry overall is in "early / expansion / mature / decline"

### 5.4 Information-sufficiency self-assessment (mandatory)

| Dimension | Grade | Note |
|-----|------|-----|
| Company financial-data completeness | A/B/C | |
| Valuation-data timeliness | A/B/C | |
| Industry-landscape judgment | A/B/C | |
| Management information | A/B/C | |

A = data sufficient and credible; B = some gaps but main conclusion holds; C = many gaps, conclusion needs caution.

### 5.5 Data points pending update

Explicitly list: which data are estimates, which need later verification, which quarter's earnings to track closely.

### 5.6 Source list

The source link for each data point/conclusion, listed by category (filings, sell-side reports, news, industry reports).

---

## AI Research Bias Awareness (important)

Pitfalls AI easily steps into during funnel screening:

| Bias | Manifestation | Countermeasure |
|------|-----|------|
| Large-cap bias | Large caps have more material, longer analysis, look "better" | Score by hard metrics and moat, not by report length |
| English-language bias | US material is abundant, A-shares/HK easily undervalued | Must search in both Chinese and English, don't miss A/H names |
| Story bias | High gain + media buzz = look-better "AI concept stocks" | Distinguish "AI revenue share" vs "AI story share", look at the real business |
| Recency bias | Companies with good current financials easily get in, may miss turnaround dark horses | Layer-2 rough screen allows "improving trend" as a relaxation |
| Listing bias | Looking only at listed companies may miss the best players in the track | Must list "future IPO candidates", note valuation and time window |

---

## Output Requirements

1. **Report location**: `reports/{industry_name}-funnel-{YYYYMMDD}.md` (industry reports go in the reports/ root)
2. **Language**: Chinese
3. **Style**: direct, sharp, no fluff
4. **Data**: cite the source for all data; mark estimates as "estimate"
5. **No preset stance**: data first → logic → conclusion
6. **Both sides**: attach a counter-argument to every core judgment
7. **Keep elimination records per layer**: even dropped companies keep their name + reason

---

## Data Spot-Check (release gate)

After the report is written, run a data spot-check; only pass it to release:

```bash
# Step 1 — extract the spot-check list (15% random sample)
python3 ~/compound/tools/report_audit.py extract \
  --report <report file path>

# Step 2 — pull each item from a reliable source (see skills/financial-data.md)

# Step 3 — output the pass/reject verdict
python3 ~/compound/tools/report_audit.py verdict \
  --results '<filled-in JSON>' \
  --report <report filename>
```

**[Pass]** all checks pass → report can be released; **[Reject]** any check fails → fix and re-review.

---

## Follow-On Actions

After the funnel yields 3 finalists, you can run separately on each:
- `/investment-team` — full four-master parallel deep research (standalone subdirectory + 5 docs)
- `/investment-checklist` — run the full Buffett pre-buy checklist
- `/management-deep-dive` — in-depth management research

`industry-funnel` is the entry; the follow-on skills are the deep dig.
