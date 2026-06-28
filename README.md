# Compound

**One command. Paste your holdings. Get a value-investing read on every position.**

Compound is a Claude Code tool that runs your portfolio through the frameworks of four
value investors — **Buffett, Munger, Duan Yongping, Li Lu** — and hands back a
buy / add / hold / trim / sell call on each name, plus a portfolio-level verdict.

It is **read-only**. It never connects to your brokerage and never places a trade. The
report is the thing you review and act on yourself.

> A fork of [**AI Berkshire**](https://github.com/xbtlin/ai-berkshire) by xbtlin.
> The original is a broad, bilingual collection of ~18 research skills. This fork
> refines it toward one dead-simple tool, in English, and is privacy-first.
> Full credit to the original author — see [Acknowledgments](#acknowledgments).

---

## What it does

```
You:  AAPL 50, NVDA 20, URG 300, $4000 cash
      (or: point it at a Robinhood / brokerage export CSV)

/compound:
  1. Parses your holdings and shows you the table — confirms before doing anything
  2. Screens each name (7 hard quality indicators)
  3. Researches each real business through the 4-master team (in parallel)
  4. Analyzes the portfolio: concentration, correlation, opportunity cost, stress test
  5. Writes one report — a call on every position + the single most important action
```

No login. No credentials. No API keys. You paste a list or drop a CSV; that's the whole setup.

## How this fork is different

| | AI Berkshire (upstream) | Compound (this fork) |
|---|---|---|
| Surface | ~18 skills you toggle | **one command, `/compound`** |
| Input | per-skill prompts | **paste holdings or a brokerage CSV** |
| Language | Chinese-first (English README) | **English throughout** |
| Privacy | reports committed to repo | **your real holdings are gitignored, never committed** |
| Scope | full research suite + report archive | refined to the portfolio tool (suite still available under the hood) |

The depth is inherited, not thrown away — the underlying screen, four-master research,
and portfolio frameworks are the original's IP. Compound just removes the toggling and
the manual steps.

## Quickstart

```bash
git clone <your-fork-url> compound
cd compound

# install the skills as Claude Code commands
cp skills/*.md ~/.claude/commands/

# in Claude Code:
/compound
# then paste your holdings when asked
```

The Python helpers in `tools/` (exact market-cap / valuation math, report audit) run with
zero external dependencies — standard library only.

## What's under the hood

`/compound` orchestrates the original frameworks as internal stages:

- **`quality-screen`** — 7 hard indicators (ROE, FCF, interest coverage, margins, dilution) with three exemption rules, to flag anything that fails the floor for a first-rate business.
- **`investment-team`** — four parallel agents, one per master lens: business model & moat (Duan Yongping), financials & valuation (Buffett), industry & competition (Munger), risk & management (Li Lu).
- **`portfolio-review`** — concentration, hidden correlation, opportunity cost vs. cash, and stress tests.

It also right-sizes effort: a small account doesn't get 40 agents, and holdings a value
framework can't assess (crypto, copy-trade ETFs, momentum names) are flagged honestly
rather than forced into a verdict.

The other skills (`earnings-review`, `industry-research`, `management-deep-dive`,
`thesis-tracker`, and more) remain in `skills/` for when you want to go deeper on a single name.

## Principles (inherited, non-negotiable)

- **Objective.** Every claim backed by data and a source. No "I think" / "obviously".
- **No preset stance.** Data first, logic second, conclusion last — both sides of every judgment.
- **Honest about uncertainty.** "Insufficient data" beats a confident guess.
- **Cross-checked.** Key figures need two independent sources; market cap is always recomputed (price × shares).
- **Read-only.** No brokerage connection, no orders. You are the executor.

## Disclaimer

Compound is a research tool, not financial advice. Its output is analysis to inform your
own decisions. It does not place trades and cannot access your accounts. Investing carries
risk of loss; do your own due diligence.

## Acknowledgments

This project is a fork of **[AI Berkshire](https://github.com/xbtlin/ai-berkshire)** by
**xbtlin**. The four-master research methodology, the screening and valuation frameworks,
the Python rigor tools, and the original design are all the original author's work — this
fork stands entirely on that foundation. The upstream repository also documents the
author's real-money track record; that record belongs to them, not to this fork.

The frameworks draw on the publicly shared philosophies of Warren Buffett, Charlie Munger,
Duan Yongping, and Li Lu. Compound is an independent project and is not affiliated with,
endorsed by, or connected to any of them or to Berkshire Hathaway Inc.
