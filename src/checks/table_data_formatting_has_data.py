from re import match

from geopandas import GeoDataFrame

from src.config import CheckReturnList


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
            "levels_with_data": sum(
                [
                    any(column.startswith(f"ADM{level}") for column in gdf.columns)
                    for level in range(admin_level + 1)
                ],
            ),
            "levels_with_name": sum(
                [
                    any(
                        bool(match(rf"^ADM{level}_[A-Z][A-Z]$", column))
                        for column in gdf.columns
                    )
                    for level in range(admin_level + 1)
                ],
            ),
            "levels_with_pcode": sum(
                [
                    any(column == f"ADM{level}_PCODE" for column in gdf.columns)
                    for level in range(admin_level + 1)
                ],
            ),
            "name_count": sum(
                [
                    bool(match(rf"^ADM{level}_[A-Z][A-Z]$", column))
                    for column in gdf.columns
                    for level in range(admin_level + 1)
                ],
            ),
        }
        check_results.append(row)
    return check_results
