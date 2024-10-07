from geopandas import GeoDataFrame

from src.checks.table_data_formatting_has_data import main


def test_table_data_formatting_has_data(iso3: str, gdfs: list[GeoDataFrame]) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 0,
            "levels_with_data": 1,
            "levels_with_pcode": 1,
            "levels_with_name": 1,
            "name_count": 1,
        },
        {
            "iso3": "MDG",
            "level": 1,
            "levels_with_data": 2,
            "levels_with_pcode": 2,
            "levels_with_name": 2,
            "name_count": 2,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "levels_with_data": 3,
            "levels_with_pcode": 3,
            "levels_with_name": 3,
            "name_count": 3,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "levels_with_data": 4,
            "levels_with_pcode": 4,
            "levels_with_name": 4,
            "name_count": 4,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "levels_with_data": 5,
            "levels_with_pcode": 5,
            "levels_with_name": 5,
            "name_count": 5,
        },
    ]
    assert actual == expected
