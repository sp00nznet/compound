# Investment Research Team: Four-Role Parallel Analysis Framework

Conduct a team-based investment research analysis on $ARGUMENTS. Use the Team tools to spin up a genuine multi-agent parallel research team.

## Execution Flow

### Step 1: Present the team framework

Show the user the following team structure and start once confirmed:

| Role | Responsibility | Analytical Framework |
|------|------|----------|
| **team-lead** (you) | Coordinate, synthesize judgments, deliver the final report | Combined four-master framework |
| **business-analyst** | Business model & moat analysis | Duan Yongping's lens |
| **financial-analyst** | Financial statements & valuation analysis | Buffett's lens |
| **industry-researcher** | Industry landscape & competitive dynamics | Munger's lens |
| **risk-assessor** | Risk assessment & management evaluation | Li Lu's lens |

### Step 1.5: AI research-bias assessment

Before creating the team, show the user an "AI researchability" assessment of the company:

**Information-richness rating** (determines research strategy):
| Tier | Characteristics | Research strategy adjustment |
|------|------|------------|
| Tier A (information-abundant) | Long-listed, broad sell-side coverage | The team focuses on **counter-checking** and **non-consensus angles**, avoiding "correct-but-useless" output that merely echoes the market |
| Tier B (moderate information) | Recently listed, limited coverage | Every agent's estimated figures must carry a confidence level; the team-lead flags "data sufficiency" when synthesizing |
| Tier C (information-scarce) | Obscure / newly listed / emerging market | The team shifts to "first-principles mode": don't chase report completeness, focus on a few core questions about the business's essence |

**Key reminder**: More material ≠ higher certainty; less material ≠ lower certainty. The confidence an AI can output ≠ the true certainty of the investment. Certainty comes from the business model itself, not from the volume of material.

Communicate the rating to each agent, as it shapes how they research.

### Step 2: Create the team

Use TeamCreate to create the team:
- team_name: `{company_name}-research` (lowercase English, e.g. `meituan-research`)
- agent_type: `team-lead`

### Step 3: Create 4 tasks

Use TaskCreate to create the following 4 tasks (each must have subject, description, and activeForm):

#### Task 1: Business model analysis
- subject: `Analyze {company_name}'s business model, moat, and user value`
- description includes:
  1. Essence of the business model: definition of the core business, breakdown of revenue structure
  2. How the platform/product flywheel operates
  3. Moat analysis: brand / switching costs / network effects / economies of scale / technological barriers, each verified individually
  4. User/customer value: what unique value is created for each party
  5. Business matrix and synergies
  6. Assessment against Duan Yongping's "good business" criteria: differentiation, pricing power, sustainable competitive advantage
  7. Require searching the latest financial reports, industry reports, and other public information

#### Task 2: Financial and valuation analysis
- subject: `Analyze {company_name}'s financial data, profitability, and valuation`
- description includes:
  1. Revenue, net profit, and operating profit trends over the past 3-5 years
  2. Profitability metrics: ROE, ROA, gross margin, operating margin
  3. Cash flow analysis: operating cash flow, free cash flow, capital expenditure
  4. Balance sheet health: cash reserves, leverage, liquidity
  5. Valuation analysis: PE/PS/PB/EV, etc., compared with history and peers
  6. Margin-of-safety assessment: intrinsic value vs. current share price
  7. **Financial rigor verification (must invoke the tool via Bash; mental math is forbidden)**:
     - Market cap check: `python3 ~/compound/tools/financial_rigor.py verify-market-cap --price {price} --shares {shares} --reported {reported_market_cap} --currency {currency}`
     - Valuation check: `python3 ~/compound/tools/financial_rigor.py verify-valuation --price {price} --eps {EPS} --bvps {bvps}`
     - Key-data cross-validation: `python3 ~/compound/tools/financial_rigor.py cross-validate --field {field} --values '{JSON}' --unit {unit}`
     - Three-scenario valuation: `python3 ~/compound/tools/financial_rigor.py three-scenario --price {price} --eps {EPS} --shares {shares_in_100M} --growth {bull} {base} {bear} --pe {bull_pe} {base_pe} {bear_pe}`
     - Embed the tool's output directly into the report as a verification record

#### Task 3: Industry and competitive analysis
- subject: `Analyze the {industry} industry landscape and {company_name}'s competitive position`
- description includes:
  1. Industry size and growth: market size, growth rate, penetration
  2. Competitive landscape: market share of major rivals, comparison of competitive strategies
  3. Threat assessment of key competitors: analyze each major rival one by one
  4. Landscape across each sub-segment
  5. Industry trends: technological change, policy impact, new entrants
  6. Value-chain analysis: value distribution across upstream, midstream, and downstream
  7. Require searching the latest industry data and competitive developments

#### Task 4: Risk and management assessment
- subject: `Assess {company_name}'s investment risks and management quality`
- description includes:
  1. Management evaluation: CEO's circle of competence, integrity, strategic vision, capital allocation ability, quality of past decisions
  2. Regulatory risk: current and potential regulatory impacts
  3. Competitive risk: assessment of the threat level posed by each rival
  4. Business risk: losses in new businesses, expansion uncertainty
  5. Macro risk: impact of the economic and industry cycles
  6. Governance structure: ownership structure, related-party transactions, shareholder-return policy
  7. Long-term certainty: what will the company look like in 10 years? What could disrupt its business model?
  8. Require searching the latest regulatory developments, management statements, etc.

### Step 4: Launch 4 parallel agents

Use the Task tool to launch 4 agents simultaneously (**must be called in parallel within a single message**):

Configuration for each agent:
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`
- `team_name`: the corresponding team name
- `name`: the corresponding role name (business-analyst / financial-analyst / industry-researcher / risk-assessor)

Prompt template for each agent:

```
You are the "{role_name}" on the {company_name} investment research team, responsible for analyzing {company_name} from {master_name}'s investment perspective.

Please complete task #{task_number}: {task_subject}

Specific requirements:
{task_description_content}

**Research method**:
- Use WebSearch to find the latest public information (financial reports, industry reports, news)
- **Financial data must come from two independent sources**, following the `skills/financial-data.md` standard (US stocks: macrotrends+stockanalysis; HK stocks: aastocks+macrotrends; A-shares: East Money+CNINFO); flag any discrepancy >1% between the two sources
- Ensure data accuracy and cite sources for key data
- Make the analysis deep, not superficial

**Output requirements**:
- The report should be thorough, using Markdown tables to present key data
- Each analytical dimension must have a clear conclusion and rating
- The report must end with an overall conclusion for that dimension

**When done**:
1. Use TaskUpdate to mark task #{task_number} as completed
2. Use SendMessage to send the complete analysis report to team-lead (type: "message", recipient: "team-lead")
```

### Step 5: Receive reports and track progress

- Show the user a live progress table (which agents are done, which are still researching)
- As each report arrives, update progress and present that report's key points (3-5 items)
- Wait until all 4 reports are in

### Step 6: Shut down team members

Once all reports are received, send a shutdown_request to each of the 4 agents (via SendMessage, type: "shutdown_request").

### Step 7: Synthesize the final report

Combine the 4 analysis reports and produce a final report with the following structure:

---

#### 1. One-sentence conclusion
> Summarize in a single paragraph (50-100 words) whether it's worth investing and the core logic

#### 2. Four-dimension scorecard
| Dimension | Framework | Score (1-5 stars) | Core judgment |
|------|------|------------|----------|

Overall score: X / 5

#### 3. Key data at a glance
Table of key financial and operating metrics (last 2 years compared)

#### 4. Summary of each dimension's analysis
Extract the 3-5 most important findings from each dimension

#### 5. Investment thesis (Bull vs. Bear)
- 🟢 Bull case (5-7 points)
- 🔴 Bear case (5-7 points)

#### 6. Buffett pre-purchase checklist
| # | Check item | Pass? | Notes |
10 core check items, each assessed

#### 7. Final investment recommendation
- Qualitative judgment table (business quality / management / valuation / timing)
- Tiered action recommendation table (aggressive / balanced / conservative → recommendation + price range)
- Key catalysts (3-5 each for add signals / trim signals)

#### 8. Concluding paragraph
A final summary of 100-200 words

---

### Step 8: Save the report

Write the complete final report to `~/{company_name}-investment-research-{date}.md` (date format YYYYMMDD).

### Step 9: Data spot-check (release gate)

```bash
# Step 1 — Extract the spot-check list (15% random sample)
python3 ~/compound/tools/report_audit.py extract \
  --report <report_file_path>

# Step 2 — For each item on the list, pull figures from reliable sources (see skills/financial-data.md)

# Step 3 — Output the pass/reject verdict
python3 ~/compound/tools/report_audit.py verdict \
  --results '<filled-in JSON>' \
  --report <report_file_name>
```

**[Released]** All pass → the report may be published; **[Rejected]** any failure → fix and re-review.

### Step 10: Clean up the team

Use TeamDelete to release team resources.

## Important notes

1. **The 4 agents must be launched in parallel** — call the Task tool 4 times within a single message
2. **Agents report via SendMessage** — this is message-based communication, not file-based collaboration
3. **Data accuracy** — require agents to use WebSearch for the latest data, with cross-validation of key figures
4. **Conclusions must be clear** — don't shy away from giving a buy/watch/avoid recommendation and a specific price range
5. **All analysis must be backed by data** — attach data sources
6. **Be patient** — the 4 agents take a few minutes to research; update the user on progress in real time
7. **Anti-bias awareness** — when synthesizing, the team-lead must assess: is each agent's analysis constrained by information abundance? Does it converge too closely with market consensus? The final report must include an "information-richness rating" and an "AI research limitations statement"
8. **Honesty principle under information scarcity** — better to leave a blank in the report flagged "insufficient data" than to fill out the framework with speculation to fake certainty
