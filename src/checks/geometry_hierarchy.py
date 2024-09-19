from geopandas import GeoDataFrame

from src.config import CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check for the number of overlaping geometries between self and parent.

    If a dataset is perfectly hierarchally nested, each geometry will only belong to a
    single parent geometry.

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of check rows to be outputed as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        if admin_level == 0:
            continue
        parent = gdfs[admin_level - 1]
        if gdf.active_geometry_name and parent.active_geometry_name:
            parents = len(gdf.sjoin(parent, how="left", predicate="overlaps").index)
            row = {
                "iso3": iso3,
                "level": admin_level,
                "geom_parent_overlaps": parents - len(gdf.index),
            }
            check_results.append(row)
    return check_results
