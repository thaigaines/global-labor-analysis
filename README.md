# Global Labor Analysis

A minimal Streamlit map for exploring unemployment rates across countries from 1991 to 2022.

## Live app

[Open the live Global Labor Analysis app](https://global-labor-analysis.streamlit.app/)

## About the app

The app shows country level unemployment rates on a world map. Use the year slider to compare reported unemployment across countries over time. The map uses a fixed color scale so the visual meaning of color stays consistent from year to year.

The current interface keeps unemployment as the only exposed measure. A future structural labor phase may use the sector share fields in the source data.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The app is ready for Streamlit Community Cloud deployment from the repository root. The CSV must remain beside `app.py`.

Version note: the current release uses the dark editorial visual direction documented in `AGENTS.md`.
