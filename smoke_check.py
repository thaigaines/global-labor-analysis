from streamlit.testing.v1 import AppTest

import app


def main() -> None:
    data = app.load_data(app.DATA_PATH)
    assert data[app.YEAR_COLUMN].min() == app.PRODUCT_MIN_YEAR
    assert data[app.YEAR_COLUMN].max() == app.PRODUCT_MAX_YEAR
    assert all(column in data.columns for column in app.SECTOR_COLUMNS)
    trend = app.prepare_sector_trend(data, "United States")
    assert trend[app.YEAR_COLUMN].min() == app.PRODUCT_MIN_YEAR
    assert trend[app.YEAR_COLUMN].max() == app.PRODUCT_MAX_YEAR
    assert list(trend.columns) == [app.YEAR_COLUMN, "Agriculture", "Industry", "Services"]
    assert len(app.build_sector_trend(trend).data) == 3
    sparse_trend = app.prepare_sector_trend(data, "Afghanistan")
    assert len(sparse_trend) == app.PRODUCT_MAX_YEAR - app.PRODUCT_MIN_YEAR + 1
    assert sparse_trend["Agriculture"].isna().any()

    us_2022 = data[
        data[app.COUNTRY_COLUMN].eq("United States")
        & data[app.YEAR_COLUMN].eq(app.PRODUCT_MAX_YEAR)
    ][app.MEASURE_COLUMN]
    assert not us_2022.empty and us_2022.iloc[0] == us_2022.iloc[0]

    app_test = AppTest.from_file("app.py").run()
    assert not app_test.exception
    assert app_test.slider[0].min == app.PRODUCT_MIN_YEAR
    assert app_test.slider[0].max == app.PRODUCT_MAX_YEAR

    app_test.slider[0].set_value(app.PRODUCT_MIN_YEAR).run()
    assert not app_test.exception
    app_test.slider[0].set_value(app.PRODUCT_MAX_YEAR).run()
    assert not app_test.exception

    print("Smoke check passed: app startup, year endpoints, sector trend, sector fields, and U.S. value.")


if __name__ == "__main__":
    main()
