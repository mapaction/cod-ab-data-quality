import shapefile

EMPTY_VALUES = (None, "null", "")


def table_data_completeness(shapefile_path: str) -> float:
    """Check completeness of a shapefile's table data.

    Iterates through a shapefile's records and checks for values that are None,
    null or empty strings.

    Args:
        shapefile_path - a string representing the shapefile to analyse.

    Returns:
         float between 0 and 1. 1 indicates complete table data (i.e. no
         missing data). A value of 0 indicates all table data is missing.
    """
    complete_records, missing_records = 0, 0
    sf = shapefile.Reader(shapefile_path)
    for record in sf.iterRecords():
        for field in record:
            if field in EMPTY_VALUES:
                missing_records += 1
            else:
                complete_records += 1
    return complete_records / (complete_records + missing_records)
