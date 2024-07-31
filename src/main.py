""" The main entry point to the script """

from src.table_data_completeness import table_data_completeness
from src.table_data_formatting import (
    table_data_formatting_has_data_cols,
    table_data_formatting_has_hierarchical_cols,
)


def main():
    table_completeness = table_data_completeness(
        "../tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm2_BNGRC_OCHA_20181031.dbf"
    )
    print(table_completeness)
    table_formatting = table_data_formatting_has_data_cols(
        "../tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm3_BNGRC_OCHA_20181031.dbf"
    )
    print(table_formatting)
    table_formatting2 = table_data_formatting_has_hierarchical_cols(
        "../tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm3_BNGRC_OCHA_20181031.dbf"
    )
    print(table_formatting2)


if __name__ == "__main__":
    main()
