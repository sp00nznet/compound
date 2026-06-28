# Deep Company Series: Dissecting One Company Across 8 Long-Form Essays

Write an 8-part deep-dive long-form series on $ARGUMENTS, for publication on public channels (WeChat official account, video channels, etc.). **The core IP is not "writing well" but "editing hard" — 99% of finance articles violate this skill's fact-checking standard.**

Reference sample: `reports/tencent/Understanding-Tencent/`

---

## 1. When to Use

The user wants "textbook-grade" deep research on a company, published publicly as a **long-form series**. Different from a single research note:
- 8 parts, ~120,000 characters, a complete loop from cognitive reset to decision framework
- Each part stands alone (good for sharing individually) but a single valuation / management / price-judgment thread runs through all of them
- Written for readers willing to "spend 90 minutes to truly understand a company", not for brokerage clients

**When NOT to use this skill**: single research notes, quarterly earnings reviews, industry research — use `/investment-research`, `/earnings-review`, `/industry-research` for those.

---

## 2. Series Outline Template (8 parts)

| # | Title template | Core question | Word count |
|---|---------|---------|------|
| 01 | You think you understand X — you don't | Cognitive reset: break 3 common illusions | 4,000-5,000 |
| 02 | X's moat — `<one-line business essence>` | How deep is the moat, will it still be there in 5/10 years | 6,000-8,000 |
| 03 | X's biggest profit engine — `<most profitable business>` | What the core business is, why it lasts | 6,000-8,000 |
| 04 | The other company hidden on X's balance sheet — `<hidden asset>` | Investment portfolio / subsidiaries / hidden value | 8,000-10,000 |
| 05 | In the AI (or current narrative) era, is X a winner or a loser | The era variable: break down the AI impact by business segment | 8,000-10,000 |
| 06 | Dissecting X's financials the Buffett way | Financial depth: gross margin / FCF / ROE / SBC | 8,000-10,000 |
| 07 | `<management quote>` — is X's management worth trusting | Capital-allocation discipline + integrity test + succession | 8,000-10,000 |
| 08 | What price is worth buying, what signal forces a sell (series finale) | DCF three scenarios + red-line checklist + position-sizing framework | 10,000-12,000 |

Add a `00-series-overview.md` as a table-of-contents index, not for publication.

---

## 3. Writing-Style Spec

### Tone

- **Direct, sharp, no fluff** — the first sentence delivers a number or a counterintuitive conclusion
- **Value-investing framework** — Buffett/Munger/Duan Yongping/Li Lu perspectives woven in (but don't pile on quotes)
- **No preset stance** — data first, then logic, then conclusion
- **Both sides** — every core judgment carries a "but on the other hand..." counterpoint
- **Official-account feel** — the first 18-20 characters must stand on their own (mobile preview)

### Banned words

| Banned | Reason | Replace with |
|------|------|------|
| obviously / inevitably / definitely | subjective absolutes | data shows / evidence indicates |
| I think / I feel | subjective tone | delete or change to "by this framework" |
| textbook-grade / stroke of genius | clickbait praise | describe the concrete fact |
| severely mismatched / severely undervalued | strong subjective words | give a specific discount percentage |
| perfect / flawless | one-sided judgment | add a counter-observation |

### Title style

- Use a **contrast number** or a **counter-consensus conclusion** as the hook ("15 years, 7 challenges, all failed", "¥42.92M annual pay is 0.0017% of profit")
- Subtitle is neutral and summarizes the content ("— `<essence judgment>`")
- **Avoid clickbait metaphors**: "little Buffett", "China's X", "GOAT" — all off-limits
- Use terms a professional reader knows ("Berkshire" rather than "Buffett", company name over person name)

---

## 4. Strict Fact-Check Checklist (the core IP)

### "False precision" traps to watch out for before you even write

1. **Probability-weighted expected value**: calculations like `30% × A + 50% × B + 20% × C = expected +X%` are almost all garbage — the probabilities are purely subjective and give the reader a false sense of precision. **List only scenarios + triggers + direction; do not compute a weighted expectation.**
2. **Third-party estimates of MAU/share**: QuestMobile / Qimai / CBNData and others differ wildly (can be 2-3x apart at the same point in time). **Use only the two most credible comparisons as anchors; describe the rest qualitatively.**
3. **Linear extrapolation of historical growth**: `2025 +33% × 5-year compound → 2030 X` is financially-illiterate forecasting. **Scenario assumptions + high/low range + not a promise.**
4. **Undisclosed stakes**: stakes in unlisted companies like ByteDance, Halti, etc. are **never publicly disclosed**. **Give a range, mark it "unknowable".**
5. **Strong attribution**: competitor failed = because of X. List all the multiple causes; **this article makes no single-cause attribution.**

### The 7 checks that must run during revision

```
□ 1. Cross-part number consistency: total market cap, Non-IFRS net profit, key stakes % aligned across the whole series
□ 2. Basis labeling: Non-IFRS / GAAP / Non-IFRS-SBC / FCF — which is used where, clear throughout
□ 3. Double-counting scan: consolidated subsidiaries not also in the "investment portfolio", no double-count in SOTP
□ 4. Fair like-for-like comparison: don't compare "core-business PE (ex-cash + portfolio)" vs "peer PE (not stripped)"
□ 5. Delete all probability weighting: see above
□ 6. Soften all absolute phrasing: grep "obviously|inevitably|severe|textbook|perfect"
□ 7. Cite third-party data: every non-financial-statement data point followed by "(source: X)"
```

### Known-error preferences

Before writing, **list known hard-error risks first**:
- Historical return multiples: must use cumulative-invested basis (e.g. Riot 33x, not 58x)
- Stakes: must use the latest Futu / filing basis (e.g. Tencent holds 1.5% of Meituan, not 6.4%)
- "Dividend-in-specie" accounting: deemed-disposal gain recognized on the declaration date per IFRIC 17 (e.g. JD in 2021, Meituan in 2022 but small amount)
- Share count rebounds: SBC grants concentrated early in the year temporarily lift share count

---

## 5. Execution Flow

### Phase 1: Research (complete before writing parts 01-02)

1. Read the company's last 5 annual reports and latest quarterly report
2. Read at least 3 independent sell-side reports (find consensus + counter-consensus)
3. Use `/investment-team` or `/investment-research` to first generate an internal research draft
4. Confirm the core thesis of the 8 parts with the user (avoid finishing only to find the direction was wrong)

### Phase 2: Writing (write in order 01→08, no skipping)

- Save each part to `reports/{company_name}/Understanding-{company_name}/0X-XX.md` as you finish
- Don't push to GitHub immediately — wait for the user's review
- Revise after the user gives feedback
- Only git push once revisions are done

### Phase 3: Cross-part consistency scan (after all 8 parts are written)

Dispatch Explore agents to scan the 8 parts in parallel for the following:
1. Same number (market cap, net profit, stake %) consistent across parts
2. Same term (FBS, SBC, Non-IFRS) explained on first appearance
3. References: does part 02 saying "see part 06" actually correspond
4. Recap vs body — are the numbers consistent

### Phase 4: Final pre-publication check

```bash
# Must grep locally once before pushing (per Compound privacy rules)
grep -r "linxuan\|/Users/\|<user company codename>" reports/ | head
```

Only `git pull --rebase && git commit && git push` after confirming it's clean.

---

## 6. Handling Revision Feedback

When the user gives revision feedback, process it in this order:

### 1. Fact-check first (don't just change it)

If the user says "X data is wrong", first use Bash/Read to find the source data and cross-validate:
- Check earnings/financial reports for the same company in the Compound project
- Check Futu / official disclosures
- Give a three-way comparison: "what the user said vs what I found vs what I used before"

### 2. Judge the revision level

| Level | Type | Handling |
|------|------|------|
| 🔥 Hard error | wrong number, wrong attribution, wrong basis | must fix, no hesitation |
| ⚠️ Subjective | strong subjective words, absolutes, clickbait metaphors | soften or delete |
| 🔬 Granularity | source labeling, basis refinement | low priority, balance against readability |
| ❓ Unreliable | wide third-party estimate spread | **deleting is safer than fixing** (explicit user instruction) |

### 3. Cascade check after revision

When you fix one spot, first think "where else references this number/concept". Example:
- Changed total market cap → cascade-update PE / core-business PE / discount / FCF Yield across the whole series
- Changed stake % → update top-10 ranking + historical-stakes table + divestiture list
- Changed a term's basis → update first definition + later references + recap

### 4. Report immediately after pushing

```
Push succeeded (commit hash).
Summary of [N] revisions [with table]:
- what was changed
- what was cascade-changed
- what was not changed

Awaiting next instruction.
```

---

## 7. What This Skill Does NOT Do

- **Doesn't make investment decisions for the reader** — every part ends with "not investment advice"
- **Doesn't predict stock prices** — only gives "scenario + trigger"
- **Doesn't compute a weighted "expected annualized return"** — subjective probability allocation misleads the reader
- **Doesn't write "Big Investor X also holds it"** — using someone else's holdings to vouch for your own judgment is anti-value-investing
- **Doesn't force all 8 parts** — if a part lacks enough standalone content (e.g. a company's management isn't distinctive enough), merge it into another part or cut the count

---

## 8. Compliance and Privacy

- All public reports **use only public information** (financial reports, official disclosures, brokerage reports, well-known third-party institutions)
- Use no **user personal information** (company codename, internal IM, undisclosed holdings)
- Before pushing, grep-scan privacy fields like `linxuan` / `/Users/` / user company codename (see `~/.claude/projects/-Users-linxuan/memory/feedback_privacy_upload.md`)
- Public bylines follow the user's multi-layer identity policy, never mixed

---

## One-Line Summary

**The core capability of writing the "Understanding X" series ≠ writing well, but editing strictly** — 89% of long finance articles die from false-precision numbers, subjective weighted expectations, and absolute phrasing. This skill exists to flag all those pitfalls: avoid them before writing, scrub them clean after.
