""" The main entry point to the script """

from src.table_data_completeness import table_data_completeness


def main():
    table_completeness = table_data_completeness(
        "../tests/test_data/mdg_adm_bngrc_ocha_20181031_shp/"
        "mdg_admbnda_adm2_BNGRC_OCHA_20181031.dbf"
    )
    print(table_completeness)


if __name__ == "__main__":
    main()
