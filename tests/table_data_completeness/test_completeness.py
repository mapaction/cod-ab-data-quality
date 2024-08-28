"""Test for table completedness."""

from geopandas import GeoDataFrame

from src.checks.table_data_completeness import main


def test_mdg_completeness(iso3: str, gdfs: list[GeoDataFrame]):
    """Test for table completedness.

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames.
    """
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "MDG",
            "level": 0,
            "total_number_of_records": 10,
            "number_of_missing_records": 2,
        },
        {
            "iso3": "MDG",
            "level": 1,
            "total_number_of_records": 352,
            "number_of_missing_records": 44,
        },
        {
            "iso3": "MDG",
            "level": 2,
            "total_number_of_records": 2380,
            "number_of_missing_records": 349,
        },
        {
            "iso3": "MDG",
            "level": 3,
            "total_number_of_records": 36317,
            "number_of_missing_records": 4723,
        },
        {
            "iso3": "MDG",
            "level": 4,
            "total_number_of_records": 454090,
            "number_of_missing_records": 52150,
        },
    ]
    assert actual == expected
