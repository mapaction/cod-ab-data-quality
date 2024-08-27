from src.checks.table_data_formatting_heirarchical import main

ISO = "mdg"


def test_table_data_formatting_heirarchical(gdfs):
    actual = main(ISO, gdfs)
    expected = [
        {
            "iso3": "mdg",
            "level": admin_level,
            "proportion_of_expected_heirarchical_columns": 1.0,
        }
        for admin_level in range(5)
    ]
    assert actual == expected
