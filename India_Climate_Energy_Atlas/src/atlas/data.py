from __future__ import annotations
import time
from pathlib import Path
import requests
import pandas as pd

BASE_URL = "https://api.worldbank.org/v2"
INDICATORS = {
    "NY.GDP.PCAP.KD": "GDP per capita (constant 2015 US$)",
    "EN.ATM.CO2E.PC": "CO2 emissions (metric tons per capita)",
    "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
    "EG.FEC.RNEW.ZS": "Renewable energy consumption (% of total final energy consumption)",
    "SP.POP.TOTL": "Population, total",
    "EG.USE.ELEC.KH.PC": "Electric power consumption (kWh per capita)",
}
COUNTRIES = {
    "IND": "India",
    "BGD": "Bangladesh",
    "CHN": "China",
    "IDN": "Indonesia",
    "LKA": "Sri Lanka",
    "VNM": "Vietnam",
}

def fetch_indicator(indicator: str, countries: list[str], start: int, end: int,
                    session=requests, retries: int = 3) -> pd.DataFrame:
    """Fetch one indicator from the World Bank API with pagination and retries."""
    if indicator not in INDICATORS:
        raise ValueError(f"Unsupported indicator: {indicator}")
    if start > end:
        raise ValueError("start year must be <= end year")
    country_path = ";".join(countries)
    url = f"{BASE_URL}/country/{country_path}/indicator/{indicator}"
    params = {"date": f"{start}:{end}", "format": "json", "per_page": 20000}
    last_error = None
    for attempt in range(retries):
        try:
            response = session.get(url, params=params, timeout=45)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
                return pd.DataFrame(columns=["country_code", "country", "year", "indicator_code", "indicator", "value"])
            rows = []
            for item in payload[1]:
                rows.append({
                    "country_code": item.get("countryiso3code"),
                    "country": (item.get("country") or {}).get("value"),
                    "year": int(item["date"]),
                    "indicator_code": indicator,
                    "indicator": INDICATORS[indicator],
                    "value": item.get("value"),
                })
            return pd.DataFrame(rows)
        except Exception as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {indicator}: {last_error}") from last_error

def fetch_panel(start: int = 2000, end: int = 2023, countries: list[str] | None = None) -> pd.DataFrame:
    countries = countries or list(COUNTRIES)
    frames = []
    for indicator in INDICATORS:
        frames.append(fetch_indicator(indicator, countries, start, end))
    if not frames:
        return pd.DataFrame()
    long = pd.concat(frames, ignore_index=True)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    panel = long.pivot_table(
        index=["country_code", "country", "year"], columns="indicator_code",
        values="value", aggfunc="first"
    ).reset_index()
    panel.columns.name = None
    panel = panel.rename(columns=INDICATORS)
    return panel.sort_values(["country_code", "year"]).reset_index(drop=True)

def validate_panel(df: pd.DataFrame) -> pd.DataFrame:
    required = {"country_code", "country", "year"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns: {sorted(required - set(df.columns))}")
    out = df.copy()
    out["year"] = pd.to_numeric(out["year"], errors="raise").astype(int)
    out = out.drop_duplicates(["country_code", "year"]).sort_values(["country_code", "year"])
    return out.reset_index(drop=True)
