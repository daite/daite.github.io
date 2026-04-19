"""
fetch_jma.py
------------
Fetch daily maximum temperature (最高気温) for the Japan summer season
(June–September) from JMA's ETRN portal.

Usage:
    python fetch_jma.py

Output:
    CSV to stdout, one row per day:
        year,month,day,station,max_temp_c

No third-party dependencies — stdlib only (urllib, html.parser, csv).

JMA ETRN URL pattern (main stations, daily_s1):
    https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php
        ?prec_no=<prefecture_code>
        &block_no=<station_code>
        &year=<year>
        &month=<month>
        &day=
        &view=

Column order in data <td> cells (0-indexed):
    0  日           day number
    1  現地気圧      local pressure (hPa)
    2  海面気圧      sea-level pressure (hPa)
    3  降水量合計    precipitation total (mm)
    4  降水最大1時間  max 1-hour precipitation
    5  降水最大10分   max 10-min precipitation
    6  気温平均      mean temperature (°C)
    7  気温最高      daily MAXIMUM temperature (°C)  ← target
    8  気温最低      daily minimum temperature (°C)
    ...
"""

import csv
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Stations used in the blog post
# ---------------------------------------------------------------------------
STATIONS = [
    {"name": "Tokyo",  "prec_no": 44, "block_no": 47662},
    {"name": "Osaka",  "prec_no": 62, "block_no": 47772},
    {"name": "Kofu",   "prec_no": 49, "block_no": 47638},
]

YEARS   = [2024, 2025]
MONTHS  = [6, 7, 8, 9]   # June – September

ETRN_URL = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php"
TARGET_COL = 7            # 0-indexed column for 気温最高 (daily maximum)
REQUEST_DELAY = 1.0       # seconds between requests (be polite to JMA servers)


# ---------------------------------------------------------------------------
# HTML parser
# ---------------------------------------------------------------------------
class DailyTableParser(HTMLParser):
    """
    Walk the HTML table on a JMA daily_s1 page and collect every <tr>
    as a list of stripped <td> text values.
    """

    def __init__(self):
        super().__init__()
        self._in_td   = False
        self._current_cell = []
        self._current_row  = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
        elif tag == "td":
            self._in_td = True
            self._current_cell = []

    def handle_endtag(self, tag):
        if tag == "td":
            self._in_td = False
            self._current_row.append("".join(self._current_cell).strip())
        elif tag == "tr":
            if self._current_row:
                self.rows.append(self._current_row[:])

    def handle_data(self, data):
        if self._in_td:
            self._current_cell.append(data)


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------
def fetch_html(prec_no: int, block_no: int, year: int, month: int) -> str:
    url = (
        f"{ETRN_URL}"
        f"?prec_no={prec_no}&block_no={block_no}"
        f"&year={year}&month={month}&day=&view="
    )
    req = urllib.request.Request(url, headers={"User-Agent": "fetch_jma/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_max_temps(html: str) -> list[tuple[int, float]]:
    """
    Return [(day, max_temp_c), ...] from a daily_s1 HTML page.
    Rows where the target cell is missing or non-numeric are skipped.
    """
    parser = DailyTableParser()
    parser.feed(html)

    results = []
    for row in parser.rows:
        if len(row) <= TARGET_COL:
            continue
        day_str  = row[0]
        temp_str = row[TARGET_COL]
        try:
            day  = int(day_str)
            temp = float(temp_str)
        except ValueError:
            continue   # header rows, blank cells, "--" placeholders
        results.append((day, temp))
    return results


def fetch_monthly(
    station_name: str,
    prec_no: int,
    block_no: int,
    year: int,
    month: int,
) -> list[dict]:
    """Fetch one station-month and return a list of row dicts."""
    try:
        html = fetch_html(prec_no, block_no, year, month)
    except urllib.error.URLError as exc:
        print(f"[WARN] {station_name} {year}-{month:02d}: {exc}", file=sys.stderr)
        return []

    rows = []
    for day, temp in parse_max_temps(html):
        rows.append({
            "year":         year,
            "month":        month,
            "day":          day,
            "station":      station_name,
            "max_temp_c":   temp,
        })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["year", "month", "day", "station", "max_temp_c"],
        lineterminator="\n",
    )
    writer.writeheader()

    total = len(STATIONS) * len(YEARS) * len(MONTHS)
    done  = 0

    for station in STATIONS:
        for year in YEARS:
            for month in MONTHS:
                done += 1
                print(
                    f"[{done}/{total}] fetching {station['name']} {year}-{month:02d} ...",
                    file=sys.stderr,
                )
                rows = fetch_monthly(
                    station["name"],
                    station["prec_no"],
                    station["block_no"],
                    year,
                    month,
                )
                writer.writerows(rows)
                time.sleep(REQUEST_DELAY)

    print("[done]", file=sys.stderr)


if __name__ == "__main__":
    main()
