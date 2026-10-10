# Upgrade notes

## What changed
- Reworked Streamlit app with an executive header, KPI cards, year-range control, overview/comparison/relationships/data-quality tabs.
- Added endpoint-change table, scatter plots, exploratory correlation matrix, coverage chart, provenance view and CSV download.
- Expanded `scripts/analyze.py` to write `reports/coverage.csv` and `reports/analysis_summary.json`, including a complete-year GDP/CO2 sensitivity check.
- Rebuilt the research notebook around data audit, trends, complete-pair associations, country comparisons, report exports and a publication checklist.
- Kept the project real-data-only. No demo or synthetic data are inserted when source data are absent.

## Update an existing local checkout
Back up your current project folder first, then copy the upgraded project files over it. Keep `data/processed/world_bank_panel.csv` if you already downloaded it. Reinstall dependencies only if needed:
```bash
python3 -m pip install -r requirements.txt
python3 scripts/analyze.py
python3 -m streamlit run app.py
```
For a clean data refresh:
```bash
python3 scripts/fetch_data.py --start 2000 --end 2023
python3 scripts/analyze.py
```

## Validation note
This package's analysis tests cover core helper functions. Run `pytest -q` from the project root. The app's visual appearance and live API connectivity should also be checked locally.
