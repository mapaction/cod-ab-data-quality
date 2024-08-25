import geopandas

EMPTY_VALUES = (None, "null", "")


def table_data_completeness(admin_boundary_path: str) -> float:
    """Check completeness of an admin boundary's table data.

    Iterates through a file's records and checks for values that are None,
    null or empty strings. Uses pandas isin for speed.

    Args:
        admin_boundary_path - a string representing the file to analyse.

    Returns:
         float between 0 and 1. 1 indicates complete table data (i.e. no
         missing data). A value of 0 indicates all table data is missing.
    """
    adm_boundary = geopandas.read_file(admin_boundary_path)
    all_records = adm_boundary.size
    missing_records = adm_boundary.isin(EMPTY_VALUES).sum().sum()
    return float((all_records - missing_records) / all_records)
