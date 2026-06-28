# Compound — AI Memory File

> This file records the project knowledge, user preferences, and historical decisions that Claude has accumulated while collaborating with the user, for reference in future sessions.

## User Profile

- Investment style: value investing, concentrated heavy positions, focused on Chinese internet + consumer + AI
- Research preferences: direct, sharp, no filler; wants clear conclusions rather than fence-sitting; data must be accurate
- Use case: assisting personal investment decisions, while also promoting this project as an open-source product

## Project Evolution History

### April 7–9, 2026 (first batch of research + framework refinement)

**Completed research:**
1. `/investment-team 拼多多` — the first complete 4-agent parallel research, overall score 3.4/5
2. `/investment-checklist` for 7 companies — Moutai, Tencent, NVIDIA, Meituan, Pinduoduo, Pop Mart, Kuaishou
3. Master holdings tracking — latest 13F filings of Buffett / Li Lu / Duan Yongping + PDD cost-basis analysis
4. Deep re-evaluation of 5 companies including Meituan (the user challenged the initial assessment)

**Revisions driven by user feedback:**
- Meituan changed from ❌ to ✅ conditional pass — the user pointed out: waiting until earnings recover to buy is too late; the fact that RMB 200 billion couldn't take it down = a real moat
- NVIDIA changed from ❓ to ✅ conditional pass — AI capex is still accelerating, Jevons Paradox
- Kuaishou changed from ❓ to ✅ conditional pass — Kling AI is underrated, Sora has been shut down

**Key lessons:**
- Don't apply the checklist mechanically; exercise independent judgment
- "Wait until earnings recover to buy" is a logical fallacy — the stock price reflects it in advance
- A competitor spent more money but gained no advantage = the best evidence of a moat

### Skill System Evolution

**V1 (5 Skills) — covering pre-purchase research:**
- investment-research, investment-team, investment-checklist, industry-research, private-company-research

**V2 (9 Skills) — completing the post-purchase workflow:**
- Added: earnings-review (close reading of earnings reports), thesis-tracker (thesis tracking), portfolio-review (portfolio management), management-deep-dive (deep dive on management)
- Fixed through 2 rounds of self-validation iteration: unified paths, completed tool calls, parallel collection, anti-bias mechanism, quantitative scoring formula

## Core Selling Points of the Project (already reflected in the README)

1. **Forces a conclusion, no hedging** — pass / fail / gray, with a specific price range
2. **Four-master adversarial perspectives** — not a division of labor but mutual challenge, creating real contradiction and tension
3. **Structured anti-bias mechanism** — A/B/C information richness, Munger inversion, fast rejection, anti-consensus
4. **Financial data precision** — Decimal exact calculation, market cap by hand, multi-source cross-verification
5. **Reproducible research process** — same input → structurally consistent output, supporting cross-sectional comparison and longitudinal tracking
6. **Multi-agent parallel depth** — 4 agents each search + analyze independently, 4x the information volume
7. **Live-trading validation** — RMB 1.46 million cumulative gains over two years, consistently beating the index by 40–50 percentage points

## User Preferences and Working Habits

- **Report language**: English
- **Pushing to GitHub**: the user usually asks to push after research is complete; ask proactively
- **Git operations**: the remote often has new commits (the user may also be editing elsewhere); always `git pull --rebase` before pushing
- **Attitude toward mistakes**: point them out directly, no need to be gentle. The user will challenge the AI's judgment, at which point you should seriously re-evaluate rather than defend
- **Don't over-summarize**: the user can read the diff; no need to recap what was done after every operation
- **Research depth**: better to spend time going deep and getting it right than to be rough for the sake of speed

## Known Issues and Areas for Improvement

- Some early files under reports/ have non-standard naming (mixed Chinese underscores); standardize to the English hyphenated format going forward
- Some early reports (such as 腾讯控股-投资研究报告.md) use old naming and have not been migrated
- The actual coverage of the financial_rigor.py tool needs to be validated during Skill execution
- The output examples in the README are fabricated and should later be replaced with excerpts from real reports
