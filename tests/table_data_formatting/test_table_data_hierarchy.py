from pytest import mark

from src.table_data_formatting import (  # noqa: E501
    table_data_formatting_has_hierarchical_cols,
)


@mark.parametrize(
    "admin_level,expected_value",
    [
        (0, 1),
        (1, 1),
        (2, 1),
        (3, 1),
    ],
)
def test_table_data_hierarchy(admin_level, expected_value):
    actual_value = table_data_formatting_has_hierarchical_cols(
        "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        f"mdg_admbnda_adm{admin_level}_BNGRC_OCHA_20181031.dbf"
    )
    assert actual_value == expected_value
