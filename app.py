from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).with_name("Employment_Unemployment_GDP_data.csv")
YEAR_COLUMN = "Year"
COUNTRY_COLUMN = "Country Name"
MEASURE_COLUMN = "Unemployment Rate"
COLOR_COLUMN = "Unemployment Color"
REQUIRED_COLUMNS = [COUNTRY_COLUMN, YEAR_COLUMN, MEASURE_COLUMN]
MAP_CAP = 20.0


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
    data = data.dropna(subset=[COUNTRY_COLUMN, YEAR_COLUMN]).copy()
    data[YEAR_COLUMN] = data[YEAR_COLUMN].astype(int)
    return data


def prepare_map_data(year_data: pd.DataFrame, cap: float = MAP_CAP) -> pd.DataFrame:
    """Keep raw rates for tooltips and cap only the value used for map colors."""
    return year_data.assign(**{COLOR_COLUMN: year_data[MEASURE_COLUMN].clip(upper=cap)})


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
        custom_data=[MEASURE_COLUMN],
        color_continuous_scale=["#17324d", "#45b7aa", "#f0d264", "#f08a5d"],
        range_color=(0, cap),
        labels={COLOR_COLUMN: "Unemployment (%)"},
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{location}</b><br>"
            "Unemployment rate: %{customdata[0]:.2f}%<extra></extra>"
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
st.title("GLOBAL / UNEMPLOYMENT", icon=":material/public:")
st.caption("A country-level view of unemployment from 1991 to 2022.")

try:
    data = load_data(DATA_PATH)
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

min_year = int(data[YEAR_COLUMN].min())
max_year = int(data[YEAR_COLUMN].max())
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
st.caption(f"YEAR {selected_year}  /  {coverage} COUNTRIES WITH REPORTED DATA")

map_data = prepare_map_data(year_data)
fig = build_unemployment_map(map_data)
with st.container(border=True):
    st.plotly_chart(fig, width="stretch")

st.caption(
    "Source: [Employment_Unemployment_GDP_data.csv](https://www.kaggle.com/datasets/akshatsharma2/global-jobs-gdp-and-unemployment-data-19912022). "
    "Values are descriptive unemployment rates; "
    "country coverage varies by year; neutral gray indicates no reported data, and values above 20% "
    "use the endpoint color while tooltips retain the raw rate."
)
