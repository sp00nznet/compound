# Spec for Obtaining and Cross-Validating Financial Data

This spec applies to all research involving corporate financial data. **Every key data point must come from two independent sources; flag any discrepancy >1%.**

---

## Data-Source Priority

### US-listed (PDD, Tencent ADR, NetEase ADR, etc.)

| Priority | Source | URL | How to access |
|--------|------|-----|---------|
| 1 (primary) | **macrotrends** | macrotrends.net/stocks/charts/{ticker} | Direct access, no registration |
| 2 (secondary) | **stockanalysis** | stockanalysis.com/stocks/{ticker}/financials | Direct access, no registration |
| Raw primary | SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 10-K / 10-Q original text |

### HK-listed (Tencent 0700, NetEase 9999, Meituan 3690, etc.)

| Priority | Source | URL | How to access |
|--------|------|-----|---------|
| 1 (primary) | **aastocks** | aastocks.com/tc/stocks/analysis/company-fundamental | Direct access |
| 2 (secondary) | **macrotrends** (ADR ticker) | TCEHY for Tencent, NTES for NetEase | Direct access |
| Raw primary | HKEX Disclosure | hkexnews.hk | Annual-report PDF |

### A-shares (37 Interactive Entertainment, G-bits, etc.)

| Priority | Source | URL | How to access |
|--------|------|-----|---------|
| 1 (primary) | **Eastmoney** | eastmoney.com → search ticker → financial statements | Direct access |
| 2 (secondary) | **cninfo** | cninfo.com.cn | Original annual/quarterly PDFs |

---

## Execution Spec

### Step 1: Obtain the data

For each financial metric (revenue, net profit, gross margin, operating cash flow, debt ratio, etc.), pull the figure from **source 1** and **source 2** separately.

### Step 2: Compute and flag the discrepancy

```
discrepancy = |source1 − source2| / source1 × 100%
```

| Discrepancy | Handling |
|------|---------|
| ≤ 1% | ✅ consistent, use source 1's figure, cite both sources |
| 1% ~ 5% | ⚠️ flag "data discrepancy", note both figures, explain the likely cause (FX / accounting basis) |
| > 5% | ❌ flag "major data discrepancy", must verify against the original filing, do not use directly |

### Step 3: Data-presentation format

Every key data point must be labeled in the following format:

```
Revenue: ¥123.9B ✅
  - macrotrends: ¥124.1B
  - stockanalysis: ¥123.7B
  - discrepancy: 0.3%
```

Discrepancy example:
```
Net profit: ¥24.5B ⚠️ data discrepancy
  - macrotrends: ¥24.5B (GAAP)
  - stockanalysis: ¥27.8B (Non-GAAP)
  - discrepancy: 13.5% — cause: different accounting basis (GAAP vs Non-GAAP)
```

---

## Common Causes of Discrepancy (not necessarily data errors)

| Cause | Note |
|------|------|
| GAAP vs Non-GAAP | Most common, especially for profit metrics |
| FX conversion | Different timestamps for HKD/CNY/USD conversion |
| Fiscal-year definition | Calendar year vs fiscal year (e.g. Apple's fiscal year ends in October) |
| Consolidation basis | Whether minority interests are included |
| Data-update lag | A platform hasn't yet updated the latest period |

---

## Special Rules

1. **Unlisted companies** (miHoYo, Lilith, etc.): when only one primary source exists, prefix the data with `[estimate]` and skip cross-validation
2. **Quarterly vs annual data**: prefer annual data for cross-validation; some sources may lag on quarterly data
3. **Original filing takes precedence**: if both sources disagree with the original filing (10-K / annual-report PDF), the original filing prevails, and flag the source as erroneous

---

## Quick Index

| Case | Primary source | Backup source |
|------|---------|---------|
| PDD / Pinduoduo | macrotrends.net/stocks/charts/PDD | stockanalysis.com/stocks/pdd |
| Tencent | macrotrends.net/stocks/charts/TCEHY | aastocks (0700.HK) |
| NetEase | macrotrends.net/stocks/charts/NTES | aastocks (9999.HK) |
| 37 Interactive Entertainment | eastmoney.com (002555) | cninfo.com.cn |
| G-bits | eastmoney.com (603444) | cninfo.com.cn |
| Nintendo | macrotrends.net/stocks/charts/NTDOY | stockanalysis.com/stocks/ntdoy |
| Capcom | macrotrends (CCOEY) | stockanalysis (CCOEY) |
