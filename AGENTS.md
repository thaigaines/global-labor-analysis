# Global Labor Analysis

## v2 scope

- Deploy on Streamlit Community Cloud.
- Use Python with the smallest practical dependency set: `streamlit`, `pandas`, and `plotly`; add `pycountry` only if country-to-map matching requires it.
- Preserve one Streamlit page with one interactive world map and one year slider.
- Load `Employment_Unemployment_GDP_data.csv` locally from the project.
- Keep **unemployment rate (%)** as the only exposed measure. Preserve the data seam for a separately approved structural-labor phase, but do not expose sector measures yet. Do not make raw GDP the default because its scale is dominated by country size.

## v2 visual direction

- Use a dark editorial system inspired by the portfolio reference: dark navy canvas, aqua accent, spacious composition, strong typographic hierarchy, thin visual separation, and restrained metadata.
- Keep the map as the visual anchor. Use subdued geography, a high-contrast continuous legend, and clear country tooltips.
- Styling is presentation only; do not imply causality, forecasts, or rankings.

## Explicitly out of scope

Forecasting, authentication, databases, extra pages, user accounts, rankings, extra measures, elaborate prose, custom backend services, and speculative derived metrics are not part of v2.

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
