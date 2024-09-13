from geopandas import GeoDataFrame

from src.checks.table_data_formatting_heirarchical import main


def test_table_data_formatting_heirarchical(
    iso3: str,
    gdfs: list[GeoDataFrame],
) -> None:
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": admin_level,
            "total_heirarchical_columns": admin_level + 1,
        }
        for admin_level in range(5)
    ]
    assert actual == expected
