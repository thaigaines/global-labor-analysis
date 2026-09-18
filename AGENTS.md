# Global Labor Analysis

## Product

- Build a one-page Streamlit explorer from `Employment_Unemployment_GDP_data.csv`.
- Use unemployment as the geographic anchor, agriculture/industry/services as the labor-structure story, and GDP as contextual evidence.
- Show evidence for user interpretation: describe relationships as association, not causation; define calculations; never add a composite score.
- Preserve the 1991–2022 range, honest missing values, readable tooltips, the map-first hierarchy, source link, and project credit.

## Code

- Keep the country × year data seam and dependencies minimal: `streamlit`, `pandas`, and `plotly`.
- Keep `load_data`, `prepare_map_data`, `build_unemployment_map`, `prepare_sector_snapshot`, and `build_sector_snapshot` small and testable.
- Prefer native Streamlit and Plotly. Add concise comments only for non-obvious decisions; refactor locally when it improves clarity or testability.

## Workflow

- Run `python smoke_check.py`, `python -m py_compile app.py`, and `git diff --check` before handoff.
- Push only when the manager’s chat contains the standalone token `MANAGER_DECISION: APPROVE_PUSH`. A completed task without readable approval is a communication failure, not authorization.

## Done

- The app starts from the repository root, the year interaction updates dependent views, derived values are reproducible, missing data is explicit, checks pass, and manager approval is readable.
