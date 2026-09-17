# Global Labor Analysis

## v1 scope

- Deploy on Streamlit Community Cloud.
- Use Python with the smallest practical dependency set: `streamlit`, `pandas`, and `plotly`; add `pycountry` only if country-to-map matching requires it.
- Build one Streamlit page with one interactive world map and one year slider.
- Load `Employment_Unemployment_GDP_data.csv` locally from the project.
- Map one country/year measure at a time. The v1 default and primary focus is **unemployment rate (%)**. Keep the data loading and UI structure extensible for a future pivot toward structural analysis using sector shares, but do not build that pivot into v1. Do not make raw GDP the default because its scale is dominated by country size; if exposed later, label it clearly as nominal USD.

## Explicitly out of scope

Forecasting, authentication, databases, extra pages, user accounts, elaborate prose, custom backend services, and speculative derived metrics are not part of v1.

## Design decisions to preserve

- Favor a working, legible map over dashboard breadth or visual polish.
- Keep the data model at country × year. Do not imply causality, rankings, or forecasts.
- Surface the dataset's limitations briefly: GDP is nominal USD, country coverage may vary by year, and sector percentages are shares rather than employment counts.
- Treat v1 as an unemployment exploration tool with a deliberate seam for a later structural-labor phase; avoid premature sector comparisons, composite indices, or causal interpretation.

## Completion criteria

- A fresh Streamlit Community Cloud deployment starts from the repository root with a documented run command.
- The CSV loads without manual preprocessing, and the app handles an invalid/missing file with a concise user-facing error.
- The year slider spans 1991–2022 and changes the map data.
- The map renders country-level values with a legend, tooltip, and an understandable no-data treatment.
- At least one smoke check confirms the app imports/starts, the first and last years load, and a known country has a numeric value.
- No forecasting, authentication, database, extra page, or unnecessary dependency is introduced.
