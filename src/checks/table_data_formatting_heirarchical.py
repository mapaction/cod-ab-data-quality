import re

from geopandas import GeoDataFrame

from src.config import ADMIN_BOUNDARY_REGEX, CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check completeness of an admin boundary by checking column hierarchy.

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
            "proportion_of_expected_heirarchical_columns": proportion_of_expected_heirarchical_columns(
                admin_level, gdf
            ),
        }
        check_results.append(row)
    return check_results


def proportion_of_expected_heirarchical_columns(
    admin_level: int, gdf: GeoDataFrame
) -> float:
    """Check completeness of an admin boundary by checking
    column relationships.

    Admin boundaries appear to have a hierarchical structure, where each
    file of "smaller" admin boundaries (i.e. admin4 vs admin3) has column
    names which reference the previous "larger" admin boundary. For example,
    admin4 will have columns called admin3*, admin2*, admin1* and admin0*.

    Args:
        gdf - a geodataframe to analyse

    Returns:
        float, the proportion of expected columns in that file. e.g. if
        admin1.shp had admin1* and admin0* columns it would return 1. If it had
        just admin0* column it would return 0.5. If it had neither it would
        return 0.
    """
    seen_numbers = set()
    # Find all the numbers in column names (e.g. '3' in ADM3_PCODE).
    for col_name in gdf.columns:
        if match := re.match(ADMIN_BOUNDARY_REGEX, col_name, re.IGNORECASE):
            seen_numbers.add(int(match.group(1)))
    number_of_matches = 0
    # Count backwards, checking lower numbers are
    # in col names (e.g. 2,1,0 for ADM2_*).
    for i in range(admin_level, -1, -1):
        if i in seen_numbers:
            number_of_matches += 1
    return number_of_matches / (admin_level + 1)
