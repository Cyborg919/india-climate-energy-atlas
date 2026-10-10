# India Climate & Energy Atlas
**A reproducible data-science project using real World Bank indicator data.**

This project explores India's long-run development and energy transition using the World Bank Indicators API. It is designed as a portfolio-quality project: reproducible downloads, data validation, transparent missingness, exploratory analysis, an interactive dashboard, and a notebook-friendly research workflow.

## Research questions
1. How have India's GDP per capita, electricity access, renewable energy share, and CO₂ emissions changed over time?
2. Do changes in energy indicators move alongside changes in economic output?
3. How does India compare with selected peers (Bangladesh, China, Indonesia, Sri Lanka, Vietnam)?
4. Which conclusions are supported by the observed data—and which cannot be inferred from these indicators alone?

## Data source
- World Bank Indicators API: https://api.worldbank.org/v2/
- Indicator definitions: https://data.worldbank.org/indicator
- API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

The project fetches observations live from the public API. No API key is required. Exact data availability varies by indicator and year; the app shows missing values rather than fabricating them.

### Indicators
| Code | Indicator |
|---|---|
| `NY.GDP.PCAP.KD` | GDP per capita (constant 2015 US$) |
| `EN.ATM.CO2E.PC` | CO₂ emissions (metric tons per capita) |
| `EG.ELC.ACCS.ZS` | Access to electricity (% of population) |
| `EG.FEC.RNEW.ZS` | Renewable energy consumption (% of total final energy consumption) |
| `SP.POP.TOTL` | Population, total |
| `EG.USE.ELEC.KH.PC` | Electric power consumption (kWh per capita) |

Some indicators may have a publication lag or incomplete country-year coverage. Do not treat missing values as zero.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/fetch_data.py --start 2000 --end 2023
python scripts/analyze.py
python -m streamlit run app.py
```

The scripts cache API responses under `data/raw/` and write cleaned data to `data/processed/`. The first run requires internet access.

## Upgraded dashboard and analysis
The Streamlit app now includes:
- executive KPI cards and endpoint-change summaries;
- a selectable year range and country comparison table;
- pairwise scatter plots and exploratory correlation matrices;
- indicator coverage/missingness charts;
- a CSV download of the panel and provenance display.

The analysis script additionally exports coverage and a JSON summary with a complete-year sensitivity check for GDP per capita versus CO₂ emissions. Correlations are explicitly descriptive and must not be presented as causal results.

## Project layout
```text
India_Climate_Energy_Atlas/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  # API downloads, created on first run
│   └── processed/            # cleaned panel, created on first run
├── docs/
│   ├── DATA_DICTIONARY.md
│   └── RESEARCH_PROTOCOL.md
├── notebooks/
│   └── India_Climate_Energy_Atlas.ipynb
├── scripts/
│   ├── fetch_data.py
│   └── analyze.py
├── src/atlas/
│   ├── __init__.py
│   ├── data.py
│   └── analysis.py
└── tests/
    └── test_analysis.py
```

## Important scientific limits
- This is observational, country-level data, not a causal study.
- CO₂ emissions per capita are not a complete measure of all environmental impact.
- Renewable energy consumption and renewable electricity generation are different indicators.
- A correlation between GDP and emissions does not establish that one caused the other.
- World Bank series can be revised; record the retrieval date and cite the source in any publication.
- This project does **not** claim that India has achieved emissions decoupling. That must be tested from the downloaded data, with the selected years and indicator definitions stated clearly.

## Publish responsibly
1. Run the fetch and analysis scripts.
2. Inspect `reports/analysis_summary.json` and every plot.
3. Add the actual retrieval date and data coverage to your write-up.
4. Explain limitations and missingness.
5. Never claim model accuracy or scientific discoveries that the results do not support.


## Direct-upload options

### Kaggle notebook
Upload `notebooks/India_Climate_Energy_Atlas_Kaggle.ipynb` as a Kaggle Notebook. Enable Internet in the notebook settings so it can query the official World Bank API. Run all cells from top to bottom; the notebook exports `earth_atlas_outputs/` containing the retrieved real-data panel, coverage table, and provenance metadata. The notebook deliberately errors rather than substituting synthetic data if the API is unavailable.

### GitHub / source-code archive
Upload the project files or the ZIP archive to GitHub. The repository includes the Streamlit app, a reproducible data fetcher, tests, research protocol, and the standalone Kaggle notebook.

### Run locally on macOS
Extract the ZIP, then double-click `launch_mac.command` (you may need to right-click and choose Open). It creates a virtual environment, installs dependencies, fetches data if the processed CSV is absent, runs analysis and launches the dashboard. An internet connection is required for first-time data retrieval.

**Important:** A ZIP is a source-code bundle, not itself an executable Kaggle notebook. For a Kaggle notebook upload, upload the `.ipynb` file inside `notebooks/`. No fake data or unverified performance claims are included.
