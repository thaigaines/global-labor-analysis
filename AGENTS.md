# Global Labor Analysis

## v4 scope

- Deploy on Streamlit Community Cloud.
- Use Python with the smallest practical dependency set: `streamlit`, `pandas`, and `plotly`; add `pycountry` only if country-to-map matching requires it.
- Preserve one Streamlit page with one interactive world map and one year slider.
- Load `Employment_Unemployment_GDP_data.csv` locally from the project.
- Keep **unemployment rate (%)** as the map's visual measure. Make the three source employment-sector fields—agriculture, industry, and services—a first-class descriptive view through a selected-country history. Do not create rankings, composite indices, or causal interpretations. Do not make raw GDP the default because its scale is dominated by country size.
- The map uses a fixed 0–20% visual color range. Values above 20% use the endpoint color, while tooltips retain the raw rate.

## v4 visual direction

- Use a quiet material/editorial system inspired by Google's clean visual discipline: dark navy canvas, aqua accent, spacious composition, strong typographic hierarchy, thin visual separation, restrained native metric cards, and clear interaction states. This is inspiration for clarity and rhythm, not literal Google branding.
- Keep the map as the visual anchor. Use subdued geography, a high-contrast continuous legend, and clear country tooltips.
- Keep the map visually dominant while adding a bold sector-history panel above it. Use a selected-country control, high-contrast sector colors, distinct line styles, direct hover values, and a same-measure table fallback so the page is engaging without becoming noisy.
- Styling is presentation only; do not imply causality, forecasts, or rankings.

## Explicitly out of scope

Forecasting, authentication, databases, extra pages, user accounts, rankings, composite indices, elaborate prose, custom backend services, and speculative derived metrics are not part of v4.

## Design decisions to preserve

- Favor a working, legible map over dashboard breadth; visual polish should improve orientation and comprehension rather than add noise.
- Keep the data model at country × year. Do not imply causality, rankings, or forecasts.
- Surface the dataset's limitations briefly: GDP is nominal USD, country coverage may vary by year, and sector percentages are shares rather than employment counts.
- Treat the app as a paired unemployment and structural-labor exploration tool. The map is colored only by unemployment; the sector panel shows one selected country's agriculture, industry, and services shares over 1991–2022.
- Sector values are shares, not employment counts. Do not label them as global employment structure, normalize them, weight them by GDP or population, interpolate missing years, or infer causality.
- Keep `prepare_map_data`, `build_unemployment_map`, `prepare_sector_trend`, and `build_sector_trend` as small test seams for visual encoding and future measure expansion.

## Team alignment and review protocol

- Creative direction, architecture, technical lead, and manager roles must communicate concrete decisions, risks, and acceptance checks.
- Before implementation, each role must challenge the others' assumptions using the available grilling workflow until the team is aligned. The exact referenced `grill-me` skill is not installed in this environment, so use the available `grilling` skill as the fallback.
- The architect must inspect the actual codebase and git diff at four checkpoints: before implementation, after AGENTS.md changes, after app refactor/UI changes, and immediately before manager audit. Each checkpoint must call out scope drift, shallow seams, unnecessary dependencies, and regressions.
- The technical lead coordinates implementation and verification. The manager audits the final working tree against this file and the user request; only an explicit manager approval permits push or deployment.

## Completion criteria

- A fresh Streamlit Community Cloud deployment starts from the repository root with a documented run command.
- The CSV loads without manual preprocessing, and the app handles an invalid/missing file with a concise user-facing error.
- The year slider spans 1991–2022 and changes the map data; the country selector changes the sector history.
- The sector history renders agriculture, industry, and services across 1991–2022 with a fixed 0–100% axis and no interpolated gaps.
- The map renders country-level values with a legend, tooltip, and an understandable no-data treatment.
- At least one smoke check confirms the app imports/starts, the first and last years load, and a known country has a numeric value.
- Keep the smoke check reproducible in `smoke_check.py`; malformed or unusable CSVs must fail with a concise user-facing error rather than an uncaught min/max failure.
- No forecasting, authentication, database, extra page, or unnecessary dependency is introduced.
