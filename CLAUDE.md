# Compound — project instructions

## Overview

Compound is a Claude Code tool for value-investing portfolio research. The single
entry point is **`/compound`** (`skills/compound.md`): it takes a user's holdings
(pasted, or a broker CSV/XLSX export), runs them through the four-master framework
(Buffett, Munger, Duan Yongping, Li Lu), and produces a markdown report plus a
self-contained HTML dashboard. It is **read-only and never places trades**.

Fork of [AI Berkshire](https://github.com/xbtlin/ai-berkshire) by xbtlin.

## Structure

```
skills/      — Skill definitions (.md). /compound is primary; the rest are
               internal stages / deeper single-name tools. Copy to ~/.claude/commands/.
tools/       — Python helpers, stdlib-only: financial_rigor.py (exact math),
               import_holdings.py (broker CSV/XLSX → holdings format), report_audit.py
scripts/     — install-claude-commands.sh, daily.{ps1,sh} (unattended refresh)
assets/      — demo dashboard + screenshots
reports/     — sample output; reports/private/ holds real holdings (GITIGNORED)
```

## Privacy (hard rule)

Real holdings, dashboards, and daily logs live under `reports/private/` and
`logs/*.log` — both gitignored. **Never commit real holdings, account data, share
counts, cost bases, or personal identifiers.** Use fictional data in any committed
example, sample, or screenshot. When in doubt, put it in `reports/private/`.

## Research principles (highest priority)

- **Objective.** Every claim backed by data + source. No "I think" / "obviously" —
  use "the data shows" / "evidence indicates".
- **No preset stance.** Data first, logic second, conclusion last. The conclusion
  must follow from the data.
- **Both sides.** Every core judgment carries its counter-case.
- **Honest about uncertainty.** Say "insufficient data" rather than filling a
  framework with speculation.
- **Cross-check.** Key numbers need two independent sources; recompute market cap
  (price × shares) and compare to the reported figure. Use
  `tools/financial_rigor.py` for PE/ROE/valuation — never mental-math.
- **Currency explicit** on every figure (USD / HKD / CNY).
- **Not investment advice.** Output is analysis for the user to act on themselves.
  Flag holdings a value framework can't assess (crypto, baskets, momentum) rather
  than forcing a verdict.

## Output

- All reports and the dashboard are in **English**.
- Style: direct, sharp, no filler. ★ ratings (★1–5, no half stars).
- The dashboard must be a single self-contained HTML file (inline CSS + tiny JS,
  no external deps) that opens by double-click — see `skills/compound.md` Step 6.

## Git

- Local clone path: `~/compound/`. Commit messages in English.
- Before pushing real reports, re-run the privacy check: no real holdings, numbers,
  or identifiers in tracked files (`git grep --cached` the distinctive ones).
