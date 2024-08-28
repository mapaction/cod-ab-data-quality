from src.checks.table_data_completeness import main

ISO3 = "mdg"


def test_mdg_completeness(gdfs):
    actual = main(ISO3, gdfs)
    expected = [
        {
            "iso3": "mdg",
            "level": 0,
            "total_number_of_records": 10,
            "number_of_missing_records": 2,
        },
        {
            "iso3": "mdg",
            "level": 1,
            "total_number_of_records": 352,
            "number_of_missing_records": 44,
        },
        {
            "iso3": "mdg",
            "level": 2,
            "total_number_of_records": 2380,
            "number_of_missing_records": 349,
        },
        {
            "iso3": "mdg",
            "level": 3,
            "total_number_of_records": 36317,
            "number_of_missing_records": 4723,
        },
        {
            "iso3": "mdg",
            "level": 4,
            "total_number_of_records": 454090,
            "number_of_missing_records": 52150,
        },
    ]
    assert actual == expected
