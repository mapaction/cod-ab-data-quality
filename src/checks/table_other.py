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
        name_columns = [
            column
            for column in gdf.columns
            for level in range(admin_level + 1)
            if match(rf"^ADM{level}_[A-Z][A-Z]$", column)
        ]
        pcode_columns = [
            column
            for column in gdf.columns
            for level in range(admin_level + 1)
            if column == f"ADM{level}_PCODE"
        ]
        metadata_columns = [
            "OBJECTID",
            "geometry",
            "Shape__Area",
            "Shape__Length",
            "date",
            "validOn",
            "validTo",
            "AREA_SQKM",
        ]
        ref_name_columns = [
            x for x in gdf.columns if match(rf"^ADM{admin_level}_REF", x)
        ]
        alt_name_columns = [
            column
            for column in gdf.columns
            for level in range(admin_level + 1)
            if match(rf"^ADM{level}ALT[12]_?[A-Z][A-Z]$", column)
        ]
        valid_columns = (
            name_columns
            + pcode_columns
            + metadata_columns
            + ref_name_columns
            + alt_name_columns
        )
        other_columns = [x for x in gdf.columns if x not in valid_columns]
        row = {
            "iso3": iso3,
            "level": admin_level,
            "ref_name_column_count": len(ref_name_columns),
            "ref_name_columns": ",".join(ref_name_columns),
            "alt_name_column_count": len(alt_name_columns),
            "alt_name_columns": ",".join(alt_name_columns),
            "other_column_count": len(other_columns),
            "other_columns": ",".join(other_columns),
        }
        check_results.append(row)
    return check_results
