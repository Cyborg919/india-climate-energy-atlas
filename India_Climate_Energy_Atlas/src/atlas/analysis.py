from __future__ import annotations
import numpy as np
import pandas as pd

GDP = "GDP per capita (constant 2015 US$)"
CO2 = "CO2 emissions (metric tons per capita)"
RENEWABLES = "Renewable energy consumption (% of total final energy consumption)"
ELECTRICITY = "Access to electricity (% of population)"

def coverage_table(df: pd.DataFrame) -> pd.DataFrame:
    id_cols = {"country_code", "country", "year"}
    metrics = [c for c in df.columns if c not in id_cols]
    rows = []
    for metric in metrics:
        s = df[metric]
        rows.append({"indicator": metric, "non_missing": int(s.notna().sum()),
                     "missing": int(s.isna().sum()),
                     "coverage_pct": round(float(s.notna().mean() * 100), 2) if len(s) else 0})
    return pd.DataFrame(rows).sort_values("coverage_pct", ascending=False)

def india_trends(df: pd.DataFrame) -> pd.DataFrame:
    india = df.loc[df["country_code"] == "IND"].sort_values("year").copy()
    if india.empty:
        return india
    for metric in [GDP, CO2, RENEWABLES, ELECTRICITY]:
        if metric in india:
            india[f"{metric}__pct_change"] = india[metric].pct_change(fill_method=None) * 100
    return india

def correlation_within_country(df: pd.DataFrame, x: str, y: str, country_code: str = "IND") -> dict:
    subset = df.loc[df["country_code"] == country_code, [x, y]].dropna()
    if len(subset) < 3:
        return {"n": int(len(subset)), "correlation": None, "note": "At least 3 complete observations are required."}
    return {"n": int(len(subset)), "correlation": float(subset[x].corr(subset[y])),
            "note": "Descriptive correlation only; it does not establish causation."}

def trend_summary(df: pd.DataFrame, metric: str, country_code: str = "IND") -> dict:
    subset = df.loc[df["country_code"] == country_code, ["year", metric]].dropna().sort_values("year")
    if subset.empty:
        return {"metric": metric, "start_year": None, "end_year": None, "start_value": None, "end_value": None, "change_pct": None}
    first, last = subset.iloc[0], subset.iloc[-1]
    change = None
    if first[metric] != 0:
        change = float((last[metric] / first[metric] - 1) * 100)
    return {"metric": metric, "start_year": int(first["year"]), "end_year": int(last["year"]),
            "start_value": float(first[metric]), "end_value": float(last[metric]), "change_pct": change}
