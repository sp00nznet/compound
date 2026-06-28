#!/usr/bin/env python3
"""Normalize a brokerage/portfolio export (CSV, TSV, or XLSX) into the
Compound holdings format:  `TICKER SHARES [@ COST]`  (cash as `cash AMOUNT`).

Works on exports from Robinhood, Fidelity, Schwab, Vanguard, E*TRADE,
Empower/Personal Capital, and most money-management apps — it sniffs the header
for the symbol / quantity / cost columns rather than assuming one layout.

Zero external dependencies — stdlib only (csv, zipfile, xml).

    python tools/import_holdings.py statement.csv
    python tools/import_holdings.py portfolio.xlsx --out reports/private/holdings.txt
    python tools/import_holdings.py --demo      # self-check
"""
import argparse, csv, io, re, sys, zipfile
import xml.etree.ElementTree as ET

# Header aliases (lowercased, punctuation-stripped) → field.
SYMBOL = {"symbol", "ticker", "sym", "instrument", "security", "symbolcusip", "name"}
QTY    = {"quantity", "qty", "shares", "sharequantity", "quantityshares", "units", "shareqty"}
AVGC   = {"averagecost", "avgcost", "costpershare", "averagecostbasis", "purchaseprice",
          "avgprice", "averageprice", "unitcost", "costperunit"}
TOTC   = {"costbasis", "totalcost", "costbasistotal", "totalcostbasis"}
MKTVAL = {"marketvalue", "currentvalue", "value", "mktvalue", "marketvalueusd",
          "currentmarketvalue", "marketval"}

def _norm(h):  # normalize a header cell for matching
    return re.sub(r"[^a-z0-9]", "", (h or "").lower())

def _num(v):   # parse a money/number cell: strip $ , ( ) and spaces
    if v is None: return None
    s = str(v).strip().replace(",", "").replace("$", "").replace("%", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    if s in ("", "-", "--", "n/a", "na"): return None
    try:
        x = float(s)
        return -x if neg else x
    except ValueError:
        return None

# ---- XLSX (stdlib zip + xml) -------------------------------------------------
def _xlsx_rows(path):
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root:
                # concat all <t> text under this <si> (handles rich-text runs)
                shared.append("".join(t.text or "" for t in si.iter()
                                      if t.tag.endswith("}t")))
        sheets = sorted(n for n in z.namelist()
                        if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        if not sheets:
            return []
        root = ET.fromstring(z.read(sheets[0]))
        rows = []
        for row in root.iter():
            if not row.tag.endswith("}row"):
                continue
            cells = {}
            for c in row:
                if not c.tag.endswith("}c"):
                    continue
                ref = c.get("r", "")
                col = _col_idx("".join(ch for ch in ref if ch.isalpha()))
                t = c.get("t")
                val = None
                for child in c:
                    if child.tag.endswith("}v"):
                        val = child.text
                    elif child.tag.endswith("}is"):
                        val = "".join(x.text or "" for x in child.iter()
                                      if x.tag.endswith("}t"))
                if t == "s" and val is not None:
                    val = shared[int(val)]
                cells[col] = val
            width = (max(cells) + 1) if cells else 0
            rows.append([cells.get(i) for i in range(width)])
        return rows

def _col_idx(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1

# ---- CSV / TSV ---------------------------------------------------------------
def _csv_rows(path):
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(4096); f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel
        return [row for row in csv.reader(f, dialect)]

# ---- core --------------------------------------------------------------------
def normalize(rows):
    # find the header row (first row that maps a symbol AND a quantity column)
    hdr_i = col = None
    for i, row in enumerate(rows[:15]):
        norm = [_norm(c) for c in row]
        has_sym = any(n in SYMBOL for n in norm)
        has_qty = any(n in QTY for n in norm)
        if has_sym and has_qty:
            hdr_i, col = i, norm
            break
    if hdr_i is None:
        raise SystemExit("Could not find a header row with a symbol and a quantity "
                         "column. Export with column headers, or paste holdings manually.")

    def find(aliases):
        for j, n in enumerate(col):
            if n in aliases:
                return j
        return None
    si, qi = find(SYMBOL), find(QTY)
    ai, ti, mi = find(AVGC), find(TOTC), find(MKTVAL)

    def cell(row, idx):
        return _num(row[idx]) if idx is not None and idx < len(row) else None

    out = []
    for row in rows[hdr_i + 1:]:
        if si >= len(row):
            continue
        sym = (row[si] or "").strip().upper()
        if not sym:
            continue
        low = sym.lower()
        qty = _num(row[qi]) if qi is not None and qi < len(row) else None
        # cash / sweep lines — amount may live in total-cost, market-value, or qty
        if low in ("cash", "cash & sweep", "cash and sweep", "sweep", "money market"):
            amt = cell(row, ti) or cell(row, mi) or qty
            if amt:
                out.append(f"cash {amt:g}")
            continue
        # skip totals / non-tickers
        if low in ("total", "totals", "account total", "grand total") or " " in sym or len(sym) > 6:
            continue
        if not qty or qty <= 0:
            continue
        cost = _num(row[ai]) if ai is not None and ai < len(row) else None
        if cost is None and ti is not None and ti < len(row):
            tc = _num(row[ti])
            if tc:
                cost = tc / qty  # total cost basis → per share
        out.append(f"{sym} {qty:g}" + (f" @ {cost:g}" if cost else ""))
    return out

def load(path):
    rows = _xlsx_rows(path) if path.lower().endswith(".xlsx") else _csv_rows(path)
    return normalize(rows)

def demo():
    sample = ("Symbol,Description,Quantity,Average Cost,Market Value\n"
              "AAPL,Apple Inc,10,180.50,2835.00\n"
              "VOO,Vanguard 500,2,640,1340\n"
              "Cash,Cash & Sweep,,,500.25\n"
              "Total,,,,4675.25\n")
    rows = list(csv.reader(io.StringIO(sample)))
    got = normalize(rows)
    assert got == ["AAPL 10 @ 180.5", "VOO 2 @ 640", "cash 500.25"], got
    # total-cost-basis fallback: per-share = total / qty
    rows2 = list(csv.reader(io.StringIO("Ticker,Shares,Cost Basis\nMSFT,4,2000\n")))
    assert normalize(rows2) == ["MSFT 4 @ 500"], normalize(rows2)
    print("demo OK")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", nargs="?", help="CSV / TSV / XLSX export")
    ap.add_argument("--out", help="write holdings to this file instead of stdout")
    ap.add_argument("--demo", action="store_true", help="run self-check and exit")
    a = ap.parse_args()
    if a.demo:
        demo(); return
    if not a.file:
        ap.error("give a file path, or --demo")
    lines = load(a.file)
    text = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {len(lines)} holdings → {a.out}")
    else:
        sys.stdout.write(text)

if __name__ == "__main__":
    main()
