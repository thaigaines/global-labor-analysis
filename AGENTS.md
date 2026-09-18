# Global Labor Analysis

## Mission

- Build a portfolio-quality global labor-structure explorer from `Employment_Unemployment_GDP_data.csv`.
- Make unemployment the geographic anchor and agriculture, industry, and services the temporal story.
- Explain change over time clearly, without implying causality, forecasts, rankings, or employment counts.

## Product contract

- Keep one Streamlit page with this visual order: global snapshot map, year slider below the map, country selector, sector bar chart.
- The slider controls both the map year and the selected-country sector snapshot. Keep the exact 1991–2022 range.
- Keep the globe recognizable and primary. Use bold type, asymmetry, vivid sector colors, and strong section rhythm while keeping values legible.
- Show honest no-data states. Sector values are percentages or shares, GDP is nominal USD, and country coverage varies by year.
- Keep the Kaggle source link and the small project credit visible in the page metadata or footer.

## Engineering guardrails

- Preserve the country × year data model and local CSV seam. Keep dependencies to `streamlit`, `pandas`, and `plotly` unless a documented decision adds one.
- Keep `load_data`, `prepare_map_data`, `build_unemployment_map`, `prepare_sector_snapshot`, and `build_sector_snapshot` small and testable.
- Prefer native Streamlit and Plotly. Add concise comments only where they explain a non-obvious stakeholder-facing decision; do not narrate obvious code.
- Refactor redundant code when touching a file, but keep changes local and behavior-focused.

## Team workflow

- Creative direction owns visual hierarchy and attention. The architect owns simplicity, comments, and refactoring. The technical lead verifies behavior and runtime evidence. The manager audits the final diff.
- After each meaningful adjustment, have the architect re-check the affected code and have the relevant domain lead audit it. Use grilling when a product decision is ambiguous and record the decision, not the debate.
- Run `python smoke_check.py`, `python -m py_compile app.py`, and `git diff --check` before handoff. A manager approval is required before any push or deployment.

## Completion

- The app starts from the repository root, reaches both slider endpoints, updates the map and sector chart together, and preserves honest missing values.
- The final working tree is minimal, commented where useful, visually intentional, and manager-approved with runtime evidence.
