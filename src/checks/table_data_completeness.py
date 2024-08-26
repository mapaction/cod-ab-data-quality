from geopandas import GeoDataFrame

from src.utils import CheckReturnList

EMPTY_VALUES = (None, "null", "")


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check completeness of an admin boundary's table data.

    Iterates through a file's records and checks for values that are None,
    null or empty strings. Uses vectorized pandas for speed.

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
            "total_number_of_records": gdf.size,
            "number_of_missing_records": int(
                (
                    gdf.isna()
                    | gdf.apply(
                        lambda x: x.str.strip() == "" if x.dtype == "object" else False
                    )
                )
                .values.sum()
                .sum()
            ),
        }
        check_results.append(row)
    return check_results
