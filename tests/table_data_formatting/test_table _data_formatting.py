import pytest

from src.table_data_formatting import table_data_formatting_has_data_cols


@pytest.mark.parametrize(
    "admin_level,expected_value",
    [
        (0, 1),
        (1, 1),
        (2, 1),
        (3, 0),
    ],
)
def test_table_data_formatting_has_data_cols_adm3(admin_level, expected_value):
    table_completeness = table_data_formatting_has_data_cols(
        f"tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        f"mdg_admbnda_adm{admin_level}_BNGRC_OCHA_20181031.shp"
    )
    assert table_completeness == expected_value
