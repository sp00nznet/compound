# Compound Roadmap

## P0: Near-term (1-2 months)

### A-share data source integration
- Integrate free data sources such as akshare and East Money (Eastmoney)
- Cover A-share financial data, market quotes, and the Dragon-Tiger List (longhubang)
- No changes needed to existing Skills; just extend the data layer

## P1: Mid-term (3-6 months)

### HTML report output
- Add an HTML report format on top of Markdown
- Support dark mode, navigation bar, and chart visualization
- Improve report shareability and reading experience

### Multiple depth modes
- `lite`: 5-minute quick take, rapidly giving a valuation range and core conclusions
- `standard`: the current default mode, full multi-agent research
- `deep`: more cross-validation and historical analogies, institutional-grade depth

### Multi-stock side-by-side comparison
- Support head-to-head comparison of 2-4 stocks across the same dimensions
- Valuation benchmarking against peers in the same industry
- Output a comparison matrix and a recommendation on the best pick

## P2: Long-term (6 months+)

### Test coverage
- Add unit tests for core tools (financial_rigor.py, etc.)
- Add regression tests for Skill outputs
- Ensure iterations don't break existing functionality

### Portfolio-level analysis
- Portfolio health assessment
- Industry/geographic concentration analysis
- Correlation risk detection
