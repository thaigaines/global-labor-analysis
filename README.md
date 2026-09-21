# Global Labor Analysis

A map-led Streamlit explorer for studying unemployment rates, labor structure, and economic context across countries from 1991 to 2022.

## Live app

[Open the live Global Labor Analysis app](https://global-labor-analysis.streamlit.app/)

## About the app

The year slider above the world map compares reported unemployment across countries. Choose a country to see its raw unemployment trajectory from 1991 to 2022, with the chosen year marked, plus a compact three-sector snapshot for that year. The fixed map scale caps color at 20% while tooltips retain higher raw rates. Missing years remain gaps in the trajectory.

Unemployment remains the map's only color measure; sector shares are descriptive context and are not used to rank countries or imply causality. GDP is nominal USD context only, and sector values are shares rather than employment counts. Observed relationships are associations, not causal conclusions.

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
