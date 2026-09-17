# Global Labor Analysis

A minimal Streamlit map for exploring unemployment rates across countries from 1991–2022.

## v2 visual direction

The app keeps the v1 interaction model—one map and one year slider—while moving toward a dark editorial presentation inspired by the portfolio site: dark navy canvas, aqua accent, spacious hierarchy, restrained metadata, and the map as the visual anchor. Unemployment remains the only exposed measure; structural sector analysis is reserved for a later phase.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The app is ready for Streamlit Community Cloud deployment from the repository root. The CSV must remain beside `app.py`.
