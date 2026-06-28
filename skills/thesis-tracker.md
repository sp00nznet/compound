# Investment Thesis Tracker: The Post-Buy Discipline System

Run an investment thesis tracking check on $ARGUMENTS.

**Supported input formats**:
- `company_name` — first use builds the investment thesis; later uses run a tracking check
- `company_name build thesis` — force-rebuild the investment thesis
- `company_name quarterly check` — run a thesis check against the latest earnings

> "Buying is just the beginning. The real work is the continuous tracking you do while you hold." —— Li Lu
>
> "When the facts change, I change my mind. What do you do?" —— Keynes

## Design Philosophy

Most investors' process is: research → buy → pray. The missing piece is systematic post-buy tracking, which leads to:
- Refusing to sell when you should ("just wait a bit, it'll come back")
- Panic-selling when you shouldn't ("it's down 20%, was I wrong?")
- Forgetting why you bought in the first place ("now why did I buy this again?")

What Buffett and Li Lu do: **write down your sell conditions before you buy.** Then check every quarter whether the thesis still holds.

## Execution Flow

### Step 1: Determine the operating mode

Check whether an investment thesis file already exists for the company (`reports/{company_name}-thesis.md`):
- If it doesn't exist → enter **build thesis** mode
- If it exists → enter **tracking check** mode
- If you can't find it but the user says one exists → ask for the file path

---

## Mode A: Build the Investment Thesis

### A0: Data Collection

Use WebSearch to get the current share price, valuation metrics (PE/PB/dividend yield), and core figures from the latest earnings, to fill in the valuation anchors. If a `/investment-research` or `/investment-team` report already exists for the company, read from it first.

Use `tools/financial_rigor.py verify-valuation` to validate the valuation data.

### A1: Core Thesis (must be stated clearly in 200 characters or fewer)

The investment thesis must answer the following 5 questions, one sentence each:

```
I buy ___company at ___, because:
1. The essence of this business is ___, and I understand how it makes money
2. Its moat is ___, and it is widening / stable
3. Management is ___, and the reason to trust them is ___
4. The current price is a ___ discount to intrinsic value; the margin of safety comes from ___
5. Even if I'm wrong, downside is contained, because ___
```

**If you can't complete all 5 sentences, the thesis itself is flawed — it means the buy decision isn't clear enough.**

### A2: Core Assumptions List

Break the thesis down into specific, verifiable assumptions:

| # | Core Assumption | How to Verify | Frequency | Current Status |
|---|---------|---------|---------|---------|
| 1 | e.g. revenue growth holds at 15%+ | quarterly revenue growth | every quarter | 🟢 holds |
| 2 | e.g. gross margin stable at 60%+ | quarterly gross margin | every quarter | 🟢 holds |
| 3 | e.g. management keeps buying back stock | buyback announcements / cash flow statement | every quarter | 🟢 holds |
| 4 | e.g. competitors make no breakthrough | industry data / competitor earnings | every six months | 🟢 holds |
| 5 | ... | ... | ... | ... |

Usually 3-7 assumptions. Too few means the thinking isn't deep enough; too many means the thesis isn't focused enough.

### A3: Red Lines (tripping any one = mandatory re-evaluation)

| # | Red Line Condition | Severity | Action When Triggered |
|---|---------|---------|-----------|
| 1 | e.g. management integrity breaks down (accounting fraud, related-party deals) | fatal | liquidate immediately |
| 2 | e.g. core business revenue declines for 2 consecutive quarters | severe | cut position 50%, re-evaluate |
| 3 | e.g. moat clearly breached (competitor achieves parity) | severe | launch deep research, consider exit |
| 4 | e.g. regulation fundamentally changes the business model | severe | re-estimate intrinsic value |
| 5 | e.g. large-scale management selling (unplanned) | warning | investigate the reason thoroughly |

**Duan Yongping**: "There are only three reasons to sell: 1. you realize you bought wrong; 2. the company's fundamentals changed; 3. you found something better."

### A4: Valuation Anchors

| Metric | At Purchase | Bullish Target | Base Case | Bearish Scenario |
|------|-------|---------|---------|---------|
| Share price | | | | |
| PE | | | | |
| Market cap | | | | |
| Intrinsic value estimate | | | | |
| Margin of safety | | | | |

### A5: Save the Thesis

Write the investment thesis to `reports/{company_name}-thesis.md`, including:
- Date created
- Purchase price and position size
- Core thesis (5 sentences)
- Core assumptions list
- Red lines list
- Valuation anchors
- Tracking log table (initially empty)

---

## Mode B: Tracking Check

### B1: Read the Existing Thesis

Read `reports/{company_name}-thesis.md` and load:
- Core thesis
- Core assumptions list
- Red lines list
- Last check's record

### B2: Collect the Latest Data

Use WebSearch to collect:
1. Latest earnings data (if there's a new quarterly/annual report)
2. Recent major events (management changes, regulatory policy, competitive dynamics)
3. Current share price and valuation metrics
4. Insider transaction records (major shareholders buying/selling)

### B3: Check Each Core Assumption

For each core assumption, validate against the latest data:

| # | Core Assumption | Last Status | Latest Evidence | Current Status | Change |
|---|---------|---------|---------|---------|------|
| 1 | revenue growth 15%+ | 🟢 holds | Q4 revenue growth 12% | 🟡 weakening at the margin | ⚠️ |
| 2 | gross margin 60%+ | 🟢 holds | gross margin 61.2% | 🟢 holds | — |
| 3 | ... | ... | ... | ... | ... |

Status definitions:
- 🟢 **holds** — latest data supports the assumption
- 🟡 **weakening at the margin** — data is still within acceptable range, but the trend is unfavorable
- 🔴 **impaired** — data clearly does not support the assumption
- ⚫ **broken** — the assumption has been overturned

### B4: Red Line Check

Check each red line in turn:

| # | Red Line Condition | Triggered? | Evidence |
|---|---------|:-------:|------|
| 1 | management integrity issue | ❌ not triggered | — |
| 2 | core business down 2 quarters in a row | ❌ not triggered | — |

**If any red line is triggered → flag it prominently in the report and give a clear action recommendation.**

### B5: Valuation Update

| Metric | At Purchase | Last Check | Current | Change |
|------|-------|---------|------|------|
| Share price | | | | |
| PE (TTM) | | | | |
| Intrinsic value estimate | | | | |
| Margin of safety | | | | |

### B6: Output the Tracking Report

#### Report Structure

```
1. Thesis health score (out of 10)
2. Core assumptions check results (table)
3. Red line check results (table)
4. Key changes this period (under 500 characters)
5. Valuation update
6. Conclusion and action recommendation
7. Key items to watch at the next check
```

#### Thesis Health Scoring Standard

| Score | Meaning | Recommended Action |
|:----:|------|---------|
**Formula**: health = 10 - (⚫ broken assumptions ×3) - (🔴 impaired assumptions ×2) - (🟡 weakening assumptions ×1) - (red lines triggered ×5), floored at 1 and capped at 10.

| Score | Meaning | Recommended Action |
|:----:|------|---------|
| 9-10 | all assumptions hold, thesis is stronger than at purchase | consider adding |
| 7-8 | core assumptions hold, a few weakening at the margin | keep holding |
| 5-6 | 1-2 assumptions impaired, but core logic intact | hold but raise vigilance |
| 3-4 | multiple assumptions impaired, thesis foundation shaky | consider trimming |
| 1-2 | red line triggered or core assumption broken | strongly recommend selling |

#### The Conclusion Must Clearly Answer

1. **Is the thesis still intact?** intact / weakening at the margin / impaired / broken
2. **What to do?** add / hold / trim / liquidate
3. **Next check date**: after the next earnings release / after a specific event

### B7: Update the Thesis File

Append this check's record to the tracking log table in `reports/{company_name}-thesis.md`:

| Check Date | Health | Key Change | Action Recommendation |
|---------|:------:|---------|---------|
| 2026-04-09 | 7/10 | revenue growth slowed to 12%, but margins improved | hold |

---

## Key Principles

- **Write the sell conditions before you buy** — decisions made when calm beat decisions made in panic
- **The thesis must be specific enough to verify** — "great company" is not a thesis; "ROE >25% with a stable trend" is
- **Act the moment a red line is triggered** — the deadliest instinct is "let's wait and see"; that's where big losses begin
- **Thesis broken ≠ price down** — a 30% price drop doesn't necessarily mean sell; a broken thesis does
- **Be honest about mistakes** — if the thesis was built wrong, admit it; don't tough it out to save face
