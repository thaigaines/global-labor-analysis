# Global Labor Analysis

## Mission

- Build a polished global labor-structure explorer from `Employment_Unemployment_GDP_data.csv`.
- Help people form their own conclusions from unemployment, sector structure, and economic context.
- Tell a clear descriptive story over time while preserving seams for future datasets.

## Product direction

- Keep unemployment as the geographic anchor and agriculture, industry, and services as the labor-structure story.
- Use GDP as contextual evidence alongside the labor measures, not as a competing map or headline score.
- Prefer global and country-to-country patterns when the data supports them. Do not force a single-country narrative.
- Explain relationships cautiously with explicit association, not causation, language. The interface should expose evidence, not dictate a conclusion.
- Allow only transparent calculations with visible definitions, such as changes over time or clearly labeled percentage differences. Never create a composite score.
- Optimize this dataset for educational clarity and portfolio quality first. Preserve clean data and chart seams for later datasets.

## Product contract

- Keep one Streamlit page with the globe as the primary attention anchor, followed by the year control, country context, and sector story.
- Keep the exact 1991–2022 range, honest missing-value states, and readable tooltips.
- Treat sector fields as shares, GDP as nominal USD, and country coverage as variable by year.
- Keep the Kaggle source link and small project credit visible in page metadata or the footer.

## Engineering guardrails

- Preserve the country × year model and local CSV seam. Keep dependencies to `streamlit`, `pandas`, and `plotly` unless a documented decision adds one.
- Keep `load_data`, `prepare_map_data`, `build_unemployment_map`, `prepare_sector_snapshot`, and `build_sector_snapshot` small and testable.
- Prefer native Streamlit and Plotly. Add concise comments only for non-obvious stakeholder-facing decisions.
- Refactor redundant code when touching a file, keeping changes local, minimal, and behavior-focused.

## Team workflow

- Creative direction owns visual hierarchy and attention. Architecture owns simple seams and refactoring. Technical leadership owns data quality and runtime evidence. Management owns scope and final approval.
- For a new product decision, grill the assumptions, have the roles challenge one another, record the resolved direction here, and prepare the team for implementation.
- After each meaningful adjustment, recheck the affected code and have the relevant domain lead audit it.
- Run `python smoke_check.py`, `python -m py_compile app.py`, and `git diff --check` before handoff. Manager approval is required before any push or deployment.

## Completion

- The app starts from the repository root, the year interaction updates every dependent view, derived values are reproducible from visible definitions, and missing data remains explicit.
- The final tree is minimal, readable, visually intentional, and manager-approved with runtime evidence.
