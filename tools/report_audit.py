#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

Data spot-check tool: sample 15% of the financial data points from a research
report, compare them against reliable sources, pass if they match, otherwise
reject and explain why.

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

Workflow (three steps):
  Step 1 — extract data points, randomly sample 15%:
    python3 tools/report_audit.py extract --report reports/xxx.md

  Step 2 — for each data point in the spot-check list, Claude fetches the value
            from a reliable source (macrotrends/stockanalysis/aastocks/eastmoney)
            and fills in fetched_value

  Step 3 — feed in the verification results, output a pass/reject verdict:
    python3 tools/report_audit.py verdict --results '[...]'

  One-step (extract + print the spot-check list only, no network verification):
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run
"""

import argparse
import json
import math
import os
import re
import sys
from decimal import Decimal, Context, ROUND_HALF_EVEN
from random import Random

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)

# ---------------------------------------------------------------------------
# Data point extraction: identify financial numbers in a Markdown report
# ---------------------------------------------------------------------------

# Match patterns: number + unit, with a context label in front
# Examples: 收入：1,239亿元, PE 18.8x, 毛利率 56%, market cap ~$5,670亿
_PATTERNS = [
    # percent
    (r'([\d,，\.]+)\s*%',                        '%',    'percent'),
    # 亿元 / 亿美元 / 亿港元 (hundred-million CNY/USD/HKD)
    (r'([\d,，\.]+)\s*亿(元|美元|港元|RMB|USD|HKD)?', '亿',    'hundred_million'),
    # multiple PE/PB/PS
    (r'([\d,，\.]+)\s*[xX倍]',                   'x',    'multiple'),
    # 万亿 (trillion)
    (r'([\d,，\.]+)\s*万亿',                      '万亿', 'trillion'),
    # USD absolute value (B/T)
    (r'\$\s*([\d,，\.]+)\s*([BMT亿])',             '$',    'usd_abs'),
    # plain integer (e.g. market cap, revenue, user count, appearing inside a | table cell)
    (r'\|\s*[~约]?\$?([\d,，\.]+)\s*\|',          '',     'table_num'),
]

_LABEL_RE = re.compile(
    r'(?P<label>[^\|\n：:]{2,25})[：:\s]+[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)

_TABLE_ROW_RE = re.compile(
    r'\|\s*(?P<label>[^|]{1,40})\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?\s*\|'
)


def _clean_num(s: str) -> float:
    """Convert a number string with commas / Chinese commas to a float."""
    s = s.replace(',', '').replace('，', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def _is_valid_label(label: str) -> bool:
    """Decide whether a label is a meaningful financial field name, filtering noise."""
    label = label.strip()
    # too short
    if len(label) < 2:
        return False
    # pure number or pure year
    if re.fullmatch(r'[\d\s年季度Q]+', label):
        return False
    # starts with a symbol / markdown marker
    if re.match(r'^[+\-\*#\|~\$>_`]', label):
        return False
    # contains markdown bold / code markers
    if '**' in label or '`' in label or '__' in label:
        return False
    # label is a pure change-percentage (e.g. +56%, -13% used alone as a label)
    if re.fullmatch(r'[+\-]?\d+(\.\d+)?%', label):
        return False
    # common meaningless labels
    _SKIP = {'来源', 'sources', 'source', '说明', '注意', '备注', '数据来源',
             'n/a', '—', '-', '/', '合计', 'total', '单位', '趋势'}
    if label.lower() in _SKIP:
        return False
    return True


# Two-column table row: | label | value unit |  (designed for KV tables in financial reports)
_KV_TABLE_RE = re.compile(
    r'^\|\s*(?P<label>[^|*\n]{2,40}?)\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*'
    r'(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT亿])?\s*[\|（\(]'
)

# Labeled KV line: label: value unit
_KV_LABEL_RE = re.compile(
    r'(?P<label>[一-龥A-Za-z][^\|\n：:*]{1,30})[：:]\s*[~约]?\$?'
    r'(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)


def _parse_md_tables(lines: list) -> list:
    """Parse all tables in the Markdown, return a list of (row_label, col_header, value, unit, lineno, raw)."""
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # detect a header row (contains | and is not a separator row)
        if '|' in line and not re.match(r'^\|[\-\s\|:]+\|$', line):
            headers_raw = [h.strip().strip('*_').strip() for h in line.split('|')]
            headers_raw = [h for h in headers_raw if h]
            # the next line should be a separator row
            if i + 1 < len(lines) and re.match(r'^\|[\-\s\|:]+\|$', lines[i+1].strip()):
                i += 2  # skip the separator row
                # read data rows
                while i < len(lines):
                    dline = lines[i].strip()
                    if not dline or not dline.startswith('|'):
                        break
                    cells = [c.strip().strip('*_~').strip() for c in dline.split('|')]
                    cells = [c for c in cells if c != '']
                    if len(cells) < 2:
                        i += 1
                        continue
                    row_label = cells[0]
                    for col_idx, cell in enumerate(cells[1:], start=1):
                        col_header = headers_raw[col_idx] if col_idx < len(headers_raw) else f'col{col_idx}'
                        # extract number + unit from the cell
                        m = re.search(
                            r'[~约]?\$?([\d,，\.]+)\s*(亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?',
                            cell
                        )
                        if m:
                            val = _clean_num(m.group(1))
                            unit = (m.group(2) or '').strip()
                            if val and val != 0 and val < 1e15:
                                results.append((row_label, col_header, val, unit, i + 1, dline))
                    i += 1
                continue
        i += 1
    return results


def extract_data_points(md_text: str) -> list:
    """Extract all recognizable financial data points from a Markdown report.

    Covers three structures:
      1. Multi-column Markdown tables (the main source): (row label + column header) → value
      2. KV lines with a colon: label: value unit
      3. Bold number lines: **value** unit

    Returns a list of dict:
      {id, label, reported_value, unit, raw_text, line_number}
    """
    points = []
    seen = set()

    def _add(label, val, unit, lineno, raw):
        label = re.sub(r'[\*_`]+', '', label).strip()
        if not _is_valid_label(label):
            return
        if val is None or val == 0 or val > 1e15:
            return
        # filter pure year / quarter
        if re.fullmatch(r'(20\d{2}|Q[1-4]|\d{4}\s*Q[1-4])', label.strip()):
            return
        key = f"{label}|{round(val,4)}|{unit}"
        if key in seen:
            return
        seen.add(key)
        points.append({
            'id': len(points) + 1,
            'label': label,
            'reported_value': val,
            'unit': unit,
            'raw_text': raw[:120],
            'line_number': lineno,
        })

    lines = md_text.split('\n')
    in_code = False

    # --- 1. Multi-column tables ---
    for row_label, col_header, val, unit, lineno, raw in _parse_md_tables(lines):
        # skip meaningless row labels
        if not _is_valid_label(row_label):
            continue
        # skip meaningless column headers (YoY growth columns are annotations, not data to verify)
        if col_header.upper() in ('YOY', 'YOY增速', '增速', '同比', '变化', '趋势', '说明', '备注'):
            continue
        # label = "row label · column header" (if the column header supplements the row label)
        if col_header and col_header != row_label:
            label = f"{row_label} · {col_header}"
        else:
            label = row_label
        _add(label, val, unit, lineno, raw)

    # --- 2. KV colon lines ---
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code or stripped.startswith('> ') or re.match(r'^#{1,6}\s', stripped):
            continue
        if '|' in stripped:
            continue  # tables already handled above

        for m in _KV_LABEL_RE.finditer(stripped):
            label = m.group('label')
            val = _clean_num(m.group('num'))
            unit = (m.group('unit') or '').strip()
            _add(label, val, unit, lineno, stripped)

    return points


def sample_points(points: list, ratio: float = 0.15, seed: int = None) -> list:
    """Randomly sample `ratio` of the data points, at least 3, at most 30."""
    n = max(3, min(30, math.ceil(len(points) * ratio)))
    n = min(n, len(points))
    rng = Random(seed)
    sampled = rng.sample(points, n)
    # sort by line number to ease manual comparison
    return sorted(sampled, key=lambda p: p['line_number'])


# ---------------------------------------------------------------------------
# Pass / reject verdict
# ---------------------------------------------------------------------------

_TOLERANCE = 0.01   # 1% tolerance


def _pct_diff(reported: float, fetched: float) -> float:
    """Relative deviation (absolute)."""
    if reported == 0:
        return 0.0 if fetched == 0 else float('inf')
    return abs(reported - fetched) / abs(reported)


def render_verdict(results: list, report_name: str = "") -> dict:
    """
    Output a pass/reject verdict based on the verification results.

    results: list of dict, each containing:
      - id, label, reported_value, unit, fetched_value, fetched_source
      - (optional) fetched_value2, fetched_source2   ← second source

    Returns:
      {
        'verdict': 'PASS' | 'FAIL',
        'pass_count': int,
        'fail_count': int,
        'total': int,
        'fail_items': [...],
        'summary': str,
      }
    """
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print('=' * 70)
    print(f'{BOLD}Report data spot-check — pass/reject verdict{RESET}')
    if report_name:
        print(f'Report: {report_name}')
    print('=' * 70)
    print()

    fail_items = []
    warn_items = []

    for item in results:
        label = item.get('label', '?')
        reported = float(item.get('reported_value', 0))
        unit = item.get('unit', '')
        fetched = item.get('fetched_value')
        source = item.get('fetched_source', '?')
        fetched2 = item.get('fetched_value2')
        source2 = item.get('fetched_source2', '')

        # --- primary source comparison ---
        if fetched is None:
            # no verification value provided → skip (not counted as pass/fail)
            print(f'  ⬜ [{item["id"]:>2}] {label[:35]:35s} {reported:>12.2f} {unit}  →  [no verification value, skipped]')
            continue

        fetched = float(fetched)
        diff1 = _pct_diff(reported, fetched)

        # --- second source comparison (if any) ---
        diff2 = None
        if fetched2 is not None:
            fetched2 = float(fetched2)
            diff2 = _pct_diff(reported, fetched2)

        # judgment
        pass1 = diff1 <= _TOLERANCE
        pass2 = (diff2 is None) or (diff2 <= _TOLERANCE)

        if pass1 and pass2:
            status = f'{GREEN}✅ pass{RESET}'
            detail = f'{source}: {fetched:.2f} (deviation {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (deviation {diff2*100:.2f}%)'
        elif not pass1 and not pass2:
            status = f'{RED}❌ fail{RESET}'
            detail = f'{source}: {fetched:.2f} (deviation {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (deviation {diff2*100:.2f}%)'
            fail_items.append({
                'id': item['id'],
                'label': label,
                'reported': reported,
                'unit': unit,
                'fetched': fetched,
                'source': source,
                'fetched2': fetched2,
                'source2': source2,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
                'raw_text': item.get('raw_text', ''),
                'line_number': item.get('line_number', 0),
            })
        else:
            # one source passes, one fails → warning, not counted as a failure
            status = f'{YELLOW}⚠️  warning{RESET}'
            detail = f'{source}: {fetched:.2f} (deviation {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (deviation {diff2*100:.2f}%)'
            warn_items.append({
                'id': item['id'], 'label': label,
                'reported': reported, 'unit': unit,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
            })

        print(f'  {status} [{item["id"]:>2}] {label[:35]:35s}  reported: {reported:>12.2f} {unit}')
        print(f'              {" " * 38}{detail}')

    print()
    print('-' * 70)

    total = len([r for r in results if r.get('fetched_value') is not None])
    fail_count = len(fail_items)
    warn_count = len(warn_items)
    pass_count = total - fail_count - warn_count

    print(f'  Spot-checked: {total}  |  pass: {GREEN}{pass_count}{RESET}  |  warning: {YELLOW}{warn_count}{RESET}  |  fail: {RED}{fail_count}{RESET}')
    print()

    if fail_count == 0:
        print(f'{BOLD}{GREEN}[PASS] All spot-checked data passed, the report may be published.{RESET}')
        verdict = 'PASS'
    else:
        print(f'{BOLD}{RED}[REJECT] {fail_count} data point(s) failed verification, the report needs correction and re-review.{RESET}')
        print()
        print(f'{BOLD}Reasons for rejection:{RESET}')
        for fi in fail_items:
            print(f'  ❌ line {fi["line_number"]} | {fi["label"]}')
            print(f'     reported value: {fi["reported"]} {fi["unit"]}')
            print(f'     {fi["source"]}: {fi["fetched"]}  (deviation {fi["diff1_pct"]}%)')
            if fi.get('fetched2') is not None:
                print(f'     {fi["source2"]}: {fi["fetched2"]}  (deviation {fi["diff2_pct"]}%)')
            print(f'     original text: {fi["raw_text"][:80]}')
            print()
        verdict = 'FAIL'

    if warn_count > 0:
        print(f'{YELLOW}Note: {warn_count} data point(s) have inconsistent results across two sources (>1%), possibly a measurement-basis difference (GAAP/Non-GAAP or FX), please review manually.{RESET}')
        for wi in warn_items:
            print(f'  ⚠️  {wi["label"]}  reported:{wi["reported"]} {wi["unit"]}  deviation: {wi["diff1_pct"]}% / {wi["diff2_pct"]}%')

    print('=' * 70)

    return {
        'verdict': verdict,
        'pass_count': pass_count,
        'warn_count': warn_count,
        'fail_count': fail_count,
        'total': total,
        'fail_items': fail_items,
        'warn_items': warn_items,
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Report Audit Tool — research report data spot-check tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow:

  Step 1 — extract data points and randomly sample 15%, output the spot-check list:
    python3 tools/report_audit.py extract --report reports/腾讯/腾讯-research-20260408.md

  Step 2 — for each data point in the list, Claude fetches the value from a reliable
            source and fills in fetched_value / fetched_source / fetched_value2 / fetched_source2

  Step 3 — feed in the verification results, output a pass/reject verdict:
    python3 tools/report_audit.py verdict --results '[
      {"id":1,"label":"营业收入","reported_value":7518,"unit":"亿","fetched_value":7518,"fetched_source":"macrotrends","fetched_value2":7500,"fetched_source2":"stockanalysis"},
      ...
    ]'

  One-step preview (print the spot-check list only, no verification):
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run

  Specify the sampling ratio (default 0.15):
    python3 tools/report_audit.py extract --report reports/xxx.md --ratio 0.20

  Fix the random seed (reproduce the same sample batch):
    python3 tools/report_audit.py extract --report reports/xxx.md --seed 42
        """)

    sub = parser.add_subparsers(dest='command')

    # extract
    ext = sub.add_parser('extract', help='extract data points from a report and randomly sample')
    ext.add_argument('--report', required=True, help='report file path (Markdown)')
    ext.add_argument('--ratio', type=float, default=0.15, help='sampling ratio, default 0.15')
    ext.add_argument('--seed', type=int, default=None, help='random seed (optional, for reproducibility)')
    ext.add_argument('--dry-run', action='store_true', help='print only, do not output JSON')

    # verdict
    vrd = sub.add_parser('verdict', help='output a pass/reject verdict from the verification results')
    vrd.add_argument('--results', required=True, help='JSON array with fetched_value etc. fields')
    vrd.add_argument('--report', default='', help='report name (optional, for display)')
    vrd.add_argument('--output-json', action='store_true', help='output the verdict as JSON to stdout')

    args = parser.parse_args()

    if args.command == 'extract':
        if not os.path.exists(args.report):
            print(f'❌ File does not exist: {args.report}', file=sys.stderr)
            sys.exit(1)

        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()

        all_points = extract_data_points(text)
        sampled = sample_points(all_points, ratio=args.ratio, seed=args.seed)

        print('=' * 70)
        print(f'Report data spot-check list')
        print(f'File: {args.report}')
        print(f'Total data points extracted: {len(all_points)}  |  sampling ratio: {args.ratio:.0%}  |  spot-check count: {len(sampled)}')
        if args.seed is not None:
            print(f'Random seed: {args.seed} (can be used to reproduce the same sample batch)')
        print('=' * 70)
        print()
        print(f'{"ID":>3}  {"Line":>5}  {"Data label":<35}  {"Reported":>12}  {"Unit"}')
        print(f'{"─"*3}  {"─"*5}  {"─"*35}  {"─"*12}  {"─"*6}')
        for p in sampled:
            print(f'{p["id"]:>3}  {p["line_number"]:>5}  {p["label"][:35]:<35}  {p["reported_value"]:>12.2f}  {p["unit"]}')
        print()
        print('↑ For each data point above, fetch the value from the following sources and fill in fetched_value:')
        print('  US stocks: macrotrends.net (primary) + stockanalysis.com (secondary)')
        print('  HK stocks: aastocks.com (primary) + macrotrends ADR (secondary)')
        print('  A-shares:  eastmoney.com (primary) + cninfo.com.cn (secondary)')
        print()

        if not args.dry_run:
            # output a fillable JSON template
            template = []
            for p in sampled:
                template.append({
                    'id': p['id'],
                    'label': p['label'],
                    'reported_value': p['reported_value'],
                    'unit': p['unit'],
                    'line_number': p['line_number'],
                    'raw_text': p['raw_text'],
                    'fetched_value': None,       # ← fill in the primary-source verification value
                    'fetched_source': '',        # ← fill in the primary source name
                    'fetched_value2': None,      # ← fill in the secondary-source verification value (optional)
                    'fetched_source2': '',       # ← fill in the secondary source name (optional)
                })
            print('Spot-check list JSON (after filling in fetched_value, pass it to the verdict command):')
            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'verdict':
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError as e:
            print(f'❌ JSON parse failed: {e}', file=sys.stderr)
            sys.exit(1)

        report_name = args.report or ''
        outcome = render_verdict(results, report_name=report_name)

        if args.output_json:
            print(json.dumps(outcome, ensure_ascii=False, indent=2))

        # non-zero exit code means rejected, convenient for CI/scripts to detect
        sys.exit(0 if outcome['verdict'] == 'PASS' else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
