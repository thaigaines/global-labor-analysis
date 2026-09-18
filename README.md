# Global Labor Analysis

A focused Streamlit map for exploring unemployment rates and employment-sector context across countries from 1991 to 2022.

## Live app

[Open the live Global Labor Analysis app](https://global-labor-analysis.streamlit.app/)

## About the app

The app pairs country-level unemployment on a world map with a selected-country history of agriculture, industry, and services shares. Use the year slider to compare reported unemployment across countries over time, and use the country selector to inspect sector shifts from 1991 to 2022. The map uses a fixed color scale so the visual meaning of color stays consistent from year to year.

Unemployment remains the map's only color measure; sector shares are shown as descriptive country history and are not used to rank countries or imply causality. GDP is nominal USD, and sector values are shares rather than employment counts.

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

Version note: the current release uses the dark editorial visual direction documented in `AGENTS.md`.
