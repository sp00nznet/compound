# Earnings Close-Reading Team: Four Masters Analyze in Parallel + Publication

Run a team-based close-reading earnings analysis on $ARGUMENTS. Four masters read the earnings in parallel, an editor polishes it into an article, a reader-reviewer guards quality, and the final output is a ready-to-publish official-account article.

**Supported input format**: `company quarter`, e.g. `腾讯 2025Q4`, `PDD 2025年报`, `美团 最新`.

## Design Philosophy

A good earnings analysis must solve two problems:
1. **You yourself can see the future** — needs deep research from four different perspectives
2. **The reader can see the value** — needs editorial polish and a reader's-eye quality check

This skill's flow has three phases:
- **Phase 1 · Research**: four masters read the earnings in parallel (Duan Yongping reads the business essence, Buffett audits financial quality, Munger reads competitive change, Li Lu hunts risk signals)
- **Phase 2 · Synthesis**: the Team Lead synthesizes the four perspectives into a research-report draft
- **Phase 3 · Publication**: an editor agent rewrites it into an official-account article + a reader-reviewer agent proposes edits → Team Lead finalizes

---

## Phase 1: Four Masters Research in Parallel

### Step 1: Obtain primary sources

Use the Agent tool to launch background agents to fetch the following raw materials **in parallel**:

| Material type | Source | Priority |
|---------|---------|--------|
| Original filing | Company IR page, SEC EDGAR (US), HKEX Disclosure (HK), cninfo (A-shares) | Highest |
| Earnings-call transcript | Seeking Alpha, company IR page, Xueqiu | Highest |
| Letter to shareholders | Extracted from the annual report | High (annual reports only) |
| Prior-period earnings/call | Same as above | High (for promise tracking) |

**Source-availability grade**:

| Grade | Trait | Impact |
|------|------|------|
| Grade A | Obtained the full original text | Run all steps normally |
| Grade B | Only partial original text or third-party summaries | Flag "non-primary source", lower the weight of footnote analysis |
| Grade C | Only news coverage and data-site summaries | Focus on core data changes, skip footnote mining, flag "insufficient primary sources" |

Tell each agent the source-availability grade — it affects analysis depth.

### Step 2: Show the user the team framework

| Phase | Role | Master/positioning | Core task |
|------|------|----------|---------|
| Research | **Team Lead** (you) | Overall coordination | Coordinate, synthesize, finalize |
| Research | Business-essence reader | Duan Yongping | Did the business get better or worse? |
| Research | Financial-quality auditor | Buffett | Is the money real or fake? |
| Research | Competitive-change reader | Munger | How is the competitive landscape shifting? |
| Research | Risk-signal hunter | Li Lu | What is management hiding? |
| Publication | Editor | Official-account writing | Rewrite the research report into a good article |
| Publication | Reader-reviewer | Ordinary investor | Can the reader follow it? Do they get something? |

### Step 3: Launch 4 parallel research agents

Use the Agent tool to launch 4 background agents **in the same message**.

---

#### Agent 1: Business-Essence Reading (Duan Yongping's view)

**Core question: does the business essence reflected in this report get better or worse?**

> Duan Yongping: "Investing is buying a business. Reading earnings isn't reading numbers, it's seeing whether the business changed."

What to analyze:

1. **Revenue-structure breakdown and interpretation**
   - Revenue by business/region — which are accelerating, which decelerating
   - Don't just list numbers — what business logic does each segment reflect
   - Does revenue growth come from "volume" or "price"? Which is healthier?

2. **Change in user/customer value**
   - Operating metrics like DAU/MAU/paying users
   - Quality metrics like time spent, ARPU, retention
   - Is the platform/product's value to users strengthening or weakening?

3. **Moat check**
   - Gross-margin change reflects whether pricing power is solid
   - Market-share change reflects whether the competitive barrier is effective
   - Any sign that switching costs / network effects are being eroded

4. **"Good business" criteria assessment**
   - Duan Yongping's three conditions: differentiation, pricing power, sustainable competitive advantage — this period's change
   - Is the business getting "heavier" or "lighter"?
   - If the company shut down tomorrow, would users be in real pain? Did this report change that?

5. **Management's product instinct**
   - When discussing product/users, does management use concrete language or bureaucratic language
   - Any impressive product insight or worrying signs of disconnect

**Output requirement**: flag each sub-item 🟢 improving / 🟡 flat / 🔴 deteriorating, and give a Duan-Yongping-style summary.

---

#### Agent 2: Financial-Quality Audit (Buffett's view)

**Core question: is the money this company earns real or fake? Did the margin of safety change?**

> Buffett: "The first thing I do with every filing is turn to the cash-flow statement."

What to analyze:

1. **Extract and verify core financial data**
   - Revenue, gross profit, operating profit, net profit — both GAAP and Non-GAAP
   - GAAP vs Non-GAAP gap: how big, where, widening or narrowing
   - Cross-validate key data from at least two sources

   ```bash
   python3 ~/compound/tools/financial_rigor.py cross-validate \
     --metric "revenue" --values {value1} {value2} --sources "{source1}" "{source2}"
   ```

2. **Cash-flow analysis (most important)**
   - Operating cash flow vs net profit ratio (>100% good, <80% caution)
   - Free cash flow = operating cash flow − capex
   - Capex composition: maintenance vs expansion
   - Buyback and dividend amounts

3. **Profit-quality check**
   - Receivables growth vs revenue growth
   - Inventory growth vs revenue growth
   - Trend in the gap between operating cash flow and net profit
   - Did capitalized spending suddenly rise
   - Non-recurring gains' share

4. **Balance-sheet health**
   - Net-cash / net-debt change
   - Days receivable / days inventory change
   - Goodwill and intangibles impairment risk

5. **Valuation and margin-of-safety update**

   ```bash
   python3 ~/compound/tools/financial_rigor.py verify-market-cap \
     --price {price} --shares {shares} --reported {reported_mcap} --currency {currency}
   python3 ~/compound/tools/financial_rigor.py verify-valuation \
     --price {price} --eps {EPS} --bvps {bvps}
   python3 ~/compound/tools/financial_rigor.py three-scenario \
     --price {price} --eps {EPS} --shares {shares_100m} \
     --growth {optimistic} {neutral} {pessimistic} --pe {optimistic_pe} {neutral_pe} {pessimistic_pe}
   ```

**Output requirement**: attach the tool output for all calculations, profit-quality traffic lights 🟢/🟡/🔴, and a Buffett-style summary.

---

#### Agent 3: Competitive-Landscape Reading (Munger's view)

**Core question: what change in the competitive landscape does this report reveal?**

> Munger: "I want to know where I'm going to die, so I never go there."

What to analyze:

1. **Infer competitive change from the financials**
   - Revenue growth vs industry growth — outperforming or underperforming?
   - Gross-margin change reflects intensifying / easing competition
   - Marketing-expense ratio change — does it cost more to acquire customers?
   - R&D spending — proactive investment or forced to follow?

2. **Compare against competitors in the same period**
   - Same-period key metrics of major competitors (if released)
   - Compare growth, margins, intensity of investment
   - Who's winning? Who's losing?

3. **Management's discussion of competition**
   - How they describe the competitive environment on the call
   - Do they name competitors? Confident tone or anxious?
   - Any new competitive threat?

4. **Industry-trend signals**
   - Impact of technological change (AI / new platforms, etc.)
   - Impact of regulatory change on the competitive landscape
   - Consumption / demand-side trends

5. **Munger-style inversion**
   - What would kill this company? Does this report point to any of those threats?
   - Looking back in 5 years, will this report be an "inflection point"?

**Output requirement**: competitive-landscape call (strengthened/flat/deteriorating), competitor comparison table, Munger-style inversion commentary.

---

#### Agent 4: Risk-Signal Hunter (Li Lu's view)

**Core question: what is management hiding in this report? Which signals are flashing?**

> Li Lu: "The most important thing in investing is to avoid permanent loss of capital."

What to analyze:

1. **Management-tone analysis**
   - Read the management discussion and call remarks paragraph by paragraph, flagging signals:
   - 🟢 candor signal (proactively admits problems) / 🟢 clarity signal (quantified targets)
   - 🔴 vagueness signal (empty words) / 🔴 deflection signal (non-answers) / 🔴 externalizing blame

2. **Promise tracking**
   - Prior-period specific promises vs this-period actual delivery, item by item
   - Duan Yongping: "To tell whether management is reliable, check whether they did what they said before."

3. **Footnotes and hidden information**
   - Related-party transactions, SBC dilution, contingent liabilities
   - Accounting-policy changes, segment-margin differences
   - Customer/supplier concentration change

4. **Selected call Q&A**
   - The 3-5 sharpest analyst questions and a quality score of management's answers

5. **Permanent-capital-loss risk**
   - Any signal that could lead to permanent loss
   - New developments in regulatory/compliance/litigation risk
   - Did management make any irreversible wrong decision

**Output requirement**: management-credibility score ★1-5, promise-delivery rate, risk-signal list, Li-Lu-style summary.

---

### Step 4: Track progress

Show the user in real time:

```
📊 {company_name} {period} earnings close-reading progress
━━━━━━━━━━━━━━━━━━━━━━━
Phase 1 · Research
  ☐ Duan Yongping · business essence    ⏳ analyzing...
  ☐ Buffett · financial quality         ⏳ analyzing...
  ☐ Munger · competitive landscape      ⏳ analyzing...
  ☐ Li Lu · risk signals                ⏳ analyzing...
Phase 2 · Synthesis                      ⏸ waiting
Phase 3 · Publication                    ⏸ waiting
```

As each report arrives, update progress and show the core findings (3-5 points).

---

## Phase 2: Team Lead Synthesizes the Research Report

Once all 4 research reports are in, the Team Lead synthesizes them into a research-report draft.

**Synthesis priorities** — not stapling reports together, but finding intersections and contradictions:

1. **Points of consensus across the four**: conclusions all four masters agree on — highest confidence
2. **Points of contradiction across the four**: e.g. Duan Yongping says the business improved, but Munger says competition is deteriorating — this kind of contradiction is the most valuable analysis
3. **Overlooked corners**: what none of the four emphasized — could that be precisely the most important thing?

#### Research-report structure

```markdown
# {company_name} {period} Earnings Close-Reading Report
**Four masters read in parallel | {date}**

## 1. One-sentence conclusion
> 50-100 chars: beat/in line/miss, the core change, the impact on the investment thesis.

## 2. The 3 most important changes this period
Focus on the truly important changes, don't list data; each change under 100 chars.

## 3. Four-master scorecard
| Perspective | Master | Core question | Conclusion | Score | vs prior |
|------|------|---------|------|------|--------|

## 4. Core data snapshot
Table of key financial and operating metrics (this period vs prior period vs YoY)

## 5. Deep analysis per perspective
3-5 most important findings per perspective

## 6. Management tone and promise tracking
Promise-delivery table + tone-change analysis

## 7. What would the four masters do?
| Master | If holding | If not holding | Rationale |

## 8. Conclusion
1. Beat/in line/miss?
2. Thesis impact: strengthened/no impact/weakened/broken
3. Next catalyst
4. Action recommendation
```

---

## Phase 3: Editorial Polish + Reader Review

After the research report is done, launch two agents **in parallel**:

### Agent 5: Editor (rewrite into an official-account article)

**Positioning**: rewrite the hardcore research report into an article that official-account readers love and can understand.

**Core principles**:
- Keep all key data and conclusions, don't lower the professional depth
- Improve the delivery so non-professional investors can follow the logic
- Not "dumbing down", but "making professional content read effortlessly"

**Concrete tasks**:

1. **Title and opening**
   - The title should be informative and clickable, but not clickbait
   - Good title example: "Kuaishou bet ¥26B on AI — did the bet pay off?"
   - Bad title example: "Shocking! Kuaishou earnings blow up!"
   - Within the first 100 chars, make clear: what the most important conclusion of this report is, and why the reader should care

2. **Structure optimization**
   - The research report is for yourself; the official-account article is for others — adjust the logical order
   - Put "the 3 most important changes" up front (inverted-pyramid structure)
   - Keep tables but trim them; turn long analysis into bullet points
   - Insert a "mini-recap" roughly every 500 chars to help the reader digest

3. **Polishing the delivery**
   - Explain stiff financial jargon with analogies/scenarios: "operating cash flow is 30% below net profit" → "earned ¥100 but only ¥70 actually reached the pocket"
   - The four masters' commentary quotes are the soul of the article — make sure each reads sharp and memorable
   - Paragraphs no longer than 4 lines, sentences no longer than 30 chars
   - Use contrast moderately to create reading rhythm

4. **Reader-value check**
   - For each section, ask: after reading this, what decision can the reader make? If the answer is "nothing", rewrite or delete it
   - The article must end with a clear "so what?" — give action guidance separately for holders and watchers

5. **Format adaptation**
   - WeChat-official-account-friendly layout: short paragraphs, clear subheads, concise tables
   - Add appropriate dividers and blockquotes
   - Keep article length to 1,000-3,000 chars (too long and readers bounce)

**Output**: the full rewritten official-account article.

---

### Agent 6: Reader Review (ordinary-investor view)

**Positioning**: read the article as an "ordinary investor who follows value investing, has basic financial knowledge, and holds/follows this company".

**Review dimensions**:

1. **Readability (weight 30%)**
   - How many minutes to read the whole thing? Any paragraphs you want to skip?
   - Where is it hard to understand or needs rereading?
   - How's the rhythm? Any "I'm tired of reading" feeling?

2. **Information value (weight 30%)**
   - After reading, is my understanding of this company deeper?
   - Any "oh, so that's how it is" moments?
   - Compared with analysis I've seen elsewhere, what's unique here?
   - Which info is redundant, removable without losing comprehension?

3. **Credibility (weight 20%)**
   - Is the data sourced? Are key judgments backed?
   - Does it present both sides, or only sing bull/bear?
   - Any "this is way too confident" judgments that feel uncomfortable?
   - Are the four masters' quotes apt and forceful?

4. **Actionability (weight 20%)**
   - After reading, do I know what to do?
   - Are the recommendations for "holders" and "watchers" specific enough?
   - What to watch next? (catalysts, timing)

**Output format**:

```markdown
## Reader Review Report

### Overall score: X/10

### Strengths (2-3)
What the article does well from a reader's view

### Must fix (hard problems)
- Problem 1: specific description → suggested fix
- Problem 2: ...

### Suggested improvements (nice-to-have)
- Suggestion 1: ...
- Suggestion 2: ...

### Questions the reader most wants answered but the article didn't
- Question 1
- Question 2

### One-line verdict
```

---

### Team Lead Finalizes

After receiving the editor's rewrite and the reader review:

1. **Address the review's "must fix" items** — one by one
2. **Selectively adopt the "suggested improvements"** — judge whether worth it
3. **Add the "questions the reader wanted but weren't answered"** — if there's data to support, add them
4. **Final read-through** — ensure the revised article is coherent and internally consistent

---

## Output Files

```
reports/{company_name}/
├── {company_name}-earnings-{period}.md           ← final official-account article (finalized)
├── {company_name}-earnings-{period}-research-draft.md   ← four-master synthesized research report (internal)
├── {company_name}-earnings-{period}-duan-yongping.md    ← business-essence reading
├── {company_name}-earnings-{period}-buffett.md          ← financial-quality audit
├── {company_name}-earnings-{period}-munger.md           ← competitive-landscape reading
├── {company_name}-earnings-{period}-li-lu.md            ← risk-signal analysis
└── {company_name}-earnings-{period}-reader-review.md    ← reader review report
```

## Data Spot-Check (release gate)

Run a spot-check on the final article:

```bash
python3 ~/compound/tools/report_audit.py extract \
  --report reports/{company_name}/{company_name}-earnings-{period}.md

python3 ~/compound/tools/report_audit.py verdict \
  --results '<filled-in JSON>' \
  --report {report filename}
```

**[Pass]** all checks pass → ready to release; **[Reject]** any check fails → fix and re-review.

## Relationship to Existing Skills

| Skill | Positioning | When to use |
|-------|------|------|
| `/earnings-review` | Single-agent close reading | Quick pass, one perspective is enough |
| **`/earnings-team` (this skill)** | **Six-agent team close reading + publication** | **A key earnings report for an important company, needs depth + publication** |
| `/investment-team` | Four-agent full company research | First-time research on a company |

## Key Principles

- **Read the original, not the summary**: do everything possible to get primary sources
- **Four perspectives are not four departments**: they must corroborate and challenge each other, not talk past each other
- **The Team Lead's value is integrated judgment**: find intersections and contradictions, not staple reports together
- **The conclusion must be clear**: no "overall broadly in line with expectations but with some points worth watching"
- **Counter-checking runs throughout**: every positive finding carries a counter-argument
- **The editor isn't lowering rigor**: making professional content more readable, not turning it into pop science
- **Reader review isn't a rubber stamp**: genuinely pick at flaws from the reader's view
- **Data accuracy**: cross-validate key data, verify with the financial_rigor.py tool
