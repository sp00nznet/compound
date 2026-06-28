# Supply-Chain Bottleneck Hunter: AI-Driven Arbitrage of Global Supply-Chain Chokepoints

Run a supply-chain bottleneck scan on the $ARGUMENTS super-trend and mine it for arbitrage opportunities.

## Core Idea

Don't ask "what stock does AI recommend?" Ask "if this trend keeps expanding, which link runs short first?"

Traditional research stares at market leaders and well-known tracks. This system flips it around: **start from the physical chokepoints of the supply chain, and find the companies nobody watches — but whose failure would force the entire industry to stop and wait.**

Where the excess return comes from: the first-layer bottlenecks (GPUs, HBM, power) are already fully priced. The real alpha sits in the **second and third layers** — optical modules, lasers, InP substrates, SOI wafers, epitaxy equipment, wafer-level test, IC substrates, specialty glass fiber, and the like.

---

## Step 1: Confirm the Super-Trend

### 1.1 Trend screening criteria

Don't chase hallucinations inside tiny fads. Only pursue super-trends that meet ALL of the following:

| Criterion | Requirement | How to verify |
|------|------|---------|
| Durability | At least 3-5 years of high-certainty growth | Search industry forecasts, capex plans |
| Physicality | Requires real hardware/materials/equipment build-out | Distinguish "software upgrade" from "physical expansion" |
| Scale | Global capex > $50B/year | Search top players' capex guidance |
| Acceleration | Demand growth > supply expansion rate | Compare demand growth rate vs capacity expansion plans |

### 1.2 Current super-trend watchlist

Update on every run. Initial list:

1. **AI infrastructure build-out** — data centers, GPU clusters, networking, power
2. **Energy transition** — nuclear restarts, grid upgrades, storage
3. **Defense modernization** — Western defense-spending upcycle, supply-chain reshoring
4. **Semiconductor re-industrialization** — US/EU/Japan subsidized fabs, equipment/materials bottlenecks
5. **Space economy** — satellite internet, surging launch cadence

If the user specifies a concrete trend (e.g. "AI infrastructure"), focus only on that trend.

### 1.3 Trend-validation output

```
Trend name:
Core driver: (one sentence)
Validation events that have already happened (at least 3):
  1. [date] [event] [source]
  2.
  3.
Capex scale: ~ $XX B/year globally, growing YY%
Supply-demand gap call: demand growth > supply expansion rate? yes/no/unclear
Trend confirmed: ✅ trackable / ❌ insufficient evidence, do not track for now
```

---

## Step 2: Physical Decomposition of the Supply Chain

### 2.1 Layered decomposition framework

**Don't stop at the conceptual level — decompose down to physical entities.**

```
Layer 0 (end product): final product/service
    │
Layer 1 (core components): core hardware the market already watches closely
    │                 ⬆ fully priced, limited alpha
    │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
    │                 ⬇ low attention, alpha concentrated here
    │
Layer 2 (subcomponents/materials): parts and materials supporting the core components
    │
Layer 3 (upstream equipment/feedstock): equipment and raw materials needed to make subcomponents
    │
Layer 4 (infrastructure): power, cooling, land, talent, certification
```

### 2.2 Decomposition template, using AI infrastructure as an example

```
Layer 0: AI model training/inference services
Layer 1: GPU/accelerators, HBM memory, servers, data centers
Layer 2 (key scan zone):
  ├─ Networking: optical modules, optical fiber, switch chips, copper cables
  ├─ Optical comms core: lasers (EML/VCSEL/CW), modulators, photodetectors
  ├─ Semiconductor materials: InP substrates, GaAs substrates, SOI wafers, SiC substrates
  ├─ Advanced packaging: CoWoS substrates, HBM TSV, ABF substrate film
  ├─ PCB/substrates: high-frequency high-speed PCB, IC substrates, specialty glass-fiber cloth
  ├─ Test: wafer-level test (Probe Card), burn-in test, ATE
  ├─ Thermal/cooling: liquid cooling systems, CDU, immersion coolant
  └─ Power connection: busways, UPS, switchgear, transformers
Layer 3:
  ├─ Epitaxy equipment: MOCVD, MBE
  ├─ Litho/etch: special-wavelength lithography, InP etch
  ├─ Raw materials: high-purity metals (indium, gallium, germanium), specialty gases, sputtering targets
  └─ Certification/standards: MSA standards, Telcordia certification
Layer 4:
  ├─ Power: nuclear, gas-fired generation, transmission/transformation
  ├─ Cooling water / thermal infrastructure
  └─ Data-center land / permits
```

### 2.3 Decomposing other trends

Run a similar decomposition for each confirmed super-trend. Use WebSearch for:
- "{trend} supply chain bottleneck 2026"
- "{trend} shortage critical component"
- "{trend} capacity constraint"
- "{trend} sole source supplier"

---

## Step 3: Bottleneck Identification — Finding the "Chokepoint"

### 3.1 Six criteria for judging a bottleneck

For each link in Layers 2-3, evaluate one by one:

| # | Criterion | Question | Score |
|---|------|------|------|
| 1 | **Supply concentration** | Global suppliers ≤ 3? | 🔴 ≤2 / 🟡 3-5 / 🟢 >5 |
| 2 | **Expansion lead time** | How long to add capacity? | 🔴 >2yr / 🟡 1-2yr / 🟢 <1yr |
| 3 | **Substitution difficulty** | Can another tech/material replace it? | 🔴 irreplaceable / 🟡 partly / 🟢 easily |
| 4 | **Capacity utilization** | Current utilization? | 🔴 >90% / 🟡 70-90% / 🟢 <70% |
| 5 | **Demand growth** | Downstream demand growth? | 🔴 >50%/yr / 🟡 20-50% / 🟢 <20% |
| 6 | **Customer qualification cycle** | How long for a new supplier to qualify? | 🔴 >1yr / 🟡 6-12mo / 🟢 <6mo |

**Bottleneck rating:**
- 🔴🔴🔴 ≥4 → **S-class bottleneck** (single point of failure, top priority)
- 🔴🔴 3 → **A-class bottleneck** (severely constrained)
- 🔴 1-2 → **B-class bottleneck** (under pressure but manageable)
- No 🔴 → not a bottleneck, skip

### 3.2 Bottleneck-map output

```
Supply-chain bottleneck map — {trend name}
Updated: YYYY-MM-DD

S-class bottlenecks (single point of failure):
  1. [link name] — [one-line reason] — suppliers: [company list]
  2.

A-class bottlenecks (severely constrained):
  1.
  2.

B-class bottlenecks (under pressure):
  1.
  2.

Recent changes (vs last scan):
  - [added/upgraded/downgraded/cleared] [link name] — [reason]
```

---

## Step 4: Company Screening — From Bottleneck to Target

### 4.1 For each S- and A-class bottleneck, find all related listed companies

How to search:
- WebSearch "{bottleneck link} supplier listed company"
- WebSearch "{bottleneck link} manufacturer stock"
- WebSearch "{bottleneck product} market share company"

### 4.2 First-pass screen (quick filter)

| Criterion | Requirement | Rationale |
|------|------|------|
| Listing status | Listed (A/HK/US/JP/TW/EU) | Tradable |
| Bottleneck revenue share | >30% of revenue from the bottleneck link | Purity |
| Market cap | Prefer < $10B | Large caps already fully priced |
| Liquidity | Avg daily turnover > $1M | Can get in and out |

### 4.2.1 Valuation check (mandatory, cannot be skipped)

**A real bottleneck ≠ an investment opportunity.** You must compute PS and PE for every company and note them in the report. Use the following combined conditions to judge whether the valuation is stretched:

#### Valuation red light (any one met → signal strength capped at ★★, flagged "⚠️ valuation stretched")

1. **Market cap > 20% of TAM**: the company's market cap already exceeds 20% of its addressable market — growth expectations are over-internalized
2. **PS > 30x and revenue growth < 100%**: high valuation but growth too weak to support it. Companies growing >100% are exempt from the PS red line, but still flag "⚠️ high valuation needs sustained high growth to validate"
3. **Market cap > 10x of optimistic 5-year revenue forecast**: even if the most optimistic assumptions all play out, the current price is still too high
4. **Stock doubled within 60 days of a secondary offering**: clear sentiment-driven signature, drop signal strength one notch

#### Valuation yellow light (needs extra explanation, otherwise downgrade)

1. **Loss-making + PS > 15x**: allowed up to ★★★ but must lay out the path and timeline to profitability
2. **PS more than 5x that of profitable peers**: must explain the premium (market share, growth gap, moat difference)
3. **PE > 80x**: compute PEG and explain whether growth supports it

#### Valuation green light (bonus)

- PS < 10x and revenue growing → signal strength may go up one notch
- PE < 30x with a moat → flag "valuation has a margin of safety"

#### Valuation sanity check (mandatory)

For each target, answer: "Buying at today's market cap, assuming the most optimistic scenario fully plays out, exiting at 25x PE in 10 years, what's the annualized return?" If annualized return <10% → flag "current price offers no margin of safety".

**Note**: the point of the valuation check is to prevent obvious mistakes like recommending "a loss-making company at 100x PS", not to exclude every high-valuation early-stage company. The key is whether growth, TAM, and competitive structure can support the current valuation — this requires specific analysis, not a blanket rule.

### 4.3 Deep-screen dimensions

For companies that pass the first-pass screen, evaluate one by one:

```
## {company_name} ({ticker})

**Bottleneck positioning**:
- Specific position in the supply chain
- Market share: #X globally, XX%
- Customer list (those known)

**Capacity and expansion**:
- Current capacity / utilization
- Expansion plan / timeline
- Capital needed for expansion vs cash on hand

**Financial snapshot**:
- Market cap / revenue / profit / growth
- Bottleneck-business revenue share
- Gross-margin trend (the tighter the bottleneck, the more margin should rise)

**Risk checklist**:
- [ ] Substitute-technology risk: can it be bypassed?
- [ ] Dilution risk: heavy secondary offerings / convertibles?
- [ ] Geopolitical risk: located in a sensitive region / subject to export controls?
- [ ] Management risk: any bad track record?
- [ ] Customer-concentration risk: over-reliant on a single customer?
- [ ] Valuation stretched: does the current valuation already price in 3 years of growth?

**Bottleneck durability call**:
- When will this bottleneck be cleared?
- After it clears, what does this company have left?
- Is it one-off or recurring?
```

---

## Step 5: Cross-Validation — Don't Listen to Just One Story

### 5.1 Positive validation

| Item | Question | How to search |
|--------|------|---------|
| Customer validation | Have top customers signed/designed in? | Search company filings, customer earnings mentions |
| Revenue validation | Is the bottleneck already showing up in revenue growth? | Search the last 2-3 quarters of earnings |
| Price validation | Are product prices rising? | Search industry pricing, analyst reports |
| Capacity validation | Is capacity really tight? | Search lead-time data, customer complaints |
| Capital validation | Is there expansion capex? | Search company capex guidance |

### 5.2 Negative validation (Munger-style inversion)

| Inversion question | Significance |
|---------|------|
| Why won't smart people buy this stock? | Find the known bearish thesis |
| Can this bottleneck be bypassed? Any alternative path? | Technology-path risk |
| Can China / other players replicate the capacity quickly? | Supply-shock risk |
| If end demand slows 50%, what happens to this company? | Downside sensitivity |
| Has management diluted shareholders at the top before? | Management trustworthiness |
| What growth assumptions does the current valuation imply? | Valuation reasonableness |

### 5.3 Signal cross-validation

- Are multiple companies on the same bottleneck all rising? (industry validation)
- Are downstream customers mentioning tight supply in their earnings? (customer validation)
- Do industry associations / research firms have corroborating data? (third-party validation)

---

## Step 6: Output — Bottleneck Opportunity Board

### 6.1 Bottleneck opportunity ranking table

| Rank | Company | Ticker | Mkt cap | Annual rev | PS | PE | Bottleneck link | Rating | Mkt share | Rev growth | Signal | Valuation call |
|------|------|------|------|--------|-----|-----|---------|---------|---------|---------|---------|---------|
| 1 | | | | | x | x | | S/A | | | ★1-5 | fair/high/stretched |

**Mandatory fields**: market cap, annual revenue, PS, PE are required — cannot be skipped with "to be confirmed". If financial data cannot be obtained, signal strength may not exceed ★★.

Signal-strength rating (the valuation check directly affects the rating):
- ★★★★★ multiple cross-validations, customer designed in, revenue already showing, valuation green (reasonable PS + profitable or near-profitable)
- ★★★★ most validations pass, valuation green or yellow (with explanation)
- ★★★ logic holds but parts unvalidated, valuation yellow acceptable (e.g. high-growth early-stage company)
- ★★ early signal, or bottleneck logic holds but valuation red (mkt cap >20% TAM, PS>30x with weak growth, mkt cap far above 5-year forecast, etc.)
- ★ pure concept, unvalidated

### 6.2 One-pager per opportunity

```
🎯 {company_name} ({ticker}) — {one-line bottleneck positioning}

Why it's a bottleneck:
(2-3 sentences on why this link is a chokepoint)

Why this company:
(2-3 sentences on why this one and not another)

Catalyst timeline:
- Near term (1-3 mo): [specific events, e.g. earnings, capacity ramp, customer qualification]
- Medium term (3-12 mo): [industry trends, expansion milestones]

Key risks:
1.
2.

Key data: mkt cap $XX / annual rev $XX / PS Xx / PE Xx / rev growth XX% / bottleneck-business share XX%

Margin-of-safety check: buying at today's market cap, exiting at 25x PE in 10 years, requires net profit of $XX, implying annual revenue of $XX (X times today's), annualized return XX%. Verdict: has / lacks margin of safety.

Cross-validation status: ✅ customer / ✅ revenue / ✅ valuation reasonable / ⚠️ valuation stretched / ❌ unvalidated items

Conclusion: worth deep research / add to watchlist / do not track
```

### 6.3 Action recommendations

| Target | Recommended action | Rationale |
|------|---------|------|
| A | Run `/investment-team` for deep research | S-class bottleneck + multiple validations |
| B | Add to watchlist, wait for next earnings | Logic holds but revenue not yet showing |
| C | Do not track | Substitute-technology risk too high |

---

## Step 7: Maintenance — Keeping the Bottleneck Map Live

### 7.1 Incremental update on each run

1. Check whether identified bottlenecks still hold
   - Any new supplier entering?
   - Has capacity expanded enough to clear the bottleneck?
   - Any breakthrough in substitute technology?

2. Scan for newly emerging bottlenecks
   - Search the last 7 days of supply chain / shortage / bottleneck news
   - Check supply-chain-related disclosures during earnings season

3. Update bottleneck ratings (upgrade/downgrade/clear)

### 7.2 State files

Maintain under the `reports/bottleneck-map/` directory:
- `master-map.md` — master bottleneck map (continuously updated)
- `watchlist.md` — watchlist (continuously updated)
- `YYYY-MM-DD/` — one folder per day, holding all scan reports for that day
- `deep-dive/` — separate file per company under deep analysis

---

## Hourly Scan Mode (for scheduled tasks)

Runs once per hour, in a "only report when there's something" mode:

### Scan flow (hourly)

1. **News scan**: search supply-chain-related news from the past 1-2 hours
   - Keywords: supply chain bottleneck, shortage, capacity constraint, allocation, lead time, sole source, 瓶颈, 缺货, 产能, 涨价
   - Coverage: English + Chinese sources
2. **Market signals**: check stock-price moves of tracked companies (watch especially for abnormal swings >5%)
3. **Earnings/filings**: check whether any bottleneck-related company released earnings or a major filing
4. **Valuation opportunities**: check whether any watchlist company has entered a buy zone due to a market sell-off, etc.
5. **Decide whether to report**:
   - New bottleneck signal, a clear target opportunity, or a major status change → **report**
   - Nothing new → **don't report**, just log "no new signal this round"

### Report output rules

**One folder per day**: `reports/bottleneck-map/YYYY-MM-DD/`

**File-naming rule** (so you can tell at a glance whether there's a target from the filename):

| Situation | Filename format | Example |
|------|-----------|------|
| Clear target found | `HH-MM-ticker1-ticker2.md` | `09-00-FORM-IBDN.md` |
| Bottleneck signal but no clear target | `HH-MM-signal-scan.md` | `14-00-signal-scan.md` |
| Nothing new | no file generated | — |

**The tickers in the filename = companies that pass the valuation check and are worth deep research.** Companies that surface only in the signal-scan phase but fail the valuation check do not go in the filename.

### Report template (when there's a target)

```markdown
# Bottleneck Hunter — YYYY-MM-DD HH:MM

## Clear targets

### {company_name} ({ticker}) — {one-line bottleneck positioning}

**Why it's worth attention now**: (the specific event/data change that triggered this attention)

**Bottleneck positioning**: Layer X, {link name}, rating S/A/B
**Financial snapshot**: mkt cap $XX / annual rev $XX / PS Xx / PE Xx / rev growth XX%
**Valuation check**: red/yellow/green (with specifics)
**Margin of safety**: 10-year 25x-PE exit method, annualized return XX%

**Bull case** (2-3 points):
1.
2.

**Bear case** (2-3 points):
1.
2.

**Recommendation**: run deep research / add to watchlist / wait for a better price

---

## Other signals (no clear target)

| Link | Signal | Source | Preliminary call |
|------|------|------|---------|

## Watchlist status changes

(upgrade/downgrade/added/removed; if none, write "no change")
```

### Report template (signal scan only)

```markdown
# Bottleneck Hunter Signal Scan — YYYY-MM-DD HH:MM

## New signals

| Link | Signal description | Source | Investable target? | Next step |
|------|---------|------|----------------|-------|

## Watchlist status

No change / changed (list them)
```

---

## AI Research Bias Awareness

| Bias | Manifestation | Countermeasure |
|------|-----|------|
| Large-cap bias | Search results dominated by large-cap companies | Deliberately search small-cap suppliers, add "small cap" keyword |
| English-language bias | Missing Japanese/Korean/Taiwanese companies | Must search suppliers in JP/KR/TW markets |
| Narrative bias | Drawn to the "AI concept" label | Look only at actual supply-chain position, not market labels |
| Confirmation bias | Once a bottleneck is found, only look for confirming evidence | Force negative validation (Step 5) |
| Recency bias | Relying on stale information | Prioritize data from the last 30 days |

---

## Core Principles (highest priority)

1. **Don't let AI recommend stocks — let AI decompose the supply chain** — the question matters more than the answer
2. **Physical first** — only care about links that require real physical products/materials/equipment
3. **Second and third layers** — don't chase fully-priced leaders
4. **Cross-validate** — every conclusion backed by at least 2 independent sources
5. **Be honest about uncertainty** — if you can't find data, write "insufficient data", don't fill it with speculation
6. **Bottlenecks are time-bound** — every bottleneck eventually clears; the key is judging the time window
7. **Small cap ≠ good opportunity** — a small cap can also be a bad company; it must clear the financial-quality bar
8. **A real bottleneck ≠ an investment opportunity** — a company can sit on the tightest bottleneck, but if PS>30x or it's still losing money, the current price is not a buy point. **Valuation is a hard gate; it cannot be overridden by bottleneck purity, signal strength, or narrative appeal.** Better to miss a bottleneck stock that ran than to buy a loss-making company at 100x PS
9. **Follow the objectivity principle in CLAUDE.md** — no preset bull bias; data first, conclusion second

---

## Output Requirements

1. **Report location**:
   - Full scan: `reports/bottleneck-map/{trend name}-bottleneck-{YYYYMMDD}.md`
   - Daily scan: `reports/bottleneck-map/daily/{YYYY-MM-DD}-{am/pm}.md`
   - Master bottleneck map: `reports/bottleneck-map/master-map.md`
   - Watchlist: `reports/bottleneck-map/watchlist.md`
2. **Language**: Chinese
3. **Style**: direct, sharp, no fluff
4. **Data**: cite the source for all data; mark estimates as "estimate"
5. **No preset stance**: data first → logic → conclusion
6. **Both sides**: attach a counter-argument to every core judgment
