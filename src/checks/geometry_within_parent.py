from re import match

from geopandas import GeoDataFrame

from src.config import CheckReturnList


def check_nesting(
    row: dict,
    gdf: GeoDataFrame,
    admin_level: int,
    within: GeoDataFrame,
) -> dict[str, int | str]:
    """Checks whether nested polygon contains all the same attributes as its parent.

    Args:
        row: Check result for current layer.
        gdf: layer GeoDataFrame.
        admin_level: layer admin level.
        within: layer GeoDataFrame join with its parent's attributes.

    Returns:
        Check result for current layer.
    """
    name_columns = [
        column
        for column in gdf.columns
        for level in range(admin_level)
        if match(rf"^ADM{level}_[A-Z][A-Z]$", column)
    ]
    pcode_columns = [
        column
        for column in gdf.columns
        for level in range(admin_level)
        if column == f"ADM{level}_PCODE"
    ]
    for name, columns in [("name", name_columns), ("pcode", pcode_columns)]:
        for column in columns:
            column_left = column + "_left"
            column_right = column + "_right"
            if all(x in within.columns for x in [column_left, column_right]):
                same_value = within[column_left].eq(within[column_right]).sum()
                row[f"geom_within_{name}_mismatch"] += len(within.index) - same_value
    return row


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
        row = {
            "iso3": iso3,
            "level": admin_level,
            "geom_not_within_parent": 0,
            "geom_within_name_mismatch": 0,
            "geom_within_pcode_mismatch": 0,
        }
        if (
            admin_level > 0
            and gdf.active_geometry_name
            and gdfs[admin_level - 1].active_geometry_name
        ):
            parent = gdfs[admin_level - 1]
            within = gdf.sjoin(parent, predicate="within")
            row["geom_not_within_parent"] = len(gdf.index) - len(within.index)
            row = check_nesting(row, gdf, admin_level, within)
        check_results.append(row)
    return check_results
