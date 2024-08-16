from pytest import approx

from src.check_table_completeness.table_data_completeness import table_data_completeness


def test_mdg_adm0_completeness():
    table_completeness = table_data_completeness(
        "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm0_BNGRC_OCHA_20181031.dbf"
    )
    assert table_completeness == 1.0


def test_mdg_adm1_completeness():
    table_completeness = table_data_completeness(
        "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm1_BNGRC_OCHA_20181031.shp"
    )
    assert table_completeness == 1.0


def test_mdg_adm2_completeness():
    table_completeness = table_data_completeness(
        "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm2_BNGRC_OCHA_20181031.shp"
    )
    assert table_completeness == approx(0.93, 0.01)


def test_mdg_adm3_completeness():
    table_completeness = table_data_completeness(
        "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm3_BNGRC_OCHA_20181031.shp"
    )
    assert table_completeness == approx(0.94, 0.01)


def test_mdg_adm4_completeness():
    table_completeness = table_data_completeness(
        "tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm4_BNGRC_OCHA_20181031.shp"
    )
    assert table_completeness == approx(0.95, 0.01)
