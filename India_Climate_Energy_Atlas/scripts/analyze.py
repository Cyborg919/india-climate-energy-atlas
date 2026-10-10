#!/usr/bin/env python3
"""Reproducible descriptive analysis of World Bank country-year indicator data."""
import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from atlas.analysis import coverage_table, trend_summary, correlation_within_country, GDP, CO2, RENEWABLES, ELECTRICITY

def main():
    data_path = ROOT / "data" / "processed" / "world_bank_panel.csv"
    if not data_path.exists():
        raise SystemExit("Run `python scripts/fetch_data.py` first.")
    df = pd.read_csv(data_path)
    reports = ROOT / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    coverage_table(df).to_csv(reports / "coverage.csv", index=False)
    metrics = [m for m in [GDP, CO2, RENEWABLES, ELECTRICITY] if m in df.columns]
    summary = {
        "dataset_rows": int(len(df)),
        "countries": sorted(df["country_code"].dropna().unique().tolist()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "indicator_coverage": coverage_table(df).to_dict(orient="records"),
        "india_trends": [trend_summary(df, metric) for metric in metrics],
        "india_gdp_co2_correlation": correlation_within_country(df, GDP, CO2) if GDP in df and CO2 in df else None,
        "sensitivity": {},
        "interpretation_warning": "Descriptive trends/correlations do not establish causation."
    }
    # Sensitivity: correlation only on the shared, complete observation years.
    if GDP in df and CO2 in df:
        india = df[df["country_code"] == "IND"][["year", GDP, CO2]].dropna().sort_values("year")
        if len(india) >= 3:
            summary["sensitivity"]["india_gdp_co2_complete_years"] = {
                "n": int(len(india)), "first_year": int(india.year.min()), "last_year": int(india.year.max()),
                "pearson_r": float(india[GDP].corr(india[CO2])),
                "spearman_r": float(india[GDP].corr(india[CO2], method="spearman")),
                "note": "Both correlations use only years where both indicators are observed. Neither is causal."
            }
        else:
            summary["sensitivity"]["india_gdp_co2_complete_years"] = {
                "n": int(len(india)), "note": "Insufficient complete years for a meaningful correlation."
            }
    # Common-year panel to avoid comparing countries over different time windows.
    if metrics:
        complete = df[["country_code", "country", "year"] + metrics].dropna(subset=metrics)
        if not complete.empty:
            common_start = int(complete["year"].min())
            common_end = int(complete["year"].max())
            summary["sensitivity"]["all_metrics_complete_case"] = {
                "rows": int(len(complete)), "first_year": common_start, "last_year": common_end,
                "note": "Complete cases across all selected metrics; this can strongly reduce coverage and may select a non-representative subset."
            }
    (reports / "analysis_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False))
    print(json.dumps(summary, indent=2, allow_nan=False))
    print(f"\nReports saved under: {reports}")

if __name__ == "__main__":
    main()
