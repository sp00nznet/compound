# Compound — daily unattended refresh (Windows).
# Re-prices saved holdings and regenerates the dashboard. Scheduled via Task Scheduler.
# Disable anytime:  Unregister-ScheduledTask -TaskName "Compound-Daily-Portfolio" -Confirm:$false
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
New-Item -ItemType Directory -Force -Path (Join-Path $repo "logs") | Out-Null
$log = Join-Path $repo ("logs\daily-{0}.log" -f (Get-Date -Format "yyyyMMdd"))

$prompt = @'
Run /compound in DAILY mode. Steps:
1. Read reports/private/holdings.txt for the portfolio.
2. Re-price each holding via web search (current price only — do NOT re-run the deep 4-master research).
3. Recompute weights and re-flag any call the new prices change (TRIM target hit, new 52-week extreme, concentration threshold crossed).
4. Regenerate reports/private/dashboard.html with the refreshed numbers.
5. Prepend ONE dated entry to the "Daily suggestions" log noting what moved today.
Follow skills/compound.md. This is read-only analysis, never a trade.
'@

& claude -p $prompt --permission-mode bypassPermissions *>> $log
"`n[done $(Get-Date -Format s)]" | Out-File -Append -Encoding utf8 $log
