from src.checks.table_data_formatting_has_data import main


def test_table_data_formatting_has_data(iso3, gdfs):
    actual = main(iso3, gdfs)
    expected = [
        {"iso3": "mdg", "level": admin_level, "has_at_least_1_data_column": True}
        for admin_level in range(5)
    ]
    assert actual == expected
