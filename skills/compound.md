# /compound — One-command portfolio research

Give me your holdings, I give you back a buy / add / hold / trim / sell call on
every position plus a portfolio-level verdict. Read-only: I never touch your
brokerage and I never place a trade. The report is the thing you review and act
on yourself.

This is the single entry point. It orchestrates the underlying frameworks
(`quality-screen` → `investment-team` → `portfolio-review`) internally — you
don't toggle skills, you run one command.

---

## Modes

- **Interactive (default)** — you paste holdings; full pipeline below, with the
  confirm gate.
- **`/compound daily`** — unattended refresh. Reads saved holdings from
  `reports/private/holdings.txt`, **skips the confirm gate**, re-prices every
  position, regenerates the dashboard, and **prepends one dated entry** to the
  Daily-suggestions log noting what moved. It does **not** re-run the deep
  4-master research (that's expensive and nothing changes that fast) — it
  re-prices, recomputes weights, and re-flags any call that the new prices
  change (e.g. a TRIM target now hit, a new 52-week extreme, a position that
  crossed a concentration threshold). Cheap enough to run every morning.
- **`/compound weekly`** (or just rerun interactively) — the full deep
  re-research. Do this when you actually want fresh theses, not daily.

For daily/weekly mode the holdings come from `reports/private/holdings.txt` (one
holding per line, e.g. `MSFT 4` or `AAPL 10 @ 180`; `cash 500`).
If that file is missing, say so and fall back to asking for a paste.

---

## Input — how to give me your portfolio

Any of these works. No login, no credentials, no API.

| Form | Example |
|------|---------|
| Pasted list | `AAPL 50, NVDA 20, RKLB 300, $4000 cash` |
| With cost basis | `AAPL 50 @ $180, NVDA 20 @ $700` |
| Weights only | `AAPL 30%, NVDA 25%, cash 15%` |
| Broker export (CSV / XLSX) | Point me at a file exported from Robinhood, Fidelity, Schwab, Vanguard, E*TRADE, Empower, etc. |

**Broker file import.** Most money apps export CSV or XLSX. Normalize any of them
with the bundled tool (stdlib only, no install):

```
python tools/import_holdings.py <path-to-export> --out reports/private/holdings.txt
```

It sniffs the header for symbol / quantity / cost columns (layouts differ per
broker), converts a total cost basis to per-share when needed, and emits the
holdings format below. For an old `.xls` (binary) export, ask the user to
re-save as CSV or XLSX. Ignore option legs and pending orders unless asked.
After import, **always show the parsed table and confirm** before researching.

---

## Step 1 — Parse and CONFIRM (the gate)

Build the holdings table and **show it to the user before doing any research.**
This is the confirmation layer — nothing runs until they say go.

| Ticker | Name | Shares | Cost | Price | Mkt Value | Weight |
|--------|------|--------|------|-------|-----------|--------|

- Fetch current price per ticker (WebSearch / a quote source). Cash is a position.
- Compute weights from market value. Verify the total.
- Ask: **"This is what I'll research — correct? Anything to add to a watchlist?"**
- Accept watchlist tickers (names you don't own but are considering) — they get
  the same research so you can compare against what you hold.

Do not proceed past this step without confirmation.

---

## Step 1.5 — Triage & right-size (do this before researching)

Two judgments that keep the run proportionate and honest:

**Classify each holding:**
- **Analyzable business** → full pipeline below (AAPL, banks, miners, etc.).
- **Not a single business** → ETF / index / copy-trade basket. Don't run moat/DCF on
  it; describe what it actually holds and what role it plays in the book.
- **Unvaluable** → crypto, meme coins. No cash flows, no moat — say so plainly,
  give a one-line risk note, do not force a value verdict.
- **Pure momentum / distressed penny** → flag it as not-a-value-holding and assess
  the trade (size, exit), not the "investment".

**Right-size depth to account size and position weight.** Firing four master-agents
on every name is often absurd (a 10-name, $300 account does not need 40 agents):
- Large/core positions of a meaningfully-sized account → full four-master team.
- Small account, or positions <3–5% → one combined-analyst pass per name.
- Always state in the report which depth you used and why.

## Step 2 — De-risk screen (fast)

Run the `quality-screen` 7-indicator test on every holding to flag anything that
fails the floor for a first-rate business (10y avg ROE <8%, negative 5y FCF,
interest coverage <2x, gross margin <15%, OCF/NI <0.7, net margin <5%, >20%
share dilution). Apply the three exemptions (strategic-investment phase,
deliberate-low-margin, high-turnover-thin-margin) before flagging.

Output a one-row-per-holding pass/fail strip. A failed screen doesn't auto-sell
— it raises the bar for the deeper research in Step 3.

---

## Step 3 — Deep research, per position (parallel)

For each holding **and** each watchlist ticker, run the four-master team in
parallel background agents (this is `investment-team`). Launch all agents for a
given company in one message.

| Agent | Lens | Master |
|-------|------|--------|
| business-analyst | business model & moat | Duan Yongping |
| financial-analyst | financials & valuation | Buffett |
| industry-researcher | industry & competition | Munger |
| risk-assessor | risk & management | Li Lu |

Each agent must:
- Use WebSearch for the latest public info (filings, earnings, news).
- **Pull every key financial number from two independent sources** per
  `financial-data.md` (US: macrotrends + stockanalysis; HK: aastocks +
  macrotrends; A-share: eastmoney + cninfo). Flag any >1% discrepancy.
- **Never mental-math valuation.** Use the Bash tool to call:
  - `python tools/financial_rigor.py verify-market-cap --price P --shares S --reported R --currency USD`
  - `python tools/financial_rigor.py verify-valuation --price P --eps E --bvps B`
  - `python tools/financial_rigor.py three-scenario --price P --eps E --shares S --growth opt neu pes --pe optPE neuPE pesPE`
  - Embed the tool output in the analysis as the verification record.
- Return a scored writeup with a clear conclusion, bull AND bear case, and sources.

To keep it tractable on a large portfolio: research positions in descending
weight order; for very small positions (<3% and passed the screen) a single
combined analyst pass is fine instead of the full four-agent team — say so in
the report when you do this.

---

## Step 4 — Portfolio-level analysis

This is `portfolio-review`. After per-position research:

- **Concentration**: top position <40%, top-3 50–80%, 5–15 names, cash 10–30%.
- **Correlation**: surface hidden overlap (same theme/country/supply chain) and
  what a single macro shock does to the whole book.
- **Opportunity cost**: rank every position by expected annual return × certainty
  (`FCF yield + growth` as the base estimate, cross-checked with
  `three-scenario`). The key question: is the lowest-ranked position beating cash
  (~4% risk-free)? If not, it's a sell candidate.
- **Stress test**: recession, rate spike, sector PE compression, geopolitical —
  qualitative + rough magnitude per scenario.

---

## Step 5 — The report (the only output that matters)

Write one report. Per position **and** portfolio-level. Structure:

```
1. One-line portfolio verdict
2. Holdings table with a Call column: BUY MORE / HOLD / TRIM / SELL / NEW
3. Per-position cards — each: thesis still intact? valuation, bull, bear,
   the call, and a target price band
4. Portfolio analysis — concentration, correlation, opportunity cost, stress test
5. The single most important action right now (one sentence)
6. Biggest current risk (one sentence)
7. Add-signals / trim-signals to watch per position
```

End with the standard disclosures: **information-richness rating (A/B/C)** per
name, an **AI research-limitations note**, and the reminder that this is
analysis, not a trade order — the user decides and executes.

Save to **`reports/private/portfolio-latest.md`** (gitignored — real holdings
never get committed; append the dated review + any rebalance notes over time).
The tracked `reports/portfolio-latest.md` is a sample only — never write real
holdings there.

---

## Step 6 — Generate the dashboard (the thing you actually look at)

Also write a **self-contained HTML dashboard** to
**`reports/private/dashboard.html`** (gitignored). One file, inline CSS + tiny
vanilla JS only (no server, no external dependencies, no frameworks) — it must
open by double-click and work offline. Three tabs:

**Tab 1 — Dashboard**
- KPI strip (total value, position count, cash %, cash freed if you act)
- "Most important action" + "Biggest risk" callouts
- A **"Suggested moves" table with CONCRETE amounts** — never just a target
  percentage. For every trim/sell, compute and show **shares to sell and the
  dollar amount**, plus the resulting weight (e.g. "NVDA: sell ~2 of 7 sh
  (~$380) → 13% → 9%"). Sum the total dry powder freed.
- Holdings table with weight bars and color-coded call badges
  (BUY/ADD green, HOLD blue, TRIM amber, SELL red)
- **Every ticker is a clickable link** to its Yahoo Finance quote page
  (`https://finance.yahoo.com/quote/{TICKER}`; crypto uses `{TICKER}-USD`).
- A few per-position cards (bull/bear one-liners + a concrete "Do:" line)
- A **"Daily suggestions"** log: a dated list. On each run, **prepend today's
  entry** (date + what changed + the day's call) above the prior entries —
  don't overwrite the log. This is what turns a one-shot report into a running
  advisor.

**Tab 2 — Predictions** — researched ideas sized to available cash:
- State the user's concentrations and current cash.
- **Diversify** ideas: low-correlation holdings (broad-market ETF, short-Treasury
  ETF like SGOV for real cash yield, gold) that reduce the flagged concentration
  risk — each sized as a $ split of the freed cash.
- **Deepen** ideas: for themes the user already holds, suggest the *basket* (an
  industry ETF) or the quality blue-chip over a single micro-cap to cut
  single-stock blow-up risk — framed as a **swap**, not new money — and say
  "skip / already covered" where adding would worsen concentration.
- **Actually research each candidate** (web search for live price, fee/yield,
  what it holds, recent performance; fundamentals for a single company). Render
  each as an **expandable research card** (`<details>`) whose body has:
  **Thesis · key data line · 🟢 Bull · 🔴 Bear/risks · Fit to your book · Call.**
  Don't just list a ticker and a one-liner — a suggestion needs its "why".
- **Write a full standalone research report** per candidate to
  `reports/private/research/{TICKER}.md` (gitignored) — a proper multi-section
  deep-dive (Snapshot, What it is/holds, Performance & risk, Costs & taxes, Bull,
  Bear/risks, Role in this portfolio, Alternatives & how to choose, Verdict).
  For a single company, make it a full equity note (business, financials,
  valuation, moat, management, scenarios). The card body is the *summary*; this
  file is the *full report*.
- Each card's **"⬇ Download full report"** link points at that file:
  `<a class="dl" href="research/{TICKER}.md" download>`. (Real downloadable
  reports, like the report archive — not a re-dump of the card text.)
- Tickers link to Yahoo Finance. Mark amounts/ideas as illustrative, not advice.

**Tab 3 — Glossary** — plain-English, one line each, for every piece of jargon
that appears anywhere in the report (moat, ADR, de-listing, ETF, P/E, P/B, FCF
yield, dividend yield, NIM, ISR, value vs momentum, concentration, correlation,
dry powder, trim vs sell, position sizing). Also add `title="..."` hover
tooltips on jargon used inline in the other tabs (dotted underline) so the
reader never has to leave the page to understand a term. **Assume the reader is
new to investing** — define before you use.

End every tab's content with the same disclosures as the markdown report.

Because real holdings live in it, the dashboard stays in `reports/private/`
(gitignored). Open it locally; do not push it to a public host. For a "daily
suggestions" cadence, schedule `/compound` to re-run (e.g. via the `schedule`
or `loop` skill, or cron) — each run refreshes the page and grows the log.

---

## Hard rules (inherited from CLAUDE.md — non-negotiable)

- **Objective, objective, objective.** Every claim backed by data + source. No
  "I think" / "obviously" — use "the data shows" / "evidence indicates".
- **No preset stance.** Data first, logic second, conclusion last. Show both
  sides of every judgment ("but on the other hand…").
- **Honest about uncertainty.** Say "insufficient data" rather than filling a
  framework with speculation to fake confidence.
- **Cross-check.** Key numbers need two independent sources; market cap is
  always recomputed (price × shares) and compared to the reported figure.
- **Currency is explicit** on every figure (USD / HKD / CNY).
- **Read-only.** No brokerage connection, no order placement, ever. The report
  is the deliverable; the human is the executor.
