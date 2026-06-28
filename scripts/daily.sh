#!/usr/bin/env bash
# Compound — daily unattended refresh (macOS/Linux).
# Re-prices saved holdings and regenerates the dashboard. Schedule via cron, e.g.:
#   0 8 * * *  /path/to/compound/scripts/daily.sh
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo"
mkdir -p "$repo/logs"
log="$repo/logs/daily-$(date +%Y%m%d).log"

prompt='Run /compound in DAILY mode. Steps:
1. Read reports/private/holdings.txt for the portfolio.
2. Re-price each holding via web search (current price only — do NOT re-run the deep 4-master research).
3. Recompute weights and re-flag any call the new prices change (TRIM target hit, new 52-week extreme, concentration threshold crossed).
4. Regenerate reports/private/dashboard.html with the refreshed numbers.
5. Prepend ONE dated entry to the "Daily suggestions" log noting what moved today.
Follow skills/compound.md. This is read-only analysis, never a trade.'

claude -p "$prompt" --permission-mode bypassPermissions >> "$log" 2>&1
echo "[done $(date -Iseconds)]" >> "$log"
