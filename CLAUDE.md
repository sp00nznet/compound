# Compound — Project Instructions

## Project Overview

A collection of value-investing research Skills built on Claude Code. Four-master framework: Buffett, Munger, Duan Yongping, Li Lu.
GitHub: xbtlin/ai-berkshire

The project is now centered on a single tool, `/compound` — a one-command portfolio research tool that takes pasted holdings or a brokerage CSV export and runs screen → 4-master research → portfolio analysis. It is read-only and never trades. The skills below remain available, but `/compound` is the primary single entry point.

## Project Structure

```
skills/          — Research Skill definitions (.md), copied to ~/.claude/commands/ for use
tools/           — Helper tools (financial_rigor.py for exact calculation)
reports/         — Investment research report output
assets/          — Static assets such as images
```

## Report Directory Structure

All reports are organized into folders by **company name**; every report related to a company goes in its corresponding folder:

```
reports/
├── AI产业研究/              — AI industry-chain panorama research (pinned)
│   ├── AI五层蛋糕-产业全景研究-20260605.md
│   └── AI五层蛋糕-公众号-20260605.md
├── 腾讯/                    — All Tencent research reports
│   ├── 腾讯-research-20260408.md
│   ├── 腾讯-earnings-2025Q4.md
│   ├── 腾讯-management-20260409.md
│   └── 腾讯-thesis.md
├── 拼多多/                  — All Pinduoduo research reports
├── 泡泡玛特/                — All Pop Mart research reports
├── 核电-industry-20260409.md — Industry reports go in the root directory
├── AI算力-funnel-20260509.md  — Funnel screening reports go in the root directory
├── AI-轮动判断-20260509.md    — Theme-level synthesis judgment reports go in the root directory
├── portfolio-latest.md       — Portfolio reports go in the root directory
└── 多公司对比-checklist-20260408.md — Multi-company reports go in the root directory
```

## Report Naming Conventions

| Skill | File naming format | Example |
|------|---------|------|
| /investment-team | `{company}/` directory containing 4 perspectives + final report | `reports/拼多多/最终报告.md` |
| /investment-research | `{company}-research-{YYYYMMDD}.md` | `reports/腾讯/腾讯-research-20260408.md` |
| /investment-checklist | `{company}-checklist-{YYYYMMDD}.md` | `reports/腾讯/腾讯-checklist-20260408.md` |
| /industry-research | `{industry}-industry-{YYYYMMDD}.md` (root directory) | `reports/核电-industry-20260409.md` |
| /industry-funnel | `{industry}-funnel-{YYYYMMDD}.md` (root directory) | `reports/AI算力-funnel-20260509.md` |
| /private-company-research | `{company}-private-{YYYYMMDD}.md` | `reports/字节跳动/字节跳动-private-20260408.md` |
| /earnings-review | `{company}-earnings-{period}.md` | `reports/腾讯/腾讯-earnings-2025Q4.md` |
| /earnings-team | `{company}/` directory containing 4 master perspectives + research draft + article + reader review | `reports/腾讯/腾讯-earnings-2025Q4.md` (final article) |
| /thesis-tracker | `{company}-thesis.md` (maintained long-term) | `reports/腾讯/腾讯-thesis.md` |
| /portfolio-review | `portfolio-latest.md` (root directory, continuously updated) | `reports/portfolio-latest.md` |
| /management-deep-dive | `{company}-management-{YYYYMMDD}.md` | `reports/腾讯/腾讯-management-20260409.md` |

## /investment-team File Structure

```
reports/{company}/
├── README.md                         — Research framework overview + core conclusions
├── 01-商业模式分析-段永平视角.md       — Business model analysis (Duan Yongping's perspective)
├── 02-财务估值分析-巴菲特视角.md       — Financial & valuation analysis (Buffett's perspective)
├── 03-行业竞争分析-芒格视角.md         — Industry & competition analysis (Munger's perspective)
├── 04-风险管理层评估-李录视角.md       — Risk & management assessment (Li Lu's perspective)
└── 最终报告.md                       — Team Lead synthesis report
```

## Core Principles of Research Analysis (highest priority)

- **Objective, objective, objective** — all research analysis must be based on facts and data; subjective conjecture is strictly forbidden
- Strictly distinguish "facts" from "opinions": facts must be backed by data; opinions must be explicitly labeled as "opinion" or "speculation"
- **No preset stance**: do not assume bullish or bearish in advance. Lay out the data first, then reason through the logic, then reach a conclusion. Conclusions must follow naturally from the data
- Avoid subjective phrasing such as "I think", "I feel", or "obviously"; use "the data shows", "the evidence indicates", or "according to source XX" instead
- **Present both sides**: every core judgment must be accompanied by counter-evidence ("but on the other hand...") so the reader can weigh it themselves
- Be honest and say "uncertain" or "insufficient data" when things are unclear; do not fill in certainty with speculation
- Every skill (investment-team, investment-research, earnings-review, etc.) must follow the above principles during execution

## Report Language and Style

- All reports are written in **English**
- Style: direct, sharp, no filler
- Data must be cited with sources; key figures must be cross-verified against at least 2 sources
- Estimated values must be marked as "estimate"
- Use ★ symbols for ratings (★1–5), no half stars
- Weave in commentary quotes from Buffett / Munger / Duan Yongping / Li Lu

## GitHub Operations

- Local clone path: `~/compound/`
- Remote repository: `https://github.com/xbtlin/ai-berkshire.git`
- Before pushing, run `git pull --rebase origin main` first (the remote often has new commits)
- Write commit messages in English, clearly describing what changed
- Do not push intermediate process files (such as data_collection.md); push only the final reports

## Common Commands

```bash
# Push reports to GitHub
cd ~/compound
git add reports/xxx.md
git commit -m "Add xxx report"
git pull --rebase origin main
git push origin main
```

## Notes

- Market cap must be verified by hand: share price × total shares outstanding, compared against the reported market cap
- Currency units must be explicit (HKD / RMB / USD) to avoid confusion
- Compute metrics such as PE/ROE precisely with tools/financial_rigor.py
- After finishing a report, proactively ask whether to push it to GitHub
