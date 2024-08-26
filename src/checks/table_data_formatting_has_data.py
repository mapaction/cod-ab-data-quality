import re

from geopandas import GeoDataFrame

from src.utils import CheckReturnList

EMPTY_VALUES = (None, "null", "")
ADMIN_BOUNDARY_REGEX = r"^[aA][dD](?:M|I|N)*(\d).*"


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
            "has_at_least_1_data_column": table_data_formatting_has_data_cols(gdf),
        }
        check_results.append(row)
    return check_results


def table_data_formatting_has_data_cols(gdf: GeoDataFrame) -> float:
    """Check completeness of an admin boundary by checking the columns.

    Args:
        gdf - a Geopandas geodataframe representing a COD admin boundary

    Returns:
         1 if _any_ columns match the regex. 0 otherwise.
    """
    for column in gdf.columns:
        if re.match(ADMIN_BOUNDARY_REGEX, column, re.IGNORECASE):
            return True
    return False
