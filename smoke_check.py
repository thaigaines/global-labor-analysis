from numbers import Real

import pandas as pd
from streamlit.testing.v1 import AppTest

import app


def _heading_values(app_test: AppTest) -> list[str]:
    return [element.value for element in app_test.subheader]


def _assert_synchronized_headings(app_test: AppTest, year: int) -> None:
    headings = _heading_values(app_test)
    assert any(
        heading.startswith("Where unemployment is reported") and str(year) in heading
        for heading in headings
    )
    assert any(
        heading.startswith("Employment mix") and str(year) in heading
        for heading in headings
    )


def main() -> None:
    data = app.load_data(app.DATA_PATH)
    assert data[app.YEAR_COLUMN].min() == app.PRODUCT_MIN_YEAR
    assert data[app.YEAR_COLUMN].max() == app.PRODUCT_MAX_YEAR
    assert all(column in data.columns for column in app.SECTOR_COLUMNS)
    assert app.GDP_COLUMN in data.columns
    assert pd.api.types.is_numeric_dtype(data[app.GDP_COLUMN])

    known_row = data[
        data[app.COUNTRY_COLUMN].eq("United States")
        & data[app.YEAR_COLUMN].eq(app.PRODUCT_MAX_YEAR)
    ].iloc[0]
    assert isinstance(known_row[app.GDP_COLUMN], Real)
    assert known_row[app.GDP_COLUMN] >= 0

    map_data = app.prepare_map_data(
        data[data[app.YEAR_COLUMN].eq(app.PRODUCT_MAX_YEAR)]
    )
    assert app.GDP_DISPLAY_COLUMN in map_data.columns
    assert map_data[app.GDP_DISPLAY_COLUMN].notna().all()
    map_figure = app.build_unemployment_map(map_data)
    assert "Nominal GDP" in map_figure.data[0].hovertemplate
    assert map_figure.layout.coloraxis.cmax == app.MAP_CAP
    assert f"{app.MAP_CAP:g}%+" in map_figure.layout.coloraxis.colorbar.ticktext
    capped_row = pd.DataFrame(
        {
            app.MEASURE_COLUMN: [app.MAP_CAP + 5],
            app.GDP_COLUMN: [0],
            **{column: [float("nan")] for column in app.SECTOR_COLUMNS},
        }
    )
    capped_map_data = app.prepare_map_data(capped_row)
    assert capped_map_data[app.COLOR_COLUMN].iloc[0] == app.MAP_CAP
    assert (
        capped_map_data[app.MEASURE_DISPLAY_COLUMN].iloc[0]
        == f"{app.MAP_CAP + 5:.2f}%"
    )

    snapshot = app.prepare_sector_snapshot(
        data, "United States", app.PRODUCT_MAX_YEAR
    )
    assert list(snapshot["Sector"]) == ["Agriculture", "Industry", "Services"]
    sector_figure = app.build_sector_snapshot(snapshot, app.PRODUCT_MAX_YEAR)
    assert len(sector_figure.data) == 3
    assert all(trace.orientation == "h" for trace in sector_figure.data)
    assert list(sector_figure.layout.xaxis.range) == [0, 100]
    edge_snapshot = pd.DataFrame(
        {
            "Sector": ["Agriculture", "Industry", "Services"],
            "Share": [0.0, float("nan"), 100.0],
        }
    )
    edge_figure = app.build_sector_snapshot(edge_snapshot, 2000)
    assert any(0.0 in trace.x for trace in edge_figure.data)
    assert any(100.0 in trace.x for trace in edge_figure.data)
    assert any(
        annotation.y == "Agriculture" and annotation.text == "0.0%"
        for annotation in edge_figure.layout.annotations
    )
    assert any(
        annotation.y == "Industry" and annotation.text == "No data"
        for annotation in edge_figure.layout.annotations
    )
    all_missing = edge_snapshot.assign(Share=float("nan"))
    missing_figure = app.build_sector_snapshot(all_missing, 2000)
    assert len(missing_figure.data) == 0
    assert len(missing_figure.layout.annotations) == 3

    trajectory = app.prepare_unemployment_trajectory(
        data, "United States", app.PRODUCT_MAX_YEAR
    )
    assert list(trajectory[app.YEAR_COLUMN]) == list(range(1991, 2023))
    assert trajectory["Selected year"].sum() == 1
    trajectory_figure = app.build_unemployment_trajectory(
        trajectory, app.PRODUCT_MAX_YEAR
    )
    assert list(trajectory_figure.layout.xaxis.range) == [
        app.PRODUCT_MIN_YEAR,
        app.PRODUCT_MAX_YEAR,
    ]
    assert trajectory_figure.data[0].connectgaps is False
    assert len(trajectory_figure.data) == 2
    assert all(trace.cliponaxis is False for trace in trajectory_figure.data)
    partial_history = data[data[app.COUNTRY_COLUMN].eq("United States")].drop(
        data[data[app.COUNTRY_COLUMN].eq("United States")
             & data[app.YEAR_COLUMN].eq(2000)].index
    )
    partial_trajectory = app.prepare_unemployment_trajectory(
        partial_history, "United States", 2000
    )
    missing_year = partial_trajectory.loc[
        partial_trajectory[app.YEAR_COLUMN].eq(2000)
    ].iloc[0]
    assert pd.isna(missing_year[app.MEASURE_COLUMN])
    assert len(partial_trajectory) == app.PRODUCT_MAX_YEAR - app.PRODUCT_MIN_YEAR + 1
    partial_figure = app.build_unemployment_trajectory(partial_trajectory, 2000)
    assert len(partial_figure.data) == 1
    assert partial_figure.layout.shapes[0].x0 == 2000

    app_test = AppTest.from_file("app.py").run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert app_test.slider[0].min == app.PRODUCT_MIN_YEAR
    assert app_test.slider[0].max == app.PRODUCT_MAX_YEAR
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 3
    assert app_test.slider[0].label == "Explore a year"
    assert any(metric.label == "Nominal GDP" for metric in app_test.metric)
    assert any(
        "associations, not evidence of causation" in caption.value
        for caption in app_test.caption
    )
    _assert_synchronized_headings(app_test, app.PRODUCT_MAX_YEAR)

    app_test.slider[0].set_value(app.PRODUCT_MIN_YEAR).run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 3
    _assert_synchronized_headings(app_test, app.PRODUCT_MIN_YEAR)

    app_test.slider[0].set_value(app.PRODUCT_MAX_YEAR).run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 3
    _assert_synchronized_headings(app_test, app.PRODUCT_MAX_YEAR)

    app_test.selectbox[0].set_value("Afghanistan").run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 3
    app_test.slider[0].set_value(app.PRODUCT_MIN_YEAR).run()
    assert not app_test.exception
    assert any(
        metric.label == "Unemployment" and metric.value == "No data"
        for metric in app_test.metric
    )
    assert any(
        "no rate was reported, so there is no dot" in caption.value
        for caption in app_test.caption
    )

    # The lookup seam must centralize country-year uniqueness and missing-row behavior.
    assert callable(getattr(app, "get_country_year_row", None))
    country_year_row = app.get_country_year_row(
        data, "United States", app.PRODUCT_MAX_YEAR
    )
    assert country_year_row is not None
    assert country_year_row[app.COUNTRY_COLUMN] == "United States"
    assert country_year_row[app.YEAR_COLUMN] == app.PRODUCT_MAX_YEAR
    assert (
        app.get_country_year_row(data, "__missing_country__", app.PRODUCT_MAX_YEAR)
        is None
    )

    print(
        "Smoke check passed: data contract, capped map color, sector edge cases, "
        "trajectory gaps, synchronized years, and missing-year UI."
    )


if __name__ == "__main__":
    main()
