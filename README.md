# Global Labor Analysis

A map-led Streamlit explorer for studying unemployment rates, labor structure, and economic context across countries from 1991 to 2022.

## Live app

[Open the live Global Labor Analysis app](https://global-labor-analysis.streamlit.app/)

## About the app

The app pairs country-level unemployment on a world map with a selected-country sector snapshot. Use the year slider to compare reported unemployment across countries over time, and use the country selector to inspect agriculture, industry, and services shares for each year or move sequentially from country to country. The map uses a fixed color scale so the visual meaning of color stays consistent from year to year.

Unemployment remains the map's only color measure; sector shares are shown as descriptive context and are not used to rank countries or imply causality. GDP is nominal USD context only, and sector values are shares rather than employment counts. Observed relationships are descriptive associations, not causal conclusions.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

Run the repository smoke check with the project environment:

```powershell
python smoke_check.py
```

The app is ready for Streamlit Community Cloud deployment from the repository root. The CSV must remain beside `app.py`.

Version note: the current release uses a bolder, map-led visual direction with a selected-country sector snapshot, as documented in `AGENTS.md`.
