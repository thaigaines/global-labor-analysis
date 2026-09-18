# Global Labor Analysis

## Product

- Build a one-page Streamlit explorer from `Employment_Unemployment_GDP_data.csv`.
- Use unemployment as the geographic anchor, agriculture/industry/services as the labor-structure story, and GDP as contextual evidence.
- Make the next analytical addition a selected-country unemployment trajectory across 1991–2022, with the shared year slider marking the current year.
- Show evidence for user interpretation: describe relationships as association, not causation; define calculations; never add a composite score.
- Preserve the 1991–2022 range, honest missing values, readable tooltips, the map-first hierarchy, source link, and project credit.
- Keep the trajectory on raw unemployment rates, show gaps for unavailable years, and keep sectors as the selected-year snapshot.

## Code

- Keep the country × year data seam and dependencies minimal: `streamlit`, `pandas`, and `plotly`.
- Keep `load_data`, `prepare_map_data`, `build_unemployment_map`, `prepare_sector_snapshot`, and `build_sector_snapshot` small and testable. Add a separate pure seam for country history rather than reshaping one year at a time.
- Prefer native Streamlit and Plotly. Add concise comments only for non-obvious decisions; refactor locally when it improves clarity or testability.

## Workflow

- Run `python smoke_check.py`, `python -m py_compile app.py`, and `git diff --check` before handoff.
- Treat review as a security gate: challenge scope and evidence, and block the push when approval is uncertain.
- Push only when the manager’s chat contains the standalone token `MANAGER_DECISION: APPROVE_PUSH`. A completed task without readable approval is a communication failure, not authorization.

## Done

- The app starts from the repository root, the year interaction updates dependent views, derived values are reproducible, missing data is explicit, checks pass, and manager approval is readable.
