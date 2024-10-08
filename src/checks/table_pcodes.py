from geopandas import GeoDataFrame

from src.config import CheckReturnList
from src.utils import is_empty


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
        pcode_columns = [
            column
            for column in gdf.columns
            for level in range(admin_level + 1)
            if column == f"ADM{level}_PCODE"
        ]
        row = {
            "iso3": iso3,
            "level": admin_level,
            "pcode_column_levels": len(pcode_columns),
            "pcode_cell_empty": sum(
                [
                    (gdf[column].isna() | gdf[column].map(is_empty)).sum()
                    for column in pcode_columns
                ],
            ),
            "pcode_cell_count": max(
                sum([gdf[column].size for column in pcode_columns]),
                1,
            ),
        }
        check_results.append(row)
    return check_results
