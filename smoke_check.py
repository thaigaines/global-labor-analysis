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

    snapshot = app.prepare_sector_snapshot(
        data, "United States", app.PRODUCT_MAX_YEAR
    )
    assert list(snapshot["Sector"]) == ["Agriculture", "Industry", "Services"]
    assert len(app.build_sector_snapshot(snapshot, app.PRODUCT_MAX_YEAR).data) == 3

    app_test = AppTest.from_file("app.py").run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert app_test.slider[0].min == app.PRODUCT_MIN_YEAR
    assert app_test.slider[0].max == app.PRODUCT_MAX_YEAR
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 2
    assert any(metric.label == "Nominal GDP" for metric in app_test.metric)
    assert any("nominal GDP context" in caption.value for caption in app_test.caption)
    _assert_synchronized_headings(app_test, app.PRODUCT_MAX_YEAR)

    app_test.slider[0].set_value(app.PRODUCT_MIN_YEAR).run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 2
    _assert_synchronized_headings(app_test, app.PRODUCT_MIN_YEAR)

    app_test.slider[0].set_value(app.PRODUCT_MAX_YEAR).run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 2
    _assert_synchronized_headings(app_test, app.PRODUCT_MAX_YEAR)

    app_test.selectbox[0].set_value("Afghanistan").run()
    assert not app_test.exception
    assert len(app_test.slider) == 1
    assert len(app_test.selectbox) == 1
    assert len(app_test.get("plotly_chart")) == 2

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
        "Smoke check passed: data contract, GDP context, lookup behavior, "
        "AppTest startup, synchronized endpoints, and selector interaction."
    )


if __name__ == "__main__":
    main()
