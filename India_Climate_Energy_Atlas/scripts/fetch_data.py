#!/usr/bin/env python3
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from atlas.data import fetch_panel, validate_panel

def main():
    parser = argparse.ArgumentParser(description="Download real World Bank indicator data.")
    parser.add_argument("--start", type=int, default=2000)
    parser.add_argument("--end", type=int, default=2023)
    parser.add_argument("--countries", nargs="+", default=["IND", "BGD", "CHN", "IDN", "LKA", "VNM"])
    args = parser.parse_args()
    raw_dir = ROOT / "data" / "raw"
    processed_dir = ROOT / "data" / "processed"
    reports_dir = ROOT / "reports"
    for d in [raw_dir, processed_dir, reports_dir]:
        d.mkdir(parents=True, exist_ok=True)
    print(f"Fetching real World Bank data for {args.countries}, {args.start}-{args.end}...")
    panel = validate_panel(fetch_panel(args.start, args.end, args.countries))
    if panel.empty:
        raise SystemExit("No rows returned. Check connectivity, API status, or year range.")
    raw_path = raw_dir / f"world_bank_panel_{args.start}_{args.end}.csv"
    out_path = processed_dir / "world_bank_panel.csv"
    panel.to_csv(raw_path, index=False)
    panel.to_csv(out_path, index=False)
    metadata = {
        "source": "World Bank Indicators API",
        "source_url": "https://api.worldbank.org/v2/",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "start_year": args.start, "end_year": args.end,
        "countries_requested": args.countries,
        "rows": int(len(panel)),
        "columns": list(panel.columns),
        "note": "Values are real API observations; missing values remain missing."
    }
    (reports_dir / "data_provenance.json").write_text(json.dumps(metadata, indent=2))
    print(f"Saved {len(panel):,} country-year rows to {out_path}")
    print("Missing values were not filled with zero.")
if __name__ == "__main__":
    main()
