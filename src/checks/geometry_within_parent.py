from geopandas import GeoDataFrame

from src.config import CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check for the number of geometries within a parent layer.

    If a dataset is perfectly hierarchally nested, each geometry will fall within a
    parent geometry.

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
            if admin_level == 0:
                row = {
                    "iso3": iso3,
                    "level": admin_level,
                    "geom_not_within_parent": 0,
                }
                check_results.append(row)
            else:
                parent = gdfs[admin_level - 1]
                if parent.active_geometry_name:
                    within = gdf.sjoin(parent, predicate="within")
                    row = {
                        "iso3": iso3,
                        "level": admin_level,
                        "geom_not_within_parent": len(gdf.index) - len(within.index),
                    }
                    pcode_left = f"ADM{admin_level-1}_PCODE_left"
                    pcode_right = f"ADM{admin_level-1}_PCODE_right"
                    if all(x in within.columns for x in [pcode_left, pcode_right]):
                        pcode = within[
                            within[f"ADM{admin_level-1}_PCODE_left"].eq(
                                within[f"ADM{admin_level-1}_PCODE_right"],
                            )
                        ]
                        row |= {
                            "geom_not_within_pcode": len(within.index)
                            - len(pcode.index),
                        }
                    check_results.append(row)
    return check_results
