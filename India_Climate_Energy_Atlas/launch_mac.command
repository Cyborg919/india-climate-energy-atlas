#!/bin/bash
set -e
cd "$(dirname "$0")"
echo "India Climate & Energy Atlas"
echo "Project folder: $PWD"
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: Python 3 was not found. Install Python 3, then run this file again."
  read -r -p "Press Return to close..."
  exit 1
fi
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ ! -s "data/processed/world_bank_panel.csv" ]; then
  echo "Downloading real World Bank observations..."
  python scripts/fetch_data.py --start 2000 --end 2023
fi
python scripts/analyze.py
echo
echo "Launching dashboard. Keep this Terminal window open."
python -m streamlit run app.py
