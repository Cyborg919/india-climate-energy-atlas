import pandas as pd
from src.atlas.analysis import coverage_table, trend_summary, correlation_within_country

METRIC = "GDP per capita (constant 2015 US$)"

def sample():
    return pd.DataFrame({
        "country_code": ["IND", "IND", "IND", "BGD"],
        "country": ["India", "India", "India", "Bangladesh"],
        "year": [2000, 2001, 2002, 2000],
        METRIC: [100.0, 110.0, 120.0, 80.0],
        "CO2 emissions (metric tons per capita)": [1.0, 1.1, 1.2, 0.5],
    })

def test_trend_summary_uses_observed_endpoints():
    out = trend_summary(sample(), METRIC)
    assert out["start_year"] == 2000
    assert out["end_year"] == 2002
    assert round(out["change_pct"], 1) == 20.0

def test_correlation_reports_sample_size_and_caveat():
    df = sample()
    out = correlation_within_country(df, METRIC, "CO2 emissions (metric tons per capita)")
    assert out["n"] == 3
    assert "does not establish causation" in out["note"]

def test_coverage_table_counts_missing():
    df = sample()
    df.loc[0, METRIC] = None
    out = coverage_table(df)
    row = out.loc[out["indicator"] == METRIC].iloc[0]
    assert row["missing"] == 1
