#!/usr/bin/env python3
"""
stock_screener.py — momentum discovery + value verification stock screen
Usage:
  python3 stock_screener.py                   # scan the entire watchlist
  python3 stock_screener.py NVDA TSLA GOOG    # scan specified targets
  python3 stock_screener.py --update MU       # update MU's fundamental data

Framework:
  Layer 1 (momentum discovery): 60-day high + volume confirmation → enter candidate pool
  Layer 2 (value verification): 6-dimension score >= 3/6 → buy signal
  Signal grades: 3/6 = probe 3% | 4/6 = standard 5% | 5-6/6 = conviction 8%

Improvements (from the NVDA/AMD/MU backtest):
  1. Gross margin improving for 2 consecutive quarters → independent buy condition (fixes NVDA 2023-01 miss)
  2. EPS beat > 30% → independent condition for cyclical stocks (fixes MU bottom signal)
  3. Signal grading replaces binary judgment
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from collections import OrderedDict

# ============================================================
# Configuration
# ============================================================

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FUND_FILE = os.path.join(DATA_DIR, "fundamentals.json")
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")

DEFAULT_WATCHLIST = {
    "us_ai_chip": ["NVDA", "AMD", "MU", "AVGO", "MRVL", "TSM"],
    "us_ai_app": ["GOOG", "META", "MSFT", "AMZN", "CRM", "NOW", "PLTR"],
    "us_ai_infra": ["ETN", "PWR", "VRT", "CRWV"],
    "us_crypto": ["COIN", "HOOD", "MSTR", "CRCL"],
    "hk_internet": ["0700.HK", "9888.HK", "1024.HK", "9992.HK"],
    "a_share": [],  # A-shares need a different data source, to be added later
}

# ============================================================
# Price data fetching (via curl to bypass Python SSL issues)
# ============================================================

def fetch_prices_curl(ticker, days=120):
    """Fetch Yahoo Finance daily data via curl"""
    end_ts = int(datetime.now().timestamp())
    start_ts = int((datetime.now() - timedelta(days=days)).timestamp())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={start_ts}&period2={end_ts}&interval=1d"
    )
    try:
        result = subprocess.run(
            ["curl", "-s", "-H", "User-Agent: Mozilla/5.0", url],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        chart = data.get("chart", {}).get("result", [{}])[0]
        timestamps = chart.get("timestamp", [])
        quote = chart.get("indicators", {}).get("quote", [{}])[0]
        rows = []
        for i, ts in enumerate(timestamps):
            c = quote.get("close", [None] * len(timestamps))[i]
            v = quote.get("volume", [None] * len(timestamps))[i]
            h = quote.get("high", [None] * len(timestamps))[i]
            if c and v and h:
                dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                rows.append({"date": dt, "close": c, "high": h, "volume": v})
        return rows if len(rows) > 60 else None
    except Exception as e:
        return None


# ============================================================
# Fundamental data management
# ============================================================

def load_fundamentals():
    """Load fundamental data"""
    if os.path.exists(FUND_FILE):
        with open(FUND_FILE) as f:
            return json.load(f)
    return {}


def save_fundamentals(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FUND_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_fundamental_interactive(ticker):
    """Interactively update fundamental data"""
    funds = load_fundamentals()
    if ticker not in funds:
        funds[ticker] = {"quarters": {}}
    print(f"\n  Updating {ticker} fundamental data")
    print(f"  Existing quarters: {', '.join(funds[ticker]['quarters'].keys()) or 'none'}")
    date = input("  Earnings release date (YYYY-MM-DD): ").strip()
    label = input("  Label (e.g. Q1 2024): ").strip()
    rev_yoy = float(input("  Revenue YoY growth (%): "))
    gm = float(input("  Gross margin (%): "))
    eps_beat = float(input("  EPS beat (%): "))

    funds[ticker]["quarters"][date] = {
        "label": label, "rev_yoy": rev_yoy, "gm": gm, "eps_beat": eps_beat
    }
    save_fundamentals(funds)
    print(f"  ✅ Saved {ticker} {label}")


# ============================================================
# Layer 1: momentum discovery
# ============================================================

def check_momentum(prices):
    """Check whether the latest trading day triggers a momentum signal"""
    if len(prices) < 61:
        return None

    latest = prices[-1]
    close = latest["close"]

    # 60-day high
    past_60_highs = [p["high"] for p in prices[-61:-1]]
    is_60d_high = close > max(past_60_highs)

    # Volume: 5-day avg volume > 20-day avg volume × 1.5
    vol_5 = sum(p["volume"] for p in prices[-5:]) / 5
    vol_20 = sum(p["volume"] for p in prices[-20:]) / 20
    vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 0
    is_volume = vol_ratio > 1.5

    # 30-day return
    close_30d = prices[-31]["close"] if len(prices) > 30 else prices[0]["close"]
    pct_30d = (close - close_30d) / close_30d * 100

    # A breakout day in the last 5 days (not necessarily today)
    recent_breakout = False
    for i in range(-5, 0):
        if prices[i]["close"] > max(p["high"] for p in prices[i-60:i]):
            recent_breakout = True
            break

    triggered = (is_60d_high or recent_breakout) and is_volume

    return {
        "triggered": triggered,
        "close": round(close, 2),
        "date": latest["date"],
        "is_60d_high": is_60d_high,
        "vol_ratio": round(vol_ratio, 2),
        "pct_30d": round(pct_30d, 1),
    }


# ============================================================
# Layer 2: value verification (6 dimensions, with backtest improvements)
# ============================================================

def check_value(ticker, signal_date=None):
    """6-dimension value verification"""
    funds = load_fundamentals()
    if ticker not in funds or not funds[ticker].get("quarters"):
        return None

    quarters = funds[ticker]["quarters"]
    sorted_q = sorted(quarters.items(), key=lambda x: x[0])

    # Find the most recent two quarters
    if signal_date:
        valid = [(d, q) for d, q in sorted_q if d <= signal_date]
    else:
        valid = sorted_q

    if not valid:
        return None

    latest = valid[-1]
    prev = valid[-2] if len(valid) >= 2 else None
    prev2 = valid[-3] if len(valid) >= 3 else None

    d = latest[1]
    pd = prev[1] if prev else None
    pd2 = prev2[1] if prev2 else None

    checks = {}

    # 1. Revenue acceleration (YoY growth improving)
    if pd:
        checks["营收加速"] = d["rev_yoy"] > pd["rev_yoy"]
    else:
        checks["营收加速"] = d["rev_yoy"] > 20

    # 2. Gross margin direction
    if pd:
        checks["毛利率扩张"] = d["gm"] > pd["gm"] or d["gm"] > 55
    else:
        checks["毛利率扩张"] = d["gm"] > 45

    # 3. EPS beat > 10%
    checks["盈利惊喜"] = d["eps_beat"] > 10

    # 4. Revenue high growth > 15%
    checks["营收高增长"] = d["rev_yoy"] > 15

    # 5. Gross margin healthy > 40%
    checks["毛利率健康"] = d["gm"] > 40

    # 6. ★Improvement: gross margin improving for 2 consecutive quarters (fixes NVDA 2023-01 miss)
    if pd and pd2:
        checks["毛利连续改善"] = d["gm"] > pd["gm"] > pd2["gm"]
    elif pd:
        checks["毛利连续改善"] = d["gm"] > pd["gm"]
    else:
        checks["毛利连续改善"] = False

    score = sum(1 for v in checks.values() if v)

    # ★Improvement: independent pass conditions
    independent_pass = False
    independent_reason = ""

    # Condition A: gross margin improving for 2 consecutive quarters + gross margin >45% (NVDA 2023-01 scenario)
    if checks.get("毛利连续改善") and d["gm"] > 45:
        independent_pass = True
        independent_reason = "gross margin improving consecutively + >45%"

    # Condition B: EPS beat > 30% (MU bottom scenario)
    if d["eps_beat"] > 30:
        independent_pass = True
        independent_reason = "EPS beat >30% (cyclical-stock signal)"

    return {
        "score": score,
        "max": 6,
        "checks": checks,
        "fund": d,
        "fund_date": latest[0],
        "fund_label": d.get("label", ""),
        "independent_pass": independent_pass,
        "independent_reason": independent_reason,
    }


# ============================================================
# Signal grading
# ============================================================

def grade_signal(momentum, value):
    """Composite grade"""
    if not momentum or not momentum["triggered"]:
        return "SKIP", "no momentum signal", ""

    if not value:
        return "WATCH", "momentum triggered but no fundamental data", "supplement fundamentals"

    score = value["score"]
    ind = value["independent_pass"]

    if score >= 5 or (score >= 4 and ind):
        return "BUY_8%", f"conviction ({score}/6)", "suggest 8% position"
    elif score >= 4 or (score >= 3 and ind):
        return "BUY_5%", f"standard ({score}/6)", "suggest 5% position"
    elif score >= 3:
        return "BUY_3%", f"probe ({score}/6)", "suggest 3% position"
    elif ind:
        return "BUY_3%", f"independent condition passed: {value['independent_reason']}", "suggest 3% position"
    else:
        return "PASS", f"momentum present but fundamentals insufficient ({score}/6)", "keep watching"


# ============================================================
# Scan a single target
# ============================================================

def scan_ticker(ticker, verbose=True):
    """Scan a single target"""
    prices = fetch_prices_curl(ticker)
    if not prices:
        if verbose:
            print(f"  {ticker:<8} ⚠️  could not fetch price data")
        return None

    momentum = check_momentum(prices)
    value = check_value(ticker)
    grade, reason, advice = grade_signal(momentum, value)

    result = {
        "ticker": ticker,
        "grade": grade,
        "reason": reason,
        "advice": advice,
        "momentum": momentum,
        "value": value,
    }

    if verbose:
        # compact output
        m = momentum
        symbol = {"BUY_8%": "🔴", "BUY_5%": "🟡", "BUY_3%": "🟢", "WATCH": "👀", "PASS": "⬜", "SKIP": "  "}
        s = symbol.get(grade, "  ")

        if grade.startswith("BUY"):
            print(f"  {s} {ticker:<8} ${m['close']:<8} 30-day +{m['pct_30d']}% volume {m['vol_ratio']}x  → {grade} {reason}")
            if value:
                v = value
                checks_str = " ".join(f"{'✅' if val else '❌'}{k}" for k, val in v["checks"].items())
                print(f"     Fundamentals ({v['fund_label']}): revenue {v['fund']['rev_yoy']}% gross margin {v['fund']['gm']}% EPS beat {v['fund']['eps_beat']}%")
                print(f"     {checks_str}")
                if v["independent_pass"]:
                    print(f"     ★Independent pass: {v['independent_reason']}")
        elif grade == "WATCH":
            print(f"  {s} {ticker:<8} ${m['close']:<8} 30-day +{m['pct_30d']}%  → momentum triggered! needs fundamental data")
        elif grade == "PASS":
            print(f"  {s} {ticker:<8} ${m['close']:<8}  → {reason}")
        # SKIP produces no output

    return result


# ============================================================
# Main program
# ============================================================

def main():
    args = sys.argv[1:]

    # Update mode
    if args and args[0] == "--update":
        ticker = args[1] if len(args) > 1 else input("  Ticker: ").strip().upper()
        update_fundamental_interactive(ticker)
        return

    # Initialize the default watchlist
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(DEFAULT_WATCHLIST, f, indent=2)
        print(f"  Created default watchlist: {WATCHLIST_FILE}")

    # Determine scan scope
    if args:
        tickers = [t.upper() for t in args]
    else:
        with open(WATCHLIST_FILE) as f:
            wl = json.load(f)
        tickers = []
        for group, syms in wl.items():
            tickers.extend(syms)

    # Run the scan
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'='*70}")
    print(f"  Momentum discovery + value verification stock screen  {today}")
    print(f"  Scan scope: {len(tickers)} targets")
    print(f"{'='*70}\n")

    buy_signals = []
    watch_signals = []

    for ticker in tickers:
        result = scan_ticker(ticker)
        if result:
            if result["grade"].startswith("BUY"):
                buy_signals.append(result)
            elif result["grade"] == "WATCH":
                watch_signals.append(result)

    # Summary
    print(f"\n{'='*70}")
    print(f"  📋 Scan results summary")
    print(f"{'='*70}")

    if buy_signals:
        print(f"\n  🎯 Buy signals: {len(buy_signals)}")
        for s in sorted(buy_signals, key=lambda x: x["grade"], reverse=True):
            m = s["momentum"]
            print(f"     {s['grade']:<8} {s['ticker']:<8} ${m['close']:<8} {s['reason']}")
    else:
        print(f"\n  No buy signals")

    if watch_signals:
        print(f"\n  👀 Watch (needs fundamentals): {len(watch_signals)}")
        for s in watch_signals:
            m = s["momentum"]
            print(f"     {s['ticker']:<8} ${m['close']:<8} 30-day +{m['pct_30d']}% — use --update {s['ticker']} to supplement")

    print(f"\n  Fundamental data file: {FUND_FILE}")
    print(f"  Watchlist file: {WATCHLIST_FILE}")
    print(f"  Use --update TICKER to add/update fundamentals\n")


if __name__ == "__main__":
    main()
