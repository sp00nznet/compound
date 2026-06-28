# Private Company Research: Multi-Agent Parallel Deep Research Framework

Conduct a team-based deep research analysis on $ARGUMENTS. Purpose-built for private companies like Ant Group, Xiaohongshu, SpaceX, and Stripe.

**Ultimate goal**: Under conditions of inherently scarce information, reconstruct this company's **true value** as faithfully as possible—not the valuation the market assigns, but what the business itself is worth.

## Framework Characteristics

Core differences between researching private vs. public companies:
- **No standardized financials**: requires multi-source assembly and cross-validation
- **Few valuation anchors**: relies on funding rounds, comparable-company analysis, and scenario modeling
- **Large information asymmetry**: demands more "jigsaw-puzzle" research methods
- **Uncertain exit path**: IPO / M&A / secondary transfer are all possible

## Awareness of AI Research Bias (the core premise of this framework)

Private companies are the area where AI research bias is most severe. You must constantly guard against the following traps:

**Core contradiction**: AI excels at structuring existing information, but information on private companies is inherently scarce. This leads to:
1. **False conservatism**: because data is scarce, AI tends to give conservative/vague conclusions—but scarce data ≠ a bad company
2. **False precision**: to fill out a report template, AI may dress up "reasonable guesses" as "evidence-based analysis"
3. **Benchmarking trap**: forcing comparisons with public companies inherits public-company valuation logic and ignores the unique value of the private company
4. **Survivorship bias**: company information found online tends to skew positive (what companies actively spread is mostly good news)

**Guiding principles**:
- Better to leave blanks and say "don't know" than to fill tables with guesses that fake certainty
- Every data point must carry a confidence level (🟢 high / 🟡 medium / 🔴 low) so readers can judge for themselves
- Distinguish "verifiable facts" from "AI's reasoning," marked in different formats
- For companies with extremely scarce information, switch to "first-principles mode"—don't chase report completeness, just answer a few core questions:
  1. What real problem does this business solve? Is the demand real or fake?
  2. Why this team? What unique advantages do they have?
  3. If it succeeds, how high is the ceiling? If it fails, where is it most likely to die?
  4. What is the key validation milestone at the current stage?

**Turning information asymmetry to your advantage**: the market has little information on private companies → pricing efficiency is low → which is precisely where excess returns may come from. The goal of AI research is not to eliminate information asymmetry (impossible), but to extract the most critical basis for judgment from limited information.

---

## Execution Flow

### Step 1: Present the Team Framework

Show the user the following team structure and start after confirmation:

| Role | Responsibility | Core Perspective |
|------|------|----------|
| **team-lead** (you) | Coordination, information assembly, cross-validation, final report output | Investment decision integration |
| **business-decoder** | Business model breakdown & product/user analysis | "What is the essence of this business" |
| **financial-detective** | Financial data assembly & valuation modeling | "Reconstruct the true financial picture as much as possible despite missing information" |
| **competitive-mapper** | Industry landscape & competitive dynamics & substitution threats | "Who competes with it, who might disrupt it" |
| **risk-governance-analyst** | Full risk panorama & management/governance/investor assessment | "What could go wrong, who's at the helm" |
| **tech-ip-analyst** | Tech stack / patents / R&D capability / technical moat | "Is the technical barrier real or fake, and how long can it last" |
| **signal-miner** | Alternative-data mining: hiring/patents/litigation/app data/supply chain | "Beyond conventional information, what other clues are there" |

### Step 2: Create the Team

Use TeamCreate to create the team:
- team_name: `{company_name}-private-research` (lowercase English, e.g., `ant-group-private-research`)
- agent_type: `team-lead`

### Step 3: Create 6 Tasks

Use TaskCreate to create the following 6 tasks (each must have subject, description, activeForm):

---

#### Task 1: Deep Analysis of Business Model and Product/Users
- subject: `Break down {company_name}'s business model, product matrix, and user ecosystem`
- activeForm: `Analyzing {company_name}'s business model and user ecosystem`
- description includes:

```
## Deep Breakdown of the Business Model

### 1. Core Business Definition
- Define the essence of this business in one sentence (Duan Yongping style: use the plainest language to explain the business to someone smart but unfamiliar with the field)
- What problem does the company solve? For whom does it create value?
- Differentiation of the value proposition vs. similar products
- If the company didn't exist, how would users solve this problem? How costly is the alternative?
- "Rigidity" of demand: would users cut this spending in an economic downturn?

### 2. Revenue Model Breakdown
- Revenue composition: advertising/commissions/subscriptions/transaction take/financial services/SaaS/hardware/licensing fees, etc.
- Share of each revenue line (if data available) and growth trends
- Estimated monetization-efficiency metrics: ARPU, take rate, ad load, conversion rate, etc.
- Revenue quality assessment:
  - Share of recurring revenue vs. one-time revenue
  - Revenue concentration: share from top 5 customers/channels
  - Revenue predictability (contract/subscription type vs. transactional)
  - Whether revenue recognition is reasonable (any signs of premature recognition)
- Benchmark monetization efficiency against public peers

### 3. Unit Economics (UE) Estimation
- CAC (customer acquisition cost) estimation:
  - Share of paid acquisition vs. organic growth
  - CAC by channel (if available)
  - CAC trend: rising or falling as scale grows?
- LTV (lifetime value) estimation:
  - ARPU × expected lifetime
  - Account for cross-sell and upsell
- LTV/CAC ratio, payback period
- Marginal cost structure: marginal cost trend per new user/transaction
- Economies-of-scale inflection: when/whether breakeven has been passed

### 4. Product Matrix and Flywheel Effect
- Core products + extension products + incubated products
- How the flywheel turns: network effects / data flywheel / scale effects
- Synergies and cross-traffic between products
- Product life cycle: which stage each product is in
- Iteration speed: app/product update frequency, major feature updates in the last 12 months

### 5. Business Model Canvas (BMC)
Fully describe the business model using the following 9 elements:
| Element | Content |
|------|------|
| Value Proposition | |
| Customer Segments | |
| Channels | |
| Customer Relationships | |
| Revenue Streams | |
| Key Resources | |
| Key Activities | |
| Key Partners | |
| Cost Structure | |

### 6. Deep User Analysis
- User scale: MAU/DAU (estimated from QuestMobile, Sensor Tower, SimilarWeb, etc.)
- User growth curve: which stage of the S-curve (argue with specific data)
- User stickiness metrics:
  - DAU/MAU ratio (daily active / monthly active)
  - Average time spent, open frequency
  - Next-day/7-day/30-day retention (if available)
  - User growth vs. retention trend comparison (detecting fake growth)
- User profile: age/geography/spending power/occupation distribution
- User reputation:
  - App Store/Google Play rating trend (change over the last 12 months)
  - Social-media sentiment analysis
  - Real user feedback on Zhihu/Weibo/Xiaohongshu
  - Main concentration points of negative reviews
- User acquisition efficiency:
  - Ratio of paid acquisition vs. organic growth vs. word-of-mouth
  - Whether it relies on a single acquisition channel

### 7. Pricing Power Assessment
- Any price-increase history in the past 3 years? User churn after the increase?
- Price comparison with competitors: price leader or follower?
- Assessment of user price sensitivity
- Reasonableness of the commission/take rate within the value chain

### 8. Moat Assessment
Verify and score each of the following 6 dimensions (★1-5):

| Moat Type | Score | Evidence | Trend | Durability Assessment |
|-----------|------|------|------|-----------|
| Network effects | | More users, more value? One-sided or two/multi-sided? | Widening/Stable/Narrowing | |
| Switching costs | | Cost for users to migrate to a competitor? Data/relationship/habit migration cost? | | |
| Brand mindshare | | Category = brand? Estimated NPS? | | |
| Data barrier | | Has a data flywheel formed? Proprietary data assets? Data scale? | | |
| Regulatory license | | Is there an entry barrier? Difficulty of obtaining licenses? | | |
| Economies of scale | | Is the cost advantage from scale significant? | | |

Overall moat rating: Wide/Medium/Narrow/None

### 9. Internationalization Analysis (if applicable)
- Overseas market expansion
- Share of international revenue
- Localization strategy and challenges
- Differences in the overseas competitive landscape
```

---

#### Task 2: Financial Data Assembly and Valuation Modeling
- subject: `Assemble {company_name}'s financial data and perform valuation analysis`
- activeForm: `Assembling {company_name}'s financial data and valuation`
- description includes:

```
## Financial Data Assembly (Detective-Style Research)

Private companies have no standardized financials, so you must assemble from multiple sources and cross-validate. Every data point must be traced to a specific source, with time and confidence level noted.

### 1. Data Source Matrix
**Search the following sources by priority**:

| Priority | Source Type | Specific Sources | Credibility | Search Method |
|--------|---------|---------|--------|---------|
| 1 | Prospectus/regulatory filings | SEC filings, HKEX, CSRC-disclosed draft prospectuses | 🟢 high | Search "company name + prospectus/IPO filing" |
| 2 | Parent/affiliated public-company financials | e.g., Ant data in Alibaba's annual report, Google Cloud annual report | 🟢 high | Search affiliate disclosures in parent annual reports |
| 3 | Regulatory penalties/compliance disclosures | PBOC, CSRC, SAMR penalty documents | 🟢 high | Search "company name + penalty/fine/rectification" |
| 4 | Bond/ABS issuance documents | e.g., underlying data in Ant Huabei ABS prospectus | 🟢 high | Search "company name + bond/ABS/trust" |
| 5 | Business registration info | Tianyancha/Qichacha annual reports, paid-in capital | 🟡 medium-high | |
| 6 | Funding news | Valuation, funding amount, investors | 🟡 medium | Search "company name + funding/valuation" |
| 7 | Third-party research | Brokerage, consulting firm, industry association reports | 🟡 medium | Search "company name + research report/report" |
| 8 | In-depth media coverage | LatePost, The Information, 36Kr, Bloomberg | 🟡 medium | Search these outlets + company name directly |
| 9 | Industry-data estimation | Back into figures via industry totals and market share | 🔴 low-medium | |
| 10 | Ex-employee/insider leaks | Blind, Maimai, forums | 🔴 low | Reference only, not primary basis |

### 2. Estimation of Key Financial Metrics
Estimate the following as much as possible; **each data point must note**: source, time, confidence level, estimation method.

**Revenue side**:
- Total revenue scale and growth rate (last 3 years, annual/quarterly granularity)
- Revenue structure breakdown (by business line/product line)
- Decomposition of revenue growth drivers: volume (users/transactions) × price (ARPU/average ticket)
- Seasonal fluctuation pattern of revenue

**Cost side**:
- Gross margin estimate (benchmark against public peers, explain selection logic)
- R&D expense ratio estimate (via headcount × per-capita compensation, or share of R&D staff)
- Sales expense ratio estimate (via acquisition channels and spend data)
- G&A expense ratio estimate

**Profit side**:
- Operating profit/EBITDA estimate
- Net profit/adjusted net profit estimate
- Profitability timeline: when profitable? If not yet, when expected?

**Cash flow side**:
- Operating cash flow assessment (positive/negative, self-funding or not)
- Capex level and trend
- Free cash flow estimate
- Cash on hand / burn rate (estimated from funding amount, funding intervals, headcount)
- Cash runway: how long can it last at the current burn rate?

**Efficiency metrics**:
- Headcount and productivity (revenue per employee, profit per employee)
- Capital efficiency: revenue generated per ¥1 raised
- Benchmark efficiency metrics against public peers

### 3. Cross-Validation of Financial Data
- If a metric has multiple sources, list them all and explain discrepancies
- Estimate the same metric with different methods, check whether results converge
- Flag unverifiable "single-source" data

| Metric | Source A (data/time) | Source B (data/time) | Discrepancy | Adopted Judgment |
|------|-------------------|-------------------|------|---------|

### 4. Funding History and Valuation Evolution
Compile a complete funding timeline:

| Round | Time | Amount | Pre-money | Post-money | Lead Investor | Co-investors | Valuation Multiple Growth | Notes |
|------|------|------|---------|---------|--------|--------|------------|------|

Analysis:
- Whether the valuation growth curve is healthy (whether each round's multiple is reasonable)
- Whether funding intervals are reasonable (too frequent = burning fast? too sparse = trouble raising?)
- Whether a down round has occurred
- Whether existing shareholders keep doubling down (confidence signal)
- Inferred terms of the latest round:
  - Liquidation preference (1x/2x/participating)
  - Anti-dilution protection (full ratchet/weighted average)
  - Performance/IPO-timing ratchets (VAM)
  - Impact of these terms on common-stock value

### 5. Valuation Analysis (multi-method cross-check)

**Method 1: Latest funding valuation**
- Latest round valuation and time
- "Common-stock-equivalent valuation" after liquidation preference and other terms (typically needs a 20-40% discount)
- Adjustment for time elapsed since
- Analysis of this round's investors' motives (financial investment vs. strategic investment; strategic investors may pay a premium)

**Method 2: Comparable public companies**
- Select 3-5 comparable public companies, explain selection rationale
- Compare key multiples:

| Comparable | P/S | P/E | EV/EBITDA | EV/Revenue | Growth | Margin |
|---------|-----|-----|-----------|------------|------|--------|

- Adjustments applied:
  - Illiquidity discount: 20-30% (note specific value and reasoning)
  - Growth premium/discount
  - Scale discount
  - Regulatory/policy risk discount

**Method 3: DCF scenario analysis**
Three scenarios, each listing key assumptions:

| Assumption | Bear | Base | Bull |
|------|------|------|------|
| Next-5-year revenue CAGR | | | |
| Terminal operating margin | | | |
| Terminal growth rate | | | |
| WACC | | | |
| Terminal multiple (EV/EBITDA) | | | |

Each assumption must be supported by evidence; no assumptions out of thin air.

**Method 4: End-state market-cap reverse-engineering**
- Assume the business's market position at its end state in 5/10 years
- End-state revenue and margin assumptions
- Reasonable end-state multiple (reference mature peers in the industry)
- Reverse-engineer the reasonable current valuation range
- Implied annualized return

**Method 5: Transaction comparables**
- M&A/funding deals in the industry over the past 2 years
- Deal multiples (P/S, P/E)
- Deal context and premium/discount factors

### 6. Integrated Valuation Judgment

| Method | Valuation Range | Confidence | Weight | Weighted Valuation |
|------|---------|--------|------|---------|

- Do the valuations from different methods converge? If they diverge widely, analyze why
- The final valuation range must distinguish "fair value" from "conservative value" (margin-of-safety value)
```

---

#### Task 3: Industry Landscape and Competitive Dynamics Analysis
- subject: `Analyze the competitive landscape and substitution threats in {company_name}'s industry`
- activeForm: `Analyzing {company_name}'s industry landscape and competitive dynamics`
- description includes:

```
## Industry Landscape and Competitive Dynamics

### 1. Industry Positioning and Market Size
- Definition of the core arena the company operates in (note: the company's own definition may be flattering—judge independently)
- Three-layer market size TAM/SAM/SOM:
  - TAM (Total Addressable Market): the entire broad industry
  - SAM (Serviceable Addressable Market): what the company's tech/model can cover
  - SOM (Serviceable Obtainable Market): what it can actually capture now
- Comparison of market-size data sources (different research firms' forecasts can vary widely)
- Market penetration: current vs. ceiling
- Industry stage: nascent/growth/mature/decline (with evidence)
- Industry growth drivers: which forces are pushing/blocking industry growth

### 2. Full Value Chain Map
Draw the complete value chain structure (text diagram):

```
Upstream suppliers (who? bargaining power?)
    ↓
The company's link (which position in the value chain? share of the profit pool?)
    ↓
Downstream customers/users (concentration? alternative choices?)
    ↕
Competitors / substitutes / potential entrants
```

- Profit pool analysis: profit distribution across value-chain links
- The company's bargaining power within the value chain (upstream/downstream)
- Upstream/downstream dependency analysis: any single-supplier/single-customer dependency
- Structural changes underway in the value chain

### 3. Porter's Five Forces Analysis (quantified scoring)

| Force | Intensity (★1-5) | Key Factors | Impact on Company |
|------|-----------|---------|-----------|
| Internal rivalry | | Concentration, degree of differentiation, exit barriers | |
| Threat of new entrants | | Capital, tech, regulatory, brand barriers | |
| Threat of substitutes | | Substitute cost-performance, switching costs | |
| Supplier bargaining power | | Supplier concentration, switching costs | |
| Buyer bargaining power | | Customer concentration, information transparency | |

Overall industry attractiveness score: ★1-5

### 4. Deep Scan of the Competitive Landscape

| Competitor | Type | Market Share (est.) | Revenue Scale | Funding/Market Cap | Core Strengths | Main Weaknesses | Threat Level |
|---------|------|---------------|---------|----------|---------|---------|---------|
| Direct competitor 1 | Direct | | | | | | |
| Direct competitor 2 | Direct | | | | | | |
| Indirect competitor 1 | Cross-sector | | | | | | |
| Potential entrant 1 | Giant | | | | | | |

Key analysis:
- **Direct competitors**: head-to-head rivals in the same arena; analyze each one's strategic intent and resource commitment
- **Indirect competitors**: cross-sector potential competition, especially big tech's related businesses
- **Substitution threats**: different technical routes/models, especially disruption AI may bring
- **Potential entrants**: probability and mode of giants entering (build/acquire/invest)

### 5. Deep Competitor Comparison
Select the 2-3 most direct competitors (public and private), compare across dimensions:

| Dimension | {company_name} | Competitor A | Competitor B | Competitor C |
|------|---------|---------|---------|---------|
| Founding year | | | | |
| User scale (MAU) | | | | |
| Revenue scale | | | | |
| Revenue growth | | | | |
| Total funding/market cap | | | | |
| Valuation/revenue multiple | | | | |
| Monetization efficiency (ARPU) | | | | |
| Gross margin | | | | |
| Profitability status | | | | |
| Headcount | | | | |
| Technical capability | | | | |
| Differentiated positioning | | | | |
| Degree of internationalization | | | | |

### 6. Competitive Dynamics and Trends
- Key changes in the competitive landscape over the last 12 months (funding, M&A, product launches, personnel changes)
- Inferred strategic direction of competitors (inferred from hiring, patents, product updates)
- Structural shifts underway in the industry
- Impact of technological change on the competitive landscape (especially AI/large models)
- Impact of regulatory policy on the competitive landscape
- Is there a "winner-take-all" industry characteristic? Or will a stable oligopoly form?

### 7. Competitive Scenario Modeling
- Scenario A: the company wins—what conditions are needed? Probability?
- Scenario B: balanced coexistence—each player's survival space?
- Scenario C: disrupted—the most likely disruptor and path?

### 8. Global Benchmark Analysis
Find overseas/domestic benchmark companies (already public), analyze:

| Dimension | Benchmark A | Benchmark B | Implication for {company_name} |
|------|---------|---------|----------------|
| Development path | | | |
| Current valuation level | | | |
| Time from a similar stage to IPO | | | |
| Post-IPO stock performance | | | |
| Key factors of success/failure | | | |

- Note the limitations of benchmarking (specifics of the China market, regulatory differences, user-habit differences)
```

---

#### Task 4: Full Risk Panorama and Governance Assessment
- subject: `Assess {company_name}'s full-dimension risks and management/governance structure`
- activeForm: `Assessing {company_name}'s risk and governance structure`
- description includes:

```
## Full Risk Panorama and Governance Assessment

### 1. Deep Assessment of Founder/CEO

> "Buying a stock is buying the person." —— Duan Yongping

- **Background and résumé**: education, professional experience, entrepreneurial experience
  - Any serial entrepreneurship? Outcome of the last venture?
  - Years of relevant industry experience
  - Largest team/business previously managed
- **Strategic vision**: search the CEO's public remarks over the past 3 years (speeches, interviews, internal letters, social media)
  | Time | CEO's judgment/prediction | Actual outcome | Accuracy |
  |------|--------------|---------|--------|
  - Any correct judgments ahead of the market?
  - Any composure when everyone else was bullish?
- **Execution**: whether key milestones were hit on time
  | Commitment | Commitment Time | Commitment Setting | Delivery | Assessment |
  |------|---------|---------|---------|------|
- **Vision and values**:
  - Attitude toward users/employees/society (judge from concrete events, not slogans)
  - Choices when facing difficulty (how layoffs are handled, crisis management, trade-offs in conflicts of interest)
  - Trade-off between short-term profit and long-term value
- **Controversies**: any negative record (search "CEO name + controversy/scandal/issue")
- **Rating**: ★1-5 (with detailed reasoning)

### 2. Core Team Assessment
- Roster and backgrounds of core executives (CTO/CFO/COO/VP, etc.)
  | Name | Title | Background | Tenure | Prior Experience |
  |------|------|------|------|---------|
- Key talent movement analysis:
  - Departures of important executives in the last 2 years (who left? where to? why?)
  - Important executives who joined in the last 2 years (poached from where? what does it signal?)
  - Net talent inflow or outflow?
- Team complementarity: are the founding team's capabilities complementary? Any obvious gaps?
- Team culture signals:
  - Glassdoor/Maimai ratings and trends (direction of change over the last 12 months matters more than the absolute value)
  - Employee recommendation willingness (would recommend to a friend)
  - CEO approval rating
  - Public sentiment on overtime culture and organizational atmosphere
- Key-person dependency: what happens to the company if the CEO/CTO leaves?

### 3. Equity Structure and Governance

**Equity architecture**:
| Shareholder | Stake % | Voting % | Type | Notes |
|------|---------|-----------|------|------|

- Founder control structure: dual-class shares/concert parties/VIE architecture
- Trend of founder stake (dilution per funding round)
- Employee stock plan: coverage, vesting conditions, IPO ratchets

**Governance structure**:
- Board composition (share of independent directors, investor seats)
- Major decision-making mechanism
- Potential conflicts of interest:
  - Related-party transactions (deals between the founder's other companies and this company)
  - Competing businesses
  - Conflict points between major and minority shareholder interests

### 4. Deep Analysis of the Investor Roster

| Investor | Round | Amount | Est. Stake | Type | Strategic Value | Exit Pressure |
|--------|------|------|---------|------|---------|---------|

Analysis:
- Brand-endorsement significance of the lead investor (top-tier VC vs. unknown fund)
- Strategic synergy value of industrial capital (does it bring resources/channels?)
- Investor exit-pressure assessment:
  - How much fund life remains?
  - Has it already sold old shares on the secondary market?
  - Are ratchet terms nearing maturity?
- Red-flag signals in the investor roster:
  - Any investors with poor reputations?
  - Have early investors already fully exited?
  - Co-investment in the latest round (existing shareholders not following = lack of confidence?)

### 5. Full-Dimension Risk Checklist

| Risk Type | Specific Risk | Probability (H/M/L) | Impact (H/M/L) | Severity | Hedgeable? | Monitoring Metric |
|---------|---------|---------------|---------------|--------|-----------|---------|
| Regulatory risk | Antitrust, data security, industry crackdowns, license risk | | | | | |
| Competitive risk | Giants entering, new-model disruption, price wars | | | | | |
| Technology risk | Platform migration, AI disruption, tech-route failure | | | | | |
| Talent risk | Loss of founder/core team | | | | | |
| Financing risk | Capital chain, down round, trouble raising | | | | | |
| IPO risk | Listing window, regulatory approval, market environment | | | | | |
| Geopolitical risk | US-China relations, cross-border data, sanctions | | | | | |
| Monetization risk | Monetization below expectations, user backlash | | | | | |
| Governance risk | Related-party transactions, opacity, investor conflicts | | | | | |
| Compliance risk | Data privacy (GDPR/PIPL), content compliance | | | | | |
| Macro risk | Economic cycle, interest-rate environment, capital-market sentiment | | | | | |
| ESG risk | Environmental/social/governance-related risks | | | | | |

### 6. Exit Path Analysis

| Exit Method | Likelihood (★1-5) | Estimated Time Window | Expected Valuation Range | Key Prerequisites | Main Obstacles |
|---------|-------------|------------|------------|---------|---------|
| A-share IPO | | | | | |
| HK IPO | | | | | |
| US IPO | | | | | |
| Acquisition | | Who are the potential buyers? | | | |
| Secondary transfer | | How is liquidity? | | | |
| SPAC | | | | | |
| Stay private long-term | | | | | |

- Most likely exit path and reasoning
- Exit timeline modeling
- Expected return analysis under each exit path

### 7. Worst-Case Scenario Analysis (Munger-style inversion)

> "Invert, always invert." —— Munger

- How is this company most likely to **fail**? List 3 specific failure paths
- Probability assessment and trigger conditions for each failure path
- In the worst case, how much can investors recover? (liquidation value analysis)
- Why would smart people **not** invest in this company? (list at least 5 reasons)
- Historically, which companies of similar positioning/stage failed? Why?
- What signal indicates the "thesis is broken" and you should cut losses?
```

---

#### Task 5: Technical Capability and Intellectual Property Analysis
- subject: `Analyze {company_name}'s tech stack, patent portfolio, and R&D capability`
- activeForm: `Analyzing {company_name}'s technical capability and intellectual property`
- description includes:

```
## Deep Analysis of Technical Capability and Intellectual Property

> For a tech company, the authenticity and durability of the technical barrier directly determine whether the valuation is reasonable.

### 1. Tech Stack Analysis
- Inferred core technical architecture (inferred from job postings, tech blogs, open-source projects, conference talks)
- Whether the tech-stack choices are reasonable (right tools for the right problems?)
- Technical-debt signals:
  - Large numbers of "refactor/migration" roles in job postings
  - Whether a large-scale tech-stack switch is underway
  - Frequent bug/outage complaints on the user side

### 2. Patent Portfolio Analysis
Search patent databases (Google Patents, CNIPA, USPTO):

| Patent Metric | Data | Source |
|---------|------|------|
| Total patents (granted) | | |
| Patents pending | | |
| New patents in the last 2 years | | |
| Distribution across core tech areas | | |
| Citation count of key patents | | |
| International patent footprint | | |

- Patent quality assessment (not just quantity):
  - Any core/foundational patents?
  - Do the patents' technical areas align with the core business?
  - Any patent litigation (sued or suing)?
- Patent trend: is filing speed accelerating or slowing? Any shift in technical direction?
- Patent comparison with competitors

### 3. R&D Capability Assessment
- **R&D investment**:
  - Number/share of R&D staff (estimated from recruiting platforms, LinkedIn)
  - R&D expense estimate (headcount × average compensation + infrastructure)
  - R&D expense ratio (vs. peers)
  - R&D investment trend: increasing or shrinking?
- **R&D output**:
  - Academic papers published (search Google Scholar, arXiv)
  - Conference talks (search top venues like KDD, NeurIPS, SIGIR)
  - Open-source contributions (search GitHub org accounts)
  - Tech blog/WeChat-account output
- **R&D efficiency**:
  - Speed from technical R&D to product launch
  - Commercialization rate of technical achievements

### 4. Technical Talent Assessment
- **Core technical leaders**: background and capability of CTO/VP Eng/chief scientist
  | Name | Title | Education | Prior Company | Technical Influence |
  |------|------|------|--------|-----------|
- **Technical talent density**:
  - From which companies/labs? (share from top institutions like Google/Meta/MSRA/BAT)
  - Compensation competitiveness for technical roles (estimated from job postings)
  - Attrition signals in the technical team (departure activity on LinkedIn)
- **Hiring signals**:
  - What technical roles are currently open? (reflects technical strategy direction)
  - Hiring difficulty and fill speed for technical roles
  - Is a new technical team/lab being built?

### 5. Technical Moat Assessment

| Technical Barrier Dimension | Score (★1-5) | Evidence | Durability |
|-------------|-----------|------|--------|
| Algorithm/model barrier | | Any proprietary algorithms? Can they be replicated? | |
| Data barrier | | Data scale, proprietary data, data-flywheel speed | |
| Engineering barrier | | System complexity, engineering capability built over time | |
| Talent barrier | | Are core technical staff hard to replace? | |
| Ecosystem barrier | | Developer ecosystem, API/SDK coverage, technical standards | |

- Overall technical moat rating: Strong/Medium/Weak
- Assess the decay speed of the technical moat (in the AI era, the half-life of technical barriers can be very short)

### 6. AI/New-Technology Impact Assessment
- The company's AI capability and positioning
- AI's impact on the company's core business (enhancement vs. threat vs. neutral)
- Is the company a beneficiary or a victim of the AI transformation?
- Impact assessment of other emerging technologies (Web3/AR/VR/quantum computing, etc.)

### 7. Technical Risk Checklist
| Risk | Specific Description | Probability | Impact |
|------|---------|------|------|
| Tech-route failure | The technical direction bet on is disproven | | |
| Open-source replacement | Core tech replaced by an open-source solution | | |
| Platform dependency | Dependency on specific cloud/chip/OS | | |
| Security vulnerability | Data breach/system attacked | | |
| Talent loss | Core technical staff leave | | |
```

---

#### Task 6: Alternative-Data Signal Mining
- subject: `Mine {company_name}'s unconventional data signals and hidden clues`
- activeForm: `Mining {company_name}'s alternative-data signals`
- description includes:

```
## Alternative-Data Signal Mining

> Conventional information on private companies is limited; alternative data often provides truer operational signals than news coverage.
> The goal of this task: beyond conventional sources, mine every potentially useful clue.

### 1. Hiring Signal Analysis
Search job postings on LinkedIn, Boss Zhipin, Maimai, Indeed, Glassdoor:

**Hiring scale and trend**:
- Total current open roles
- Hiring trend over the last 6 months (accelerating/steady/shrinking)
- Hiring scale vs. competitors

**Hiring structure analysis**:
| Role Category | Count | Share | Signal Interpretation |
|---------|------|------|---------|
| R&D/Engineering | | | Technical direction |
| Product | | | Product strategy |
| Sales/BD | | | Commercialization stage |
| Marketing/Operations | | | Growth strategy |
| Data/AI | | | AI positioning |
| Internationalization | | | Overseas expansion plan |
| Compliance/Legal | | | Regulatory response/IPO prep |
| Finance/IR | | | IPO-prep signal |

**Key signal capture**:
- Hiring IR (investor relations) = IPO signal
- Hiring compliance/data security = regulatory pressure or IPO prep
- Hiring overseas roles = internationalization push
- Compensation range for senior roles = financial strength and talent competitiveness
- Tech stack/business direction mentioned in JDs = strategic direction

### 2. App/Product Data Analysis
Search App Store, Google Play, Qimai, SimilarWeb:

| Metric | Data | Source | Trend |
|------|------|------|------|
| App Store rank | | | last-6-month trend |
| User rating | | | direction of change |
| Number of ratings | | | growth rate |
| Estimated downloads | | | |
| App update frequency | | | |
| Main features in recent updates | | | |

- High-frequency keywords and sentiment analysis in App Store reviews
- Main concentration points of recent negative reviews (bugs? pricing? degraded experience?)
- Web traffic data (SimilarWeb): UV, PV, visit duration, bounce rate

### 3. Social Media and Sentiment Signals
Search Weibo, Zhihu, Xiaohongshu, Twitter/X, Reddit:

- Engagement data of the company's official accounts (followers/reposts/comments trend)
- Heat and sentiment of spontaneous user discussion (positive/negative/neutral)
- Industry KOLs' assessments of the company
- Sentiment hot-button events over the last 3 months
- Negative-sentiment checklist and the company's response
- Any leaks from insiders (former/current employees)

### 4. Corporate Registration and Legal Signals
Search Tianyancha/Qichacha/Qixinbao:

**Registration info**:
- Registered capital and change history
- Paid-in capital
- Shareholder/equity change records
- Subsidiary/affiliate list (new entity = new business? deregistration = business contraction?)
- Business-scope changes (newly added scope = new business direction)

**Legal info**:
| Type | Count | Summary of Important Cases |
|------|------|-------------|
| Litigation as plaintiff | | |
| Litigation as defendant | | |
| IP disputes | | |
| Labor arbitration | | |
| Administrative penalties | | |
| Records as judgment debtor | | |

- Details and potential financial impact of major litigation/arbitration
- Administrative penalty records (environmental/tax/labor/data security, etc.)

### 5. Supply Chain and Partner Signals
- List of known core suppliers/partners
- Are suppliers public? Do their financials mention cooperation data with this company?
- Bidding/procurement info (government procurement sites, enterprise bidding platforms)
- Partner assessments and depth of cooperation

### 6. Domains and Digital Footprint
Search domain/subdomain info:
- List of domains registered by the company (newly registered domains may hint at new business/products)
- Subdomain analysis (api.xx.com, pay.xx.com, etc. hint at business architecture)
- SSL certificate info
- Trademark registrations (newly registered trademarks = new brand/product line)

### 7. Industry Conference and Exposure Signals
- Executives' conference talks/attendance records over the last 12 months
- Industry awards/media rankings (made any "unicorn list," "most innovative," etc.?)
- Interactions with government/industry associations (policy consultation, standards participation)
- Trend in frequency and quality of media exposure

### 8. Secondary-Market Transaction Signals (if any)
- Is there an old-share trading market (SharesPost, EquityZen, WeChat groups, etc.)?
- Implied valuation of old-share trades vs. latest-round funding valuation
- Supply/demand between buyers and sellers
- Are large numbers of employees selling options/RSUs?

### 9. Integrated Signal Scoring

| Signal Category | Direction (pos/neg/neutral) | Strength (strong/medium/weak) | Confidence | Core Findings |
|---------|----------------|---------------|--------|---------|
| Hiring signals | | | | |
| Product data | | | | |
| Sentiment signals | | | | |
| Legal signals | | | | |
| Supply chain signals | | | | |
| Digital footprint | | | | |
| Industry exposure | | | | |
| Secondary trades | | | | |

**Combined signal judgment**: do the signals point in the same direction? Any contradictory signals?

### 10. Anomaly Signal Checklist (most important)
List all "unusual" findings—these are often the most valuable information:
- Signals inconsistent with the company's external narrative
- Data inconsistent with industry common sense
- Sudden changes (abrupt hiring contraction/expansion, dense executive departures, etc.)
- Unexplainable phenomena
```

---

### Step 4: Launch 6 Parallel Agents

Use the Agent tool to launch 6 agents simultaneously (**must be called in parallel in the same message**):

Configuration for each agent:
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`

Prompt template for each agent:

```
You are the "{role_name}" in the {company_name} private-company research team.

You are researching a **private company**, which means:
- No standardized public financials; you must assemble information from multiple sources
- Data may be incomplete or contradictory; you must note confidence levels
- More reasoning and reasonable estimation is needed, but show the estimation process transparently
- Not finding information ≠ the information not existing; the information you find may be biased

Please complete the following research task: {task_subject}

Specific requirements:
{task_description_content}

**Research methods**:
1. Use WebSearch to search the latest public information—at least 3-5 searches per dimension, with different keyword combinations
2. Search keyword strategy:
   - Chinese: company name + revenue/valuation/funding/user count/MAU/IPO/prospectus/layoffs/rectification
   - English: Company Name + revenue/valuation/funding/users/IPO/filing
   - Specific person name + company name (search management-related info)
   - Company name + specific competitor name (search competitive dynamics)
3. Priority sources:
   - High credibility: prospectuses, regulatory filings, affiliate disclosures in public-company annual reports
   - Medium credibility: LatePost, The Information, 36Kr, Bloomberg, Reuters, TechCrunch
   - Supplementary verification: Zhihu, Maimai, Glassdoor, Tianyancha, Qichacha
4. Use WebFetch to get the full text of key articles (don't rely only on search snippets)
5. For important data, cross-validate with at least 2 different sources

**Data annotation standards (strictly enforced)**:
- Note the source of each key data point (down to the outlet name and article title)
- Note the data time (precise to year-month)
- Note the confidence level: 🟢 high (prospectus/official disclosure) / 🟡 medium (credible media/research) / 🔴 low (estimated/rumor)
- When sources conflict, **list them all** and explain the discrepancy and your judgment
- Distinguish "fact" from "reasoning": facts in normal font, reasoning/estimation in *italics* with the estimation method noted
- Clearly mark unobtainable information as "data missing"; do not fabricate

**Output requirements**:
- The report must be thorough, using Markdown tables to present key data
- Each analysis dimension must have a clear conclusion and score
- The estimation process must be fully transparent (show the calculation logic and every assumption)
- At the end of the report, provide:
  1. Overall score for this dimension (★1-5) and core judgment
  2. Self-assessed information completeness for this dimension (sufficient/adequate/insufficient/severely insufficient)
  3. The 3 most important findings
  4. The biggest information blind spot (which missing information most affects the judgment)
```

### Step 5: Receive Reports and Track Progress

- Show the user a real-time progress table (which agents are done, which are still researching)
- For each report received, update progress and present that report's core points (3-5 items)
- Wait for all 6 reports to arrive

### Step 6: Cross-Validation and Information Assembly

**This is the most critical new step in the enhanced framework**. Before aggregating, the team-lead must:

1. **Data conflict arbitration**:
   - Extract key data from each agent's report
   - Identify whether the same data cited by different agents is consistent
   - Arbitrate conflicting data: list all sources, state which is adopted and why

2. **Signal consistency check**:
   - Do business-growth signals (business-decoder) vs. hiring signals (signal-miner) agree?
     (if business is said to be growing fast but hiring is shrinking, it needs explanation)
   - Does the tech-leadership narrative (tech-ip) get supported by patent/talent data (signal-miner)?
   - Does the valuation level (financial-detective) match the competitive position (competitive-mapper)?
   - Does management's public narrative (risk-governance) agree with actual action signals (signal-miner)?

3. **Information jigsaw reconstruction**:
   - Assemble the information fragments from the 6 reports to see if a more complete picture emerges
   - Mark the information "white zone" (confirmed known), "gray zone" (clues but uncertain), and "black zone" (entirely unknown)

4. **Anti-bias check**:
   - Check whether the report has a "detailed positive info, brief negative info" bias
   - Confirm that each positive judgment has a corresponding negative test

### Step 7: Compile the Final Report

Synthesize the 6 analysis reports and output a final report with the following structure:

---

#### 1. One-Sentence Conclusion
> In one paragraph (50-100 words), summarize the **true-value judgment** of this private company: what the business is worth, and why.

#### 2. Company Snapshot
| Item | Content | Confidence |
|------|------|--------|
| Company name | | |
| Founding year | | |
| Headquarters | | |
| Founder/CEO | | |
| Core business | | |
| Headcount | | |
| Latest valuation | | |
| Latest funding round | | |
| Estimated revenue scale | | |
| Estimated profitability status | | |
| Estimated user scale | | |
| Major investors | | |
| VIE/red-chip architecture | | |

#### 3. Six-Dimension Scoring Table
| Dimension | Analyst | Score (★1-5) | Core Judgment | Confidence | Information Completeness |
|------|--------|-----------|---------|--------|-----------|
| Business model & users | business-decoder | | | | |
| Financials & valuation | financial-detective | | | | |
| Industry & competition | competitive-mapper | | | | |
| Risk & governance | risk-governance-analyst | | | | |
| Technology & IP | tech-ip-analyst | | | | |
| Alternative-data signals | signal-miner | | | | |

Overall score: ★X / 5

#### 4. Key Data Jigsaw (after cross-validation)
Integrate the data assembled by each analyst, **keeping only cross-validated data**:

| Metric | Data | Number of Sources | Source Details | Confidence | Notes |
|------|------|---------|---------|--------|------|

#### 5. Signal Consistency Matrix
| Check Item | Signal A | Signal B | Consistency | Interpretation |
|--------|-------|-------|--------|------|
| Growth narrative vs. hiring trend | | | ✅/⚠️/❌ | |
| Tech-leadership narrative vs. patent data | | | | |
| Valuation level vs. competitive position | | | | |
| Management narrative vs. actual action | | | | |

#### 6. Per-Dimension Analysis Summary
Extract the 3-5 most important findings from each dimension (with source and confidence noted)

#### 7. True-Value Assessment

**Business-essence judgment**:
- What kind of business is this? (one sentence)
- How high is the "certainty" of this business?
- Duan Yongping-style judgment: is this a "right business"?

**Moat scorecard**:
| Moat Type | Score (★1-5) | Core Evidence | Trend | Durability |
|-----------|-----------|---------|------|--------|
| Network effects | | | Widening/Stable/Narrowing | |
| Switching costs | | | | |
| Brand mindshare | | | | |
| Data barrier | | | | |
| Regulatory license | | | | |
| Economies of scale | | | | |
| Technical barrier | | | | |

**Valuation judgment**:
| Valuation Method | Valuation Range | Confidence | Notes |
|---------|---------|--------|------|
| Latest funding valuation (adjusted) | | | |
| Comparable companies | | | |
| DCF scenario analysis | | | |
| End-state market-cap reverse-engineering | | | |
| Transaction comparables | | | |

**Integrated true-value range**:
- Conservative valuation (margin-of-safety value): $XXB
- Fair valuation (base-case assumptions): $XXB
- Optimistic valuation (best case): $XXB
- Current market valuation: $XXB
- **Margin of safety**: current valuation vs. conservative valuation = XX%

#### 8. Investment Thesis (Bull vs. Bear)
- 🟢 Bull logic (5-7 points, each with evidence source)
- 🔴 Bear logic (5-7 points, each with evidence source)
- ⚖️ Which side's arguments are more convincing? Why?

#### 9. Risk Matrix
| Risk | Probability | Impact | Overall Severity | Hedgeable? | Monitoring Metric |
|------|------|------|-----------|-----------|---------|

Top 3 core risks and mitigation strategies

#### 10. Exit Path Assessment
Most likely exit method, time window, expected return

#### 11. Investment Decision Table

**One-page decision table**:
```
┌──────────────────────────────────────────────┐
│  Company: XXX    Latest valuation: $XXB       │
│  Stage: [Seed/Growth/Mature/Pre-IPO]          │
│  Info completeness: [Sufficient/Adequate/Insufficient/Severely insufficient] │
├──────────────────────────────────────────────┤
│  Core investment logic (3 sentences max):     │
│  1. ________________________________________  │
│  2. ________________________________________  │
│  3. ________________________________________  │
├──────────────────────────────────────────────┤
│  True-value judgment:                         │
│  Fair valuation range: $XXB - $XXB            │
│  Current vs. fair valuation: Expensive/Fair/Cheap │
│  Margin of safety: ____%                       │
├──────────────────────────────────────────────┤
│  Key assumptions & validation methods:        │
│  Assumption1 → tracked metric → validation milestone → validation time │
│  Assumption2 → tracked metric → validation milestone → validation time │
│  Assumption3 → tracked metric → validation milestone → validation time │
├──────────────────────────────────────────────┤
│  Fatal risks & "thesis broken" signals:       │
│  Risk1 → if X happens, conclusion flips → stop-loss strategy │
│  Risk2 → if Y happens, conclusion flips → stop-loss strategy │
├──────────────────────────────────────────────┤
│  Conclusion: Invest / Watch / Avoid           │
│  If watch: what triggers a re-evaluation?     │
│  Expected exit: IPO / M&A / secondary transfer │
│  Expected return multiple: X - Y x            │
│  Expected time frame: X - Y years             │
│  Annualized return: X% - Y%                    │
└──────────────────────────────────────────────┘
```

**Tiered recommendations**:
| Investor Type | Recommendation | Reason |
|-----------|------|------|
| PE/VC firm (lead) | | |
| PE/VC firm (co-invest) | | |
| Secondary transfer | | |
| Buy after IPO | | |
| Not recommended to participate | | |

**Key catalysts**:
| Bull Catalyst | Estimated Time | Bear Catalyst | Estimated Time |
|-----------|---------|-----------|---------|
| | | | |

#### 12. Information Blind-Spot Map
| Dimension | Known Information | Missing Information | Impact of Missing | Acquisition Suggestion |
|------|---------|---------|---------|---------|

Do these blind spots affect the reliability of the core conclusion? If so, state clearly: "Given the missing X information, the confidence of the above conclusion is Y."

#### 13. Ongoing Tracking Checklist
| Tracking Item | Frequency | Source | Metric to Watch | Alert Threshold |
|---------|------|---------|---------|---------|

#### 14. Concluding Paragraph
150-250 words of final summary, including:
- The essence of this business
- True-value judgment
- Reasonableness of the current valuation
- The biggest certainty and uncertainty
- Final recommendation and core reasoning

---

### Step 8: Save the Report

Write the complete final report to `reports/{company_name}/{company_name}-private-{YYYYMMDD}.md`.

### Step 9: Clean Up the Team

Use TeamDelete to clean up team resources.

---

## Important Notes

1. **The 6 agents must launch in parallel**—call the Agent tool 6 times in the same message
2. **Data confidence annotation**—private-company data sources vary widely; every key data point must carry source and confidence
3. **Transparent estimation**—all estimation processes must show the calculation logic; no numbers out of thin air
4. **Cross-validation**—cross-validate key data with at least 2 sources; when sources conflict, list them all
5. **Signal consistency check**—the aggregation stage must perform a cross-dimension signal consistency check
6. **Clear conclusions**—don't shy away from giving an Invest/Watch/Avoid recommendation, but state the conclusion's confidence
7. **Patience**—the 6 agents' research takes a few minutes; update the user on progress in real time
8. **Chinese and English search**—private-company information may be spread across Chinese and English media; search in both languages
9. **Anti-bias core principle**—scarce data ≠ a bad company; short AI analysis ≠ low investment certainty. For companies with extremely scarce information, switch to "first-principles mode" to focus on core questions, without chasing report-format completeness
10. **Honest blanks**—clearly distinguish "evidence-based analysis" from "speculative filler" in the report; it is acceptable to state "data on this dimension is insufficient to draw a meaningful conclusion"
11. **Alternative data is not noise**—hiring, patents, litigation, app data, and other alternative data may be closer to the true operating reality than news coverage
12. **True-value orientation**—the ultimate goal is to judge what this business is worth, not to produce a good-looking report. If the information is insufficient for a reliable valuation, say directly "information insufficient, cannot give a reliable valuation"
