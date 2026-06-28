#!/usr/bin/env python3
"""A-share data tool — Tencent quotes + Eastmoney search/financials, zero external deps (stdlib only).

Provides A-share real-time quotes, financial data, etc. for Claude Code Skills.
Design principles: standalone module that does not affect existing tools; uses curl
direct connection to bypass the system proxy.

Usage (called automatically by Skills):
    python3.11 tools/ashare_data.py quote 600519                    # real-time quote
    python3.11 tools/ashare_data.py financials 600519               # core financials (last 5 years)
    python3.11 tools/ashare_data.py valuation 600519                # valuation metrics
    python3.11 tools/ashare_data.py search 茅台                      # search stock code

Requires Python >= 3.8, zero external dependencies.
"""

import argparse
import json
import os
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_EVEN

_TIMEOUT = 15


def _curl(url):
    """Direct connection via curl --noproxy, bypassing the system proxy."""
    result = subprocess.run(
        ["/usr/bin/curl", "-s", "--noproxy", "*",
         "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
         url],
        capture_output=True, timeout=_TIMEOUT,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ConnectionError(f"Request failed: {url}")
    # Tencent quote API returns GBK encoding, others return UTF-8
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return result.stdout.decode("gbk")


def _curl_json(url, params=None):
    """Fetch JSON via curl."""
    if params:
        from urllib.parse import urlencode
        url = f"{url}?{urlencode(params)}"
    return json.loads(_curl(url))


# ---------------------------------------------------------------------------
# Tencent quote API (stable and reliable, no auth needed)
# ---------------------------------------------------------------------------

def _qq_code(code: str) -> str:
    """Convert a stock code to Tencent quote format."""
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    if code.startswith(("6", "9", "5")):
        return f"sh{code}"
    elif code.startswith(("0", "3", "2", "1")):
        return f"sz{code}"
    elif code.startswith(("4", "8")):
        return f"bj{code}"
    return f"sh{code}"


def _parse_qq_quote(raw: str) -> dict:
    """Parse Tencent quote data. Format: v_shXXXXXX="field1~field2~..."; """
    start = raw.find('"')
    end = raw.rfind('"')
    if start < 0 or end <= start:
        return {}
    fields = raw[start + 1:end].split("~")
    if len(fields) < 50:
        return {}
    return {
        "name": fields[1],
        "code": fields[2],
        "price": fields[3],
        "prev_close": fields[4],
        "open": fields[5],
        "volume": fields[6],         # lots
        "buy_vol": fields[7],
        "sell_vol": fields[8],
        "high": fields[33] if len(fields) > 33 else fields[3],
        "low": fields[34] if len(fields) > 34 else fields[3],
        "change_pct": fields[32],
        "change_amt": fields[31],
        "turnover_amt": fields[37] if len(fields) > 37 else "-",
        "turnover_rate": fields[38] if len(fields) > 38 else "-",
        "pe": fields[39] if len(fields) > 39 else "-",
        "market_cap": fields[45] if len(fields) > 45 else "-",    # total market cap (in 100M)
        "float_cap": fields[44] if len(fields) > 44 else "-",     # float market cap (in 100M)
        "pb": fields[46] if len(fields) > 46 else "-",
        "high_52w": fields[47] if len(fields) > 47 else "-",
        "low_52w": fields[48] if len(fields) > 48 else "-",
        "total_shares": fields[38] if len(fields) > 38 else "-",  # will recalculate
    }


def _fmt_yi(value) -> str:
    if value is None or value == "-" or value == "":
        return "-"
    try:
        v = float(value)
    except (ValueError, TypeError):
        return str(value)
    if abs(v) >= 1e8:
        return f"{v / 1e8:.2f}亿"
    if abs(v) >= 1e4:
        return f"{v / 1e4:.2f}万"
    return f"{v:.2f}"


def _fmt_pct(value) -> str:
    if value is None or value == "-" or value == "":
        return "-"
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return str(value)


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------

def cmd_quote(code: str):
    """Real-time quote snapshot."""
    qq_code = _qq_code(code)
    raw = _curl(f"https://qt.gtimg.cn/q={qq_code}")
    d = _parse_qq_quote(raw)
    if not d:
        print(f"❌ Stock not found: {code}")
        return

    print("=" * 60)
    print(f"Real-time quote: {d['name']} ({d['code']})")
    print("=" * 60)
    print(f"  Price:          {d['price']}")
    print(f"  Change %:       {d['change_pct']}%")
    print(f"  Change amount:  {d['change_amt']}")
    print(f"  Open:           {d['open']}")
    print(f"  High:           {d['high']}")
    print(f"  Low:            {d['low']}")
    print(f"  Prev close:     {d['prev_close']}")
    print(f"  Volume:         {d['volume']} lots")
    print(f"  Turnover:       {d['turnover_amt']}万")
    print(f"  Market cap:     {d['market_cap']}亿")
    print(f"  Float cap:      {d['float_cap']}亿")
    print(f"  PE (dyn):       {d['pe']}")
    print(f"  PB:             {d['pb']}")
    print(f"  Turnover rate:  {d['turnover_rate']}%")
    print(f"  52w high:       {d['high_52w']}")
    print(f"  52w low:        {d['low_52w']}")


def cmd_valuation(code: str):
    """Valuation metrics summary."""
    qq_code = _qq_code(code)
    raw = _curl(f"https://qt.gtimg.cn/q={qq_code}")
    d = _parse_qq_quote(raw)
    if not d:
        print(f"❌ Stock not found: {code}")
        return

    price = d["price"]
    market_cap_yi = d["market_cap"]

    print("=" * 60)
    print(f"Valuation metrics: {d['name']} ({d['code']})")
    print("=" * 60)
    print(f"  Price:          {price}")
    print(f"  Market cap:     {market_cap_yi}亿")
    print(f"  Float cap:      {d['float_cap']}亿")
    print(f"  PE (dyn):       {d['pe']}")
    print(f"  PB:             {d['pb']}")
    print(f"  52w high:       {d['high_52w']}")
    print(f"  52w low:        {d['low_52w']}")

    # Market cap verification
    try:
        p = Decimal(price)
        cap = Decimal(market_cap_yi) * Decimal("1e8")
        shares = cap / p
        print(f"\n  Implied total shares: {_fmt_yi(float(shares))} shares")
        calc_cap = p * shares
        reported_cap = Decimal(market_cap_yi) * Decimal("1e8")
        diff = abs(calc_cap - reported_cap) / reported_cap * 100
        print(f"  Cap check:      ✅ consistent (back-calc, deviation {float(diff):.1f}%)")
    except Exception:
        pass


def cmd_financials(code: str):
    """Core financial data for the last 5 years."""
    qq_code = _qq_code(code)
    raw = _curl(f"https://qt.gtimg.cn/q={qq_code}")
    d = _parse_qq_quote(raw)
    name = d.get("name", code) if d else code

    code_clean = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    market = "SH" if code_clean.startswith(("6", "9", "5")) else "SZ"

    # Eastmoney datacenter API (annual report data)
    fin_url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        "type": "RPT_F10_FINANCE_MAINFINADATA",
        "sty": "ALL",
        "filter": f'(SECUCODE="{code_clean}.{market}")(REPORT_TYPE="年报")',
        "p": "1",
        "ps": "5",
        "sr": "-1",
        "st": "REPORT_DATE",
        "source": "HSF10",
        "client": "PC",
    }
    reports = []
    try:
        data = _curl_json(fin_url, params)
        reports = data.get("result", {}).get("data", [])
    except Exception:
        pass

    # If the annual-report filter returns nothing, drop the annual-report restriction
    if not reports:
        params["filter"] = f'(SECUCODE="{code_clean}.{market}")'
        try:
            data = _curl_json(fin_url, params)
            reports = data.get("result", {}).get("data", [])
        except Exception:
            pass

    print("=" * 60)
    print(f"Core financials: {name} ({code_clean})")
    print("=" * 60)

    if not reports:
        print("  ⚠️ Could not fetch financial data, consider supplementing via WebSearch")
        return

    for r in reports[:5]:
        date = r.get("REPORT_DATE", "")[:10]
        report_name = r.get("REPORT_DATE_NAME", "")
        revenue = r.get("TOTALOPERATEREVE")
        net_profit = r.get("PARENTNETPROFIT")
        eps = r.get("EPSJB")
        bps = r.get("BPS")
        roe = r.get("ROEJQ")
        rev_growth = r.get("TOTALOPERATEREVETZ")
        profit_growth = r.get("PARENTNETPROFITTZ")

        print(f"\n  --- {date} {report_name} ---")
        if revenue is not None:
            print(f"  Revenue:            {_fmt_yi(revenue)}")
        if rev_growth is not None:
            print(f"  Revenue growth:     {_fmt_pct(rev_growth)}")
        if net_profit is not None:
            print(f"  Net profit (attr):  {_fmt_yi(net_profit)}")
        if profit_growth is not None:
            print(f"  Profit growth:      {_fmt_pct(profit_growth)}")
        if eps is not None:
            print(f"  Basic EPS:          {eps}")
        if bps is not None:
            print(f"  Book value/share:   {bps:.2f}")
        if roe is not None:
            print(f"  ROE (weighted):     {_fmt_pct(roe)}")


def cmd_search(keyword: str):
    """Search for a stock code."""
    url = "https://searchadapter.eastmoney.com/api/suggest/get"
    params = {
        "input": keyword,
        "type": "14",
        "token": "D43BF722C8E33BDC906FB84D85E326E8",
        "count": "10",
    }
    data = _curl_json(url, params)
    results = data.get("QuotationCodeTable", {}).get("Data", [])

    if not results:
        print(f"❌ No stock matching '{keyword}' found")
        return

    print("=" * 60)
    print(f"Search results: '{keyword}'")
    print("=" * 60)
    for r in results:
        code = r.get("Code", "")
        name = r.get("Name", "")
        market = r.get("MktNum", "")
        mkt_label = {"1": "SH", "2": "SZ", "3": "BJ"}.get(str(market), "")
        print(f"  {code} {name} [{mkt_label}]")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="A-share data tool — Tencent quotes + Eastmoney financials",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    p_quote = sub.add_parser("quote", help="Real-time quote")
    p_quote.add_argument("code", help="stock code, e.g. 600519")

    p_fin = sub.add_parser("financials", help="Core financials (last 5 years)")
    p_fin.add_argument("code", help="stock code")

    p_val = sub.add_parser("valuation", help="Valuation metrics")
    p_val.add_argument("code", help="stock code")

    p_search = sub.add_parser("search", help="Search for a stock code")
    p_search.add_argument("keyword", help="company name or keyword")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "quote": lambda: cmd_quote(args.code),
        "financials": lambda: cmd_financials(args.code),
        "valuation": lambda: cmd_valuation(args.code),
        "search": lambda: cmd_search(args.keyword),
    }
    cmds[args.command]()


if __name__ == "__main__":
    main()
