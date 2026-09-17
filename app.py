from pathlib import Path
from math import log1p

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).with_name("Employment_Unemployment_GDP_data.csv")
YEAR_COLUMN = "Year"
COUNTRY_COLUMN = "Country Name"
MEASURE_COLUMN = "Unemployment Rate"
COLOR_COLUMN = "Unemployment Color"
REQUIRED_COLUMNS = [COUNTRY_COLUMN, YEAR_COLUMN, MEASURE_COLUMN]


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path.name}.")

    data = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"The CSV is missing required columns: {', '.join(missing)}")

    data[YEAR_COLUMN] = pd.to_numeric(data[YEAR_COLUMN], errors="coerce")
    data[MEASURE_COLUMN] = pd.to_numeric(data[MEASURE_COLUMN], errors="coerce")
    data = data.dropna(subset=REQUIRED_COLUMNS).copy()
    data[YEAR_COLUMN] = data[YEAR_COLUMN].astype(int)
    return data


st.set_page_config(page_title="Global Unemployment", page_icon=":material/public:", layout="wide")
st.title("GLOBAL / UNEMPLOYMENT", icon=":material/public:")
st.caption("A country-level view of unemployment from 1991 to 2022.")

try:
    data = load_data(DATA_PATH)
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

min_year = int(data[YEAR_COLUMN].min())
max_year = int(data[YEAR_COLUMN].max())
selected_year = st.slider("Year", min_year, max_year, max_year)

year_data = data[data[YEAR_COLUMN] == selected_year]
coverage = year_data[MEASURE_COLUMN].notna().sum()
st.caption(f"YEAR {selected_year}  /  {coverage} COUNTRIES WITH REPORTED DATA")

map_data = year_data.assign(**{COLOR_COLUMN: year_data[MEASURE_COLUMN].map(log1p)})
color_ticks = [0, 5, 10, 15, 20, 25, 30, 35]

fig = px.choropleth(
    map_data,
    locations=COUNTRY_COLUMN,
    locationmode="country names",
    color=COLOR_COLUMN,
    hover_name=COUNTRY_COLUMN,
    hover_data={MEASURE_COLUMN: ":.2f", COLOR_COLUMN: False},
    color_continuous_scale=["#17324d", "#45b7aa", "#f0d264", "#f08a5d"],
    range_color=(log1p(float(data[MEASURE_COLUMN].min())), log1p(float(data[MEASURE_COLUMN].max()))),
    labels={MEASURE_COLUMN: "Unemployment (%)", COLOR_COLUMN: "Unemployment (%)"},
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#07111f",
    plot_bgcolor="#07111f",
    margin={"r": 0, "t": 10, "l": 0, "b": 0},
)
fig.update_coloraxes(
    colorbar={
        "title": "Unemployment (%)",
        "tickvals": [log1p(value) for value in color_ticks],
        "ticktext": [str(value) for value in color_ticks],
    }
)
fig.update_geos(
    showframe=False,
    bgcolor="#07111f",
    showcoastlines=True,
    showcountries=True,
    showocean=True,
    oceancolor="#07111f",
    showland=True,
    landcolor="#142538",
)
with st.container(border=True):
    st.plotly_chart(fig, width="stretch")

st.caption(
    "Source: Employment_Unemployment_GDP_data.csv. Values are descriptive unemployment rates; "
    "country coverage varies by year and does not imply causation."
)
