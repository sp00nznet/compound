---
name: news-pulse
description: Company news pulse — rapid attribution when a stock makes a sharp move. Deploys 4 parallel Agents to scout company events / regulatory policy / industry peers / market sentiment, producing an "event timeline + primary-cause attribution + whether a thesis re-review is triggered".
---

# Company News Pulse: Rapid Stock-Move Attribution Team

Run a recent-news scout and move attribution on $ARGUMENTS. **This is not deep research, it is a rapid intelligence response**—the goal is to answer within 10 minutes: "What just happened at this company? What is the real cause of the stock move? Do we need to re-review the investment thesis?"

## When to Use

- A held/watched stock spikes up or crashes (typical trigger lines: ±5% in a day, ±10% in a week)
- A stock moves after earnings and you want to quickly figure out what the market is reacting to
- You see a news headline but aren't sure whether it's noise or a real signal
- **Not for**: full research (use `/investment-team`), deep earnings reads (use `/earnings-review`), long-term thesis tracking (use `/thesis-tracker`)

## Execution Flow

### Step 1: Confirm Parameters and Scenario

Clarify the following with the user (if not provided in $ARGUMENTS):

| Parameter | Description | Default |
|------|------|------|
| **Company name** | Chinese / English / ticker all work | Required |
| **Time window** | Lookback days for news scouting | Default 14 days; can shrink to 7 days in earnings season |
| **Stock move** | Up/down magnitude + timeframe, e.g. "down 12% / 3 days" | Optional; if given, used to focus the attribution |
| **Focus emphasis** | Company events / regulatory / industry / sentiment | Default: equal weight across all four |

If the user only gives a company name, ask back first: "How many days of news? Is there a specific stock move you want explained?"—**don't silently assume**.

### Step 2: Information Availability Grading

Reference the A/B/C grading in `investment-team.md`, but with different dimensions:

| Grade | Characteristics | Scouting Strategy |
|------|------|---------|
| **Grade A (abundant info)** | Large cap, broad media coverage, earnings season | Focus is **denoising and attribution**—too much information actually makes the real cause harder to find; each Agent needs judgment to filter out "rehashed" secondhand news |
| **Grade B (moderate info)** | Mid/small cap, average coverage | Standard mode; attach 1-2 independent sources to each key event |
| **Grade C (scarce info)** | Small-cap HK names, newly listed, obscure | Switch to "broad-sweep mode"—you may find no news at all that explains the move, and **that conclusion is itself valuable** (the move may be technical/flow-driven rather than fundamental) |

Communicate the grade to each Agent, as it affects how they scout.

### Step 3: Create the Team

Use TeamCreate to create the team:
- `team_name`: `{company_name}-newspulse` (lowercase English, e.g. `pdd-newspulse`)
- `agent_type`: `team-lead`

### Step 4: Create 4 Scouting Tasks

Use TaskCreate to create the following 4 tasks:

#### Task 1: Company Event Scout (company-event-scout)

- **subject**: `Scout {company_name}'s own corporate events over the last {N} days`
- **description**:
  1. **Official filings**: latest disclosures on regulatory platforms such as HKEX / SEC / Cninfo
  2. **Earnings and guidance**: latest quarterly/annual report, pre-announcement, earnings call highlights
  3. **Management actions**: executive changes, buying/selling, buybacks, dividends, equity incentives
  4. **Major business events**: new product launches, M&A/restructuring, divestitures, big customers/big orders
  5. **Capital operations**: refinancing, convertible bonds, ADR conversion, return-to-A-share/delisting motions
  6. **Litigation and compliance**: lawsuits filed, self-disclosed compliance events
  7. Tag each event with: **date / source link / one-line summary / likely relevance to the stock move (high/medium/low)**
  8. Output a timeline table in reverse chronological order

#### Task 2: Regulatory and Policy (regulatory-watcher)

- **subject**: `Scout regulatory and policy changes for {industry/company} over the last {N} days`
- **description**:
  1. **Industry regulation**: new rules, fines, rectification orders, license changes in the company's industry
  2. **Cross-border policy**: US-China relations (for China ADRs), tariffs, export controls, data security
  3. **Tax policy**: changes related to VAT, corporate income tax, individual income tax
  4. **Antitrust and competition law**: investigations, fines, blocked deals
  5. **Sector-specific policy**: pharma centralized procurement, education "double reduction", real estate "three red lines", internet platform regulation, etc.
  6. **Monetary and FX**: changes in exchange rates / interest rates / capital controls affecting the company
  7. Tag each policy with: **date / source / degree of direct impact on the company (direct / indirect / unrelated)**
  8. Key judgment: did a "policy black swan" just land?

#### Task 3: Industry and Competitors (industry-peer-analyst)

- **subject**: `Scout {company_name}'s industry landscape and peer dynamics over the last {N} days`
- **description**:
  1. **Direct competitors**: list 3-5 core rivals and check each for recent events (earnings, products, price wars, personnel)
  2. **Up/downstream value chain**: upstream raw materials/suppliers, downstream customers/channels—recent changes in price, capacity, orders
  3. **Industry overall**: industry prosperity data, shipment volumes, demand-side signals (consumption data, tender data, etc.)
  4. **Substitution threats**: new technologies or business models disrupting the industry
  5. **Industry index performance**: recent performance of peer stocks—is the company outperforming / underperforming / in line
  6. Key judgment: **is this a company-specific event, or beta volatility across the whole industry?**
  7. Tag each event with source and date

#### Task 4: Market Sentiment and Sell-Side / Influencers (sentiment-tracker)

- **subject**: `Scout {company_name}'s market sentiment and changes in institutional views over the last {N} days`
- **description**:
  1. **Sell-side rating changes**: recent rating/price-target adjustments from Goldman, Morgan, CICC, etc.
  2. **Institutional holding changes**: 13F disclosures (US stocks), Stock Connect holdings, northbound fund flows
  3. **Short data**: short interest, newly published short reports (if any)
  4. **Influencer views**: you can run `python3 ~/compound/tools/xueqiu_scraper.py` to scrape recent relevant posts from influencers like Duan Yongping
     - Duan Yongping user_id: `1247347556`
     - Command example: `python3 ~/compound/tools/xueqiu_scraper.py --user-id 1247347556 --keywords {company_name},{ticker} --output /tmp/dyp-{company_name}.md`
     - Only call this when the company is a name Duan Yongping / Li Lu follows, otherwise skip to save time
  5. **Rumors and chatter**: unverified media rumors, social-media discussion hotspots (Xueqiu / X / Reddit)
  6. **Technical signals**: whether key support/resistance was hit, whether there were block trades, abnormal margin financing
  7. Key judgment: **is this fundamentals-driven or sentiment/flow-driven?**

### Step 5: Launch 4 Agents in Parallel

**You must call the Task tool 4 times in parallel in a single message**. Each Agent's config:
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`
- `team_name`: `{company_name}-newspulse`
- `name`: the corresponding role name (company-event-scout / regulatory-watcher / industry-peer-analyst / sentiment-tracker)

Prompt template for each Agent:

```
You are the "{role_name}" on the {company_name} news pulse team, responsible for scouting events in the {scout_dimension} dimension over the last {N} days.

Time window: {start_date} ~ {today_date}
Stock-move context: {user-provided price-move info, or "no specific move, routine checkup"}
Information availability grade: {A/B/C}

Please complete task #{task_number}: {task_subject}

Specific scouting requirements:
{task_description_content}

**Scouting method**:
- Prioritize WebSearch for time-sensitive queries (add a date or "recent" / "latest" / "2026" to keywords)
- Use WebFetch to closely read original sources for key events (filing text, earnings reports, regulatory documents)
- Do "independent source verification" for each event—rumors need at least 2 independent sources
- **Don't be misled by clickbait**: tag events where headline and body don't match as "misleading headline"

**Output format (important)**:
1. **Core findings**: 3-5 of the most critical events, 1-2 sentences each
2. **Full event timeline table** (reverse chronological):
   | Date | Event | Source | Relevance to stock move | Persistence |
3. **Attribution conclusion for this dimension**: based on the events scouted, answer "can this dimension explain the stock move? What's the confidence level?"
4. **Data gap statement**: what info wasn't found, what's questionable, what needs more time/disclosure
5. Strictly separate "fact" from "speculation", following the objectivity principles in CLAUDE.md

**When done**:
1. Use TaskUpdate to mark the task as completed
2. Use SendMessage to send the full scouting report to team-lead (type: "message", recipient: "team-lead")
```

### Step 6: Track Progress in Real Time

- Each time a scouting report arrives, show the user that dimension's 3 core findings
- Wait for all 4 reports to arrive
- Once all 4 are in, use SendMessage to send a shutdown_request to the 4 Agents

### Step 7: team-lead Synthesizes the Attribution

Aggregate the 4 scouting reports and produce the **move attribution report** (not a research report—the focus is "judgment"):

---

#### 1. One-Line Attribution
> In one short paragraph (30-60 characters), state: the primary cause + secondary cause + nature of this stock move (value event / sentiment swing / unknown)

#### 2. Full Event Timeline (4 dimensions merged)

Reverse chronological, merging events from all dimensions:

| Date | Dimension | Event | Source | Move-attribution weight |
|------|------|------|------|-----------|
| 2026-04-30 | Company | XX | link | 🔴 High |
| 2026-04-29 | Industry | XX | link | 🟡 Medium |
| 2026-04-28 | Sentiment | XX | link | ⚪ Low |

Weight legend: 🔴 High (enough to explain the move on its own) / 🟡 Medium (contributes part of it) / ⚪ Low (background noise)

#### 3. Move Attribution Table

| Candidate explanation | Evidence | Counter-evidence | Confidence | Persistence |
|---------|------|------|------|--------|
| E.g. earnings miss | revenue 5% below expectations, gross margin declined | one-off factor, management has an explanation | High | Short term, 1-2 weeks |
| E.g. industry beta | peers down 8% over the same period | this stock fell notably more than the industry | Medium | In line with the industry |

#### 4. Nature Judgment (core conclusion)

Check one:

- [ ] **Value event**: fundamentals genuinely changed (earnings, moat, management, endgame); thesis re-review needed
- [ ] **Sentiment/technical swing**: no change in fundamentals; flow/sentiment/beta-driven; can be treated as opportunity or noise
- [ ] **Cause unknown**: no event found that matches the magnitude of the stock move—**this is the most dangerous conclusion**; either the market knows something ahead of us (insider/front-running), or we missed a source
- [ ] **Mixed**: part value event + part sentiment amplification

#### 5. Per-Dimension Scouting Summary

3-5 most important findings per dimension + that dimension's attribution contribution.

#### 6. Action Recommendations

| Action | Recommended? | Rationale |
|------|--------|------|
| Trigger thesis re-review (`/thesis-tracker`) | | |
| Trigger deep earnings read (`/earnings-review`) | | |
| Trigger management re-review (`/management-deep-dive`) | | |
| Position action (add / trim / hold) | | For prompting only; final decision rests with the user |
| Observe only | | |

#### 7. Tracking Checklist for the Next 7-30 Days

- [ ] Pending event 1 (e.g. 5/15 earnings call)
- [ ] Metric to track 2
- [ ] Key signal to watch 3

#### 8. Information Gap Statement

Honestly list the open questions this scout couldn't resolve, the info that couldn't be found, and the items awaiting more disclosure. **Better to mark "uncertain" than to fill it with speculation**.

---

### Step 8: Save the Report

Write to `reports/{company_name}/{company_name}-news-{YYYYMMDD}.md`. If the `reports/{company_name}/` directory doesn't exist, create it (meaning no research report has yet been created for this company).

### Step 9: Clean Up the Team

Use TeamDelete to clean up team resources.

## Key Principles

1. **Fast beats complete**—the core value of this skill is delivering an attribution judgment within 10-15 minutes; don't fall into deep analysis (that's other skills' job)
2. **Attribution over enumeration**—finding events isn't hard; the hard part is judging "which event deserves credit for this move". Subtract, don't add
3. **Be honest about "unknown"**—when no primary cause can be found, explicitly write "cause unknown". That's more valuable than forcing a causal chain (the market may be front-running bad news)
4. **Don't presuppose a stance**—don't lean toward "it's just a sentiment swing, no big deal" because you hold the stock. Write whichever way the evidence points
5. **Distinguish "catalyst" from "coincidence"**—an event happening at the same time isn't necessarily the move's primary cause; check whether the magnitude of impact matches
6. **Respect information availability**—a Grade C company may simply have no findable news; that conclusion itself must be written down
7. **Follow the objectivity principles in `CLAUDE.md`**—every judgment carries a data source; separate fact from opinion
8. **Don't make decisions for the user**—provide attribution and an action-recommendation checklist, but leave the buy/sell decision to the user
