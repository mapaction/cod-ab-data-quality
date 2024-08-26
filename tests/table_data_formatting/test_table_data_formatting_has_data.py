from src.checks.table_data_formatting_has_data import main

ISO = "mdg"


def test_table_data_formatting_has_data(gdfs):
    actual = main(ISO, gdfs)
    expected = [
        {"iso3": "mdg", "level": admin_level, "has_at_least_1_data_column": True}
        for admin_level in range(5)
    ]
    assert actual == expected
