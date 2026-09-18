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
SECTOR_LABELS = {
    "Employment Sector: Agriculture": "Agriculture",
    "Employment Sector: Industry": "Industry",
    "Employment Sector: Services": "Services",
}
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
    # Preserve the source rate for tooltips; cap only the value that drives map color.
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
        height=560,
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


def prepare_sector_snapshot(data: pd.DataFrame, country: str, year: int) -> pd.DataFrame:
    """Return one country's sector shares for the selected year in chart-ready form."""
    # Keep a fixed three-row shape so sector order and missing-state handling stay stable.
    row = data[
        data[COUNTRY_COLUMN].eq(country) & data[YEAR_COLUMN].eq(year)
    ]
    values = row.iloc[0] if not row.empty else pd.Series(dtype="float64")
    return pd.DataFrame(
        {
            "Sector": list(SECTOR_LABELS.values()),
            "Share": [values.get(column, float("nan")) for column in SECTOR_COLUMNS],
        }
    )


def build_sector_snapshot(snapshot_data: pd.DataFrame, year: int):
    """Build a vivid, comparable sector-share snapshot for one country-year."""
    plot_data = snapshot_data.dropna(subset=["Share"])
    missing_sectors = snapshot_data.loc[
        snapshot_data["Share"].isna(), "Sector"
    ].tolist()
    fig = px.bar(
        plot_data,
        x="Sector",
        y="Share",
        color="Sector",
        text="Share",
        color_discrete_map={
            "Agriculture": "#f0b45b",
            "Industry": "#8fa9c9",
            "Services": "#73e6d1",
        },
        category_orders={"Sector": list(SECTOR_LABELS.values())},
        labels={"Share": "Employment share (%)"},
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate=f"{year}<br>%{{x}}: %{{y:.1f}}%<extra></extra>",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        margin={"r": 20, "t": 20, "l": 10, "b": 10},
        showlegend=False,
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%", gridcolor="#26384b")
    fig.update_xaxes(showgrid=False)
    if missing_sectors:
        fig.add_annotation(
            text=f"No data: {', '.join(missing_sectors)}",
            xref="paper",
            yref="paper",
            x=0,
            y=1.08,
            showarrow=False,
            font={"color": "#a9b7c6", "size": 12},
            align="left",
        )
    return fig


st.set_page_config(page_title="Global Labor Explorer", page_icon=":material/public:", layout="wide")
st.title("GLOBAL / LABOR", icon=":material/public:")
st.subheader("One globe. A changing shape of work.")
st.caption("A country-level view of unemployment and employment structure from 1991 to 2022.")

try:
    data = load_data(DATA_PATH)
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

countries = sorted(data[COUNTRY_COLUMN].dropna().unique())

# Seed the slider before the map so the requested visual order stays map -> slider.
st.session_state.setdefault("selected_year", PRODUCT_MAX_YEAR)
selected_year = int(st.session_state["selected_year"])
year_data = data[data[YEAR_COLUMN] == selected_year]
coverage = year_data[MEASURE_COLUMN].notna().sum()

# The selector changes the snapshot; the shared year keeps both views synchronized.
map_data = prepare_map_data(year_data)
fig = build_unemployment_map(map_data)
with st.container(border=True):
    heading, stat = st.columns([3.6, 1], vertical_alignment="bottom", gap="large")
    with heading:
        st.markdown("**01 / GLOBAL SNAPSHOT**")
        st.subheader(f"Unemployment across the world · {selected_year}")
        st.caption("Hover a country to read its unemployment rate and sector shares.")
    with stat:
        st.metric("Reported countries", f"{coverage}")
    st.plotly_chart(fig, width="stretch")

with st.container(horizontal=True, vertical_alignment="center", gap="small", border=True):
    st.markdown("**02 / MOVE THROUGH TIME**", width="content")
    st.slider(
        "Year",
        PRODUCT_MIN_YEAR,
        PRODUCT_MAX_YEAR,
        key="selected_year",
        label_visibility="collapsed",
    )

st.caption(f"{selected_year} · {coverage} countries with reported unemployment")

with st.container(border=True):
    selector_label, selector_control = st.columns([1.4, 2.6], vertical_alignment="center", gap="large")
    with selector_label:
        st.markdown("**03 / COUNTRY LENS**")
        st.caption("Choose a country to see how its employment mix changes with the year.")
    with selector_control:
        selected_country = st.selectbox(
            "Country for sector snapshot",
            countries,
            index=countries.index("United States") if "United States" in countries else 0,
            label_visibility="collapsed",
        )

sector_snapshot = prepare_sector_snapshot(data, selected_country, selected_year)
with st.container(border=True):
    st.markdown("**04 / THE SHAPE OF WORK**")
    st.subheader(f"Sector composition · {selected_country} · {selected_year}")
    st.caption("Employment shares for the selected country and year. Move the year slider to watch the mix shift.")
    st.plotly_chart(build_sector_snapshot(sector_snapshot, selected_year), width="stretch")

st.caption(
    f"Source: [Employment_Unemployment_GDP_data.csv]({SOURCE_URL}). "
    "Values are descriptive unemployment rates; "
    "country coverage varies by year; sector values are shares rather than employment counts; "
    "GDP is nominal USD; neutral gray indicates no reported data, and values above 20% use the "
    "endpoint color while tooltips retain the raw rate."
)
st.caption("Project by Thai Gaines.")
