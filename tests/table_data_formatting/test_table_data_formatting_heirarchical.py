from src.checks.table_data_formatting_heirarchical import main


def test_table_data_formatting_heirarchical(iso3, gdfs):
    actual = main(iso3, gdfs)
    expected = [
        {
            "iso3": "mdg",
            "level": admin_level,
            "proportion_of_expected_heirarchical_columns": 1.0,
        }
        for admin_level in range(5)
    ]
    assert actual == expected
