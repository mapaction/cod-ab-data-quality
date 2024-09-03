from geopandas import GeoDataFrame

from src.config import CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Checks for unique date values within dataset.

    There are two date fields within each COD-AB, "date" and "validOn". "date"
    represents when the current boundaries went into effect for the specified location.
    "validOn" represents when this dataset was last changed throughout the data update
    lifecycle. If there are multiple unique values for dates within the dataset, they
    will be listed in separate output columns: "date_1", "date_2", etc.

    The following are a list of source and output columns:
    - source: "date"
        - output: "date_1", "date_2", etc...
    - source: "validOn"
        - output: "update_1", "update_2", etc...

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of results from this check to output as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        row = {"iso3": iso3, "level": admin_level}
        try:
            gdf_date = gdf["date"].dt.date.drop_duplicates()
            for index, value in enumerate(gdf_date):
                row[f"date_{index+1}"] = value
            gdf_update = gdf["validOn"].dt.date.drop_duplicates()
            for index, value in enumerate(gdf_update):
                row[f"update_{index+1}"] = value
        except KeyError:
            pass
        check_results.append(row)
    return check_results
