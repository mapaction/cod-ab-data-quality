from geopandas import GeoDataFrame

from src.config import CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check for the number of self-overlaping geometries.

    Conducting a spatial join predicated by overlaps is very computationally expensive.
    This module has been separated out from other geometry checks so that it can be made
    optional.

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of check rows to be outputed as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        if gdf.active_geometry_name:
            overlaps = gdf.sjoin(gdf, predicate="overlaps")
            overlap_count = len(overlaps[overlaps.index != overlaps.index_right].index)
            row = {
                "iso3": iso3,
                "level": admin_level,
                "geom_overlaps_self": overlap_count / 2,
            }
            check_results.append(row)
    return check_results
