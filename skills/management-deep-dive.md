# Management Deep Dive: Buying a Stock Is Buying the People

Conduct a deep management study of $ARGUMENTS.

**Supported input formats**: `company_name` or `person_name company_name`, e.g.: `Meituan`, `Wang Xing Meituan`, `Jensen Huang Nvidia`

> "Buying a stock is buying the people. Find people you trust, then hold for the long term." —— Duan Yongping
>
> "To evaluate management, watch what they do when no one is watching." —— Buffett

## Design Philosophy

Most investment analysis evaluates management on the surface: résumés, ownership stakes, compensation. But Buffett spends enormous time **eating and talking with management**, Li Lu says **the essence of his investing is investing in people**, and Duan Yongping says **buying a stock is buying the people**.

This Skill is the **deep-dive version** of step five (management evaluation) in `/investment-research`. Use it for in-depth study when the management score in standard investment research is uncertain (★★★ or below), or when management is the core of the investment thesis.

AI cannot dine with management, but through public information it can:
- **Track whether management's words and actions are consistent** (promises vs. delivery)
- **Analyze the return on every major capital allocation decision**
- **Infer character from decisions made during hard times**
- **Cross-validate through feedback from employees / merchants / customers**

## Execution Flow

### Step 1: Identify Key Management and Launch Parallel Data Collection

Use WebSearch to confirm the following key individuals:

| Role | Name | Tenure | Background | Ownership/Options |
|------|------|------|------|----------|
| CEO/Chairman | | | | |
| CFO | | | | |
| Founder (if not in office) | | | | |
| Actual controller (if different from CEO) | | | | |
| Other key executives | | | | |

**Note**: Distinguish between "who makes the decisions" and "whose name is on the title." At some companies the founder has stepped down but remains the soul of the company (e.g., Colin Huang at Pinduoduo).

After confirming the key people, use the Task tool to launch multiple background Agents to collect the following data **in parallel**:
1. Agent 1: Record of CEO public statements and predictions (shareholder letters, earnings calls, interviews, social media)
2. Agent 2: Record of capital allocation decisions (M&A, buybacks, dividends, new-business investments)
3. Agent 3: Governance structure and compensation (ownership structure, related-party transactions, executive pay)
4. Agent 4: Cross-validation information (employee reviews, customer feedback, industry reputation)

### Step 2: CEO Circle of Competence Assessment

#### 2.1 Strategic Vision

Search the CEO's public statements over the past 5 years (shareholder letters, earnings calls, interviews, social media) and extract their judgments on the following:

| Time | CEO's judgment/prediction | Actual outcome | Accuracy |
|------|--------------|---------|:------:|
| | "We believe market X will..." | Market X actually... | ✅/❌ |
| | "Over the next 3 years our focus is..." | Actual execution... | ✅/❌ |

**Key questions**:
- Has the CEO made correct calls ahead of the market?
- Has the CEO stayed level-headed when everyone else was bullish?
- Is the CEO's understanding of industry trends market-following or independent thinking?

#### 2.2 Execution Ability

| Dimension | Assessment | Evidence |
|------|------|------|
| Strategy to execution | Did they deliver on what they said? | |
| Organizational ability | Can they attract and retain talent? | |
| Crisis handling | How do they respond when facing difficulty? | |
| Iteration speed | How fast do they correct after a mistake? | |

### Step 3: Integrity Assessment (Most Important)

**Buffett**: "We look for three qualities: integrity, intelligence, and energy. If you don't have the first, the other two will kill you."

#### 3.1 Promises vs. Delivery Tracking

From the past 3 years of earnings calls, shareholder letters, and public interviews, extract the **specific promises** management has made:

| # | Time | Promise | Setting | Delivery | Verdict |
|---|------|---------|---------|---------|------|
| 1 | | "We will make business X profitable in 2025" | 2024 annual results call | | ✅/⚠️/❌ |
| 2 | | "We plan to buy back $X hundred million" | 2024 shareholder letter | | ✅/⚠️/❌ |

**Delivery rate statistics**:

| Promise delivery rate | Verdict |
|:---------:|------|
| >80% | Excellent — does what it says |
| 60-80% | Acceptable — right direction but execution deviates |
| 40-60% | Concerning — over-promises, under-delivers |
| <40% | Serious problem — not trustworthy |

#### 3.2 Performance During Hard Times

Search for major crises/difficulties in the company's history (stock crashes, earnings misses, regulatory shocks, intensifying competition), and analyze management's response:

| Crisis event | Time | Management's reaction | Verdict in hindsight |
|---------|------|-----------|-------------|

**Watch for**:
- Did they communicate proactively or dodge?
- Did they own the cause internally or pass the blame externally?
- Did they seize the moment to do the hard but right thing, or choose to pander to the market short-term?

#### 3.3 Attitude Toward Stakeholders

| Stakeholder | Management's attitude | Evidence | Verdict |
|-----------|-----------|------|------|
| Shareholders | Respect/ignore/exploit | | |
| Employees | Treat well/squeeze/neglect | | |
| Customers/users | Customer-centric/short-term extraction | | |
| Merchants/suppliers | Fair partnership/extreme price-squeezing | | |
| Regulators/society | Compliant cooperation/playing the gray zone | | |

**Li Lu**: "The attitude toward stakeholders determines a company's long-term vitality. Short-term squeezing can boost efficiency, but in the long run it damages the ecosystem."

### Step 4: Capital Allocation Ability

This is the management ability Buffett values most — **for every dollar earned, how much can management turn it into?**

#### 4.1 Record of Capital Allocation Decisions

Search the company's major capital allocation decisions over the past 5 years and evaluate each one:

**M&A record**:

| Time | Target | Amount | Strategic rationale | Return in hindsight | Score (1-5) |
|------|---------|------|---------|---------|:---------:|

**Buyback record**:

Use `tools/financial_rigor.py verify-valuation` to verify valuation metrics such as PE at the time of the buyback and currently.

| Time | Buyback amount | Average buyback price | PE at the time | In hindsight | Score (1-5) |
|------|---------|-----------|:------:|---------|:---------:|

**Dividend record**:

| Year | Dividend amount | Payout ratio | FCF same period | Sustainable? |
|------|---------|:------:|---------|:---------:|

**New-business investment**:

| Time | Investment area | Cumulative investment | Current status | Return assessment | Score (1-5) |
|------|---------|---------|---------|---------|:---------:|

#### 4.2 Capital Allocation Score

| Dimension | Score (1-5) | Notes |
|------|:---------:|------|
| M&A discipline | | Acquiring at reasonable prices? How was post-deal integration? |
| Buyback timing | | Buying back when undervalued, stopping when overvalued? |
| Dividend reasonableness | | Does the payout ratio match FCF? |
| New-business investment | | What's the success rate? How disciplined is the loss-cutting? |
| Cash management | | Are cash reserves reasonable? Hoarding too much? |
| **Overall score** | | |

**Buffett's standard**: Ideal management invests decisively when good opportunities exist, aggressively buys back/pays dividends when they don't, and never overpays for an acquisition.

### Step 5: Governance Structure Assessment

#### 5.1 Ownership Structure

| Item | Details | Risk assessment |
|------|------|---------|
| Any dual-class shares/super-voting rights? | | |
| Founder/actual-controller ownership stake? | | |
| Any VIE structure? | | |
| Are independent directors truly independent? | | |
| Recent buy/sell records by major shareholders? | | |

#### 5.2 Compensation Reasonableness

| Executive | Annual total comp | % of company net profit | Vs. peers | Reasonable? |
|------|-----------|:------------:|:---------:|:-------:|

**Watch for**: Is the incentive structure aligned with long-term shareholder interests? Or does it encourage short-term behavior?

#### 5.3 Related-Party Transactions

| Related party | Transaction | Amount | Arm's length? | Risk assessment |
|--------|---------|------|:-------:|---------|

### Step 6: Cross-Validation

AI cannot meet management face to face, but it can validate through public-channel indirect information. **Note**: the following depends on publicly searchable content, may be incomplete; flag the information source and availability.

#### 6.1 Employee Perspective

Search **publicly searchable** employee reviews such as Glassdoor rating summaries and Zhihu discussions (for login-required platforms like Maimai, flag as "users may supplement on their own"):

| Dimension | Rating trend | Key feedback |
|------|---------|---------|
| Company culture | | |
| Management rating | | |
| Work intensity | | |
| Compensation satisfaction | | |
| Growth prospects | | |

#### 6.2 Customer/Merchant Perspective

Search App Store ratings, consumer complaints, merchant forums:

| Dimension | Rating/trend | Key feedback |
|------|----------|---------|
| Product satisfaction | | |
| Customer service | | |
| Merchant/supplier relations | | |

#### 6.3 Industry Reputation

Search industry forums and social media to understand how peers and industry insiders rate this management team.

### Step 7: Scenario Analysis for the CEO's Departure

**Buffett**: "A good company should be one even a fool can run — because sooner or later, one will."

| Question | Answer |
|------|------|
| If the CEO left tomorrow, could the company run normally? | |
| How deep is the existing management team? Is there a clear successor? | |
| Does the company's competitive advantage depend on the CEO personally, or on the organization/system? | |
| Have past management transitions gone smoothly? | |

### Step 8: Output the Management Assessment Report

#### Report Structure

```
1. Key People at a Glance (table)
2. Integrity Assessment
   - Promise delivery rate
   - Performance during hard times
   - Attitude toward stakeholders
3. Ability Assessment
   - Strategic vision (prediction accuracy)
   - Execution ability
   - Capital allocation record
4. Governance Structure
   - Ownership structure risk
   - Compensation reasonableness
   - Related-party transactions
5. Cross-Validation
   - Employee perspective
   - Customer/merchant perspective
6. Overall Score and Conclusion
```

#### Overall Score

| Dimension | Weight | Score (1-5) | Weighted |
|------|:----:|:---------:|:----:|
| Integrity | 35% | | |
| Strategy and execution ability | 25% | | |
| Capital allocation ability | 25% | | |
| Governance structure | 15% | | |
| **Overall score** | 100% | | |

#### Duan Yongping's "Buying the People" Standard

> Answer the following three questions:
> 1. **Is this person honest?** (honest, doesn't take advantage of shareholders)
> 2. **Is this person capable?** (strategic vision + execution + capital allocation)
> 3. **Are you willing to hand your money to this person to manage for 10 years?**
>
> All three "yes" = ★★★★★ (5 points)
> First two "yes" = ★★★★ (4 points)
> Only the first "yes" = ★★★ (3 points)
> First is not "yes" = ★ (1 point, don't invest)

### Step 9: Save the Report

Write the report to `reports/{company_name}-management-{YYYYMMDD}.md`, e.g. `reports/meituan-management-20260409.md`

---

## Key Principles

- **Integrity is a single veto** — a lack of ability can be learned; a character flaw cannot be fixed
- **Watch actions, not words** — what management says doesn't matter; what they did does
- **Truth shows in hard times** — anyone is a good CEO with a tailwind; the real skill shows in a headwind
- **Capital allocation is the ultimate exam** — making money is easy, allocating the money you made well is hard
- **Don't fall in love with management** — stay objective; even people you admire can make big mistakes
