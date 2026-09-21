# Global Labor Analysis

## Product

- Maintain a one-page, map-first Streamlit explorer of `Employment_Unemployment_GDP_data.csv` for 1991–2022.
- Place the shared year slider with the map. The selected country shows raw unemployment history as the primary country view, with a selected-year guide; three compact horizontal bars compare that year's agriculture, industry, and services employment shares. Nominal GDP is context only.
- Preserve gaps and explicit missing states, a truthful 20%+ map color cap with raw-rate tooltips, the source link, and project credit. Describe relationships as association, not causation; define derived values and avoid composite scores.

## Code and verification

- Keep the country × year lookup and pure map, sector, and trajectory preparation/build functions testable. Use the existing `streamlit`, `pandas`, and `plotly` dependencies and native UI elements.
- Run `python smoke_check.py`, `python -m py_compile app.py`, and `git diff --check` before handoff, using the project environment when needed.

## Push gate

- Treat review as a security gate. Push only when the manager's chat contains the token `MANAGER_DECISION: APPROVE_PUSH`; completed work without approval remains unpushed.
