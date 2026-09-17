from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).with_name("Employment_Unemployment_GDP_data.csv")
YEAR_COLUMN = "Year"
COUNTRY_COLUMN = "Country Name"
MEASURE_COLUMN = "Unemployment Rate"
MEASURE_DISPLAY_COLUMN = "Unemployment Rate display"
COLOR_COLUMN = "Unemployment Color"
SECTOR_COLUMNS = [
    "Employment Sector: Agriculture",
    "Employment Sector: Industry",
    "Employment Sector: Services",
]
SECTOR_DISPLAY_COLUMNS = [f"{column} display" for column in SECTOR_COLUMNS]
REQUIRED_COLUMNS = [COUNTRY_COLUMN, YEAR_COLUMN, MEASURE_COLUMN, *SECTOR_COLUMNS]
MAP_CAP = 20.0
SOURCE_URL = "https://www.kaggle.com/datasets/akshatsharma2/global-jobs-gdp-and-unemployment-data-19912022"
PRODUCT_MIN_YEAR = 1991
PRODUCT_MAX_YEAR = 2022


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
    for column in SECTOR_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=[COUNTRY_COLUMN, YEAR_COLUMN]).copy()
    data[YEAR_COLUMN] = data[YEAR_COLUMN].astype(int)
    data = data[data[YEAR_COLUMN].between(PRODUCT_MIN_YEAR, PRODUCT_MAX_YEAR)].copy()
    if data.empty:
        raise ValueError("The CSV contains no usable country-year rows from 1991 to 2022.")
    return data


def prepare_map_data(year_data: pd.DataFrame, cap: float = MAP_CAP) -> pd.DataFrame:
    """Keep raw rates and readable display values while capping only map colors."""
    map_data = year_data.assign(**{COLOR_COLUMN: year_data[MEASURE_COLUMN].clip(upper=cap)})
    map_data[MEASURE_DISPLAY_COLUMN] = map_data[MEASURE_COLUMN].map(
        lambda value: f"{value:.2f}%" if pd.notna(value) else "No data"
    )
    for column, display_column in zip(SECTOR_COLUMNS, SECTOR_DISPLAY_COLUMNS):
        map_data[display_column] = map_data[column].map(
            lambda value: f"{value:.1f}%" if pd.notna(value) else "No data"
        )
    return map_data


def build_unemployment_map(map_data: pd.DataFrame, cap: float = MAP_CAP):
    """Build the unemployment map with an explicit, truthful visual encoding."""
    color_ticks = list(range(0, int(cap) + 1, 5))
    if color_ticks[-1] != cap:
        color_ticks.append(cap)
    fig = px.choropleth(
        map_data,
        locations=COUNTRY_COLUMN,
        locationmode="country names",
        color=COLOR_COLUMN,
        custom_data=[MEASURE_DISPLAY_COLUMN, *SECTOR_DISPLAY_COLUMNS],
        color_continuous_scale=["#17324d", "#45b7aa", "#f0d264", "#f08a5d"],
        range_color=(0, cap),
        labels={COLOR_COLUMN: "Unemployment (%)"},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{location}</b><br>"
            "Unemployment rate: %{customdata[0]}<br>"
            "Agriculture: %{customdata[1]}<br>"
            "Industry: %{customdata[2]}<br>"
            "Services: %{customdata[3]}<extra></extra>"
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
    )
    fig.update_coloraxes(
        colorbar={
            "title": f"Unemployment rate (%)<br>Values above {cap:g}% use endpoint color",
            "tickvals": color_ticks,
            "ticktext": [f"{value}%" for value in color_ticks],
            "ticks": "outside",
            "ticklen": 6,
            "tickwidth": 1,
            "tickcolor": "#73e6d1",
            "outlinewidth": 1,
            "outlinecolor": "#73e6d1",
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
        landcolor="#586575",
        center={"lon": 0, "lat": 0},
        projection={"type": "natural earth", "rotation": {"lon": 0, "lat": 0}},
    )
    return fig


st.set_page_config(page_title="Global Unemployment", page_icon=":material/public:", layout="wide")
st.title("GLOBAL / LABOR", icon=":material/public:")
st.caption("A clear view of unemployment and employment structure across countries, 1991–2022.")

try:
    data = load_data(DATA_PATH)
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

min_year = PRODUCT_MIN_YEAR
max_year = PRODUCT_MAX_YEAR
with st.container(horizontal=True, vertical_alignment="center", gap="small", border=True):
    st.markdown("**Year**", width="content")
    selected_year = st.slider(
        "Year",
        min_year,
        max_year,
        max_year,
        label_visibility="collapsed",
    )

year_data = data[data[YEAR_COLUMN] == selected_year]
coverage = year_data[MEASURE_COLUMN].notna().sum()
with st.container(horizontal=True, gap="small"):
    st.metric("Selected year", selected_year)
    st.metric("Reported countries", coverage)
    st.metric("Employment sectors", len(SECTOR_COLUMNS))

st.caption(f"YEAR {selected_year}  /  {coverage} COUNTRIES WITH REPORTED DATA")

map_data = prepare_map_data(year_data)
fig = build_unemployment_map(map_data)
with st.container(border=True):
    st.plotly_chart(fig, width="stretch")

st.caption(
    f"Source: [Employment_Unemployment_GDP_data.csv]({SOURCE_URL}). "
    "Values are descriptive unemployment rates; "
    "country coverage varies by year; sector values are shares rather than employment counts; "
    "GDP is nominal USD; neutral gray indicates no reported data, and values above 20% use the "
    "endpoint color while tooltips retain the raw rate."
)
