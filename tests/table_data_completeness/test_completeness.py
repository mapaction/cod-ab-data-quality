import numpy as np

from src.checks.table_data_completeness import main

ISO3 = "mdg"


def test_mdg_completeness(gdfs):
    actual = main(ISO3, gdfs)
    expected = [
        {
            "iso3": "mdg",
            "level": 0,
            "total_number_of_records": 4,
            "number_of_missing_records": np.int64(0),
        },
        {
            "iso3": "mdg",
            "level": 1,
            "total_number_of_records": 220,
            "number_of_missing_records": np.int64(0),
        },
        {
            "iso3": "mdg",
            "level": 2,
            "total_number_of_records": 1666,
            "number_of_missing_records": np.int64(113),
        },
        {
            "iso3": "mdg",
            "level": 3,
            "total_number_of_records": 26843,
            "number_of_missing_records": np.int64(1573),
        },
        {
            "iso3": "mdg",
            "level": 4,
            "total_number_of_records": 349300,
            "number_of_missing_records": np.int64(17273),
        },
    ]
    assert actual == expected
