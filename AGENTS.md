# Global Labor Analysis

## Product

- Build a clear, portfolio-quality global labor-structure explorer from `Employment_Unemployment_GDP_data.csv`.
- Tell a truthful story over time: the year slider controls the unemployment map and the selected-country sector snapshot.
- Preserve one Streamlit page in this order: year slider, dominant world map, country selector, sector bar chart.
- Unemployment is the map's color measure. Agriculture, industry, and services are the approved sector measures and are employment shares, not employment counts.
- The sector bar chart shows the selected country's values for the selected year. Keep the fixed 1991–2022 range, exact values, and visible no-data states.
- Treat the map as the primary attention anchor. Use bold typography, asymmetric spacing, vivid sector colors, and clear section rhythm to create visual impact without obscuring data.

## Truth and scope

- Preserve the country × year data model and the local CSV seam.
- Keep the map color range fixed at 0–20%; retain raw unemployment values in tooltips.
- GDP is nominal USD. Country coverage varies by year. Sector values are shares.
- Use descriptive language only. Do not rank countries, infer causality, forecast, normalize, or weight sector values without an explicit product decision and supporting data.
- Keep dependencies to `streamlit`, `pandas`, and `plotly` unless a written decision justifies another one.

## Code and review

- Keep `load_data`, `prepare_map_data`, `build_unemployment_map`, `prepare_sector_snapshot`, and `build_sector_snapshot` small, focused test seams.
- Prefer native Streamlit elements and Plotly. Keep the implementation local and readable; refactor only when it improves locality or testability.
- Creative direction owns visual hierarchy and attention. The technical lead coordinates behavior and verification. The architect checks each meaningful change for simplicity and scope. The manager audits the final diff and runtime evidence.
- Use the grilling workflow for team alignment when a product decision is ambiguous. Record the resulting decision here, not a debate transcript.

## Done means

- `python smoke_check.py` passes in the project environment.
- The app starts from the repository root, the slider reaches 1991 and 2022, the map updates, the selector changes the bar chart, and missing values remain honest.
- A final manager audit approves the working tree before any push or deployment.
