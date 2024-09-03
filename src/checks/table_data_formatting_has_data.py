import re

from geopandas import GeoDataFrame

from src.config import ADMIN_BOUNDARY_REGEX, CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check completeness of an admin boundary by checking the columns.

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of check rows to be outputed as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        row = {
            "iso3": iso3,
            "level": admin_level,
            "has_any_data_columns": any(
                re.match(ADMIN_BOUNDARY_REGEX, column) for column in gdf.columns
            ),
        }
        check_results.append(row)
    return check_results
