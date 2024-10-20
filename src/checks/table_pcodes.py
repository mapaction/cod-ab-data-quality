from geopandas import GeoDataFrame
from hdx.location.country import Country

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

    def not_iso2(value: str | None) -> bool:
        iso2 = Country.get_iso2_from_iso3(iso3)
        if iso2 and value and value.strip():
            return not value.startswith(iso2)
        return False

    def not_alnum(value: str | None) -> bool:
        if value and value.strip():
            return not value.isalnum()
        return False

    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        pcode_columns = [
            column
            for column in gdf.columns
            for level in range(admin_level + 1)
            if column == f"ADM{level}_PCODE"
        ]
        pcodes = gdf[pcode_columns]
        row = {
            "iso3": iso3,
            "level": admin_level,
            "pcode_column_levels": len(pcode_columns),
            "pcode_cell_count": max(pcodes.size, 1),
            "pcode_empty": (pcodes.isna() | pcodes.map(is_empty)).sum().sum(),
            "pcode_not_iso2": pcodes.map(not_iso2).sum().sum(),
            "pcode_not_alnum": pcodes.map(not_alnum).sum().sum(),
            "pcode_lengths": 0,
            "pcode_duplicated": 0,
            "pcode_not_nested": 0,
        }
        pcode_self = f"ADM{admin_level}_PCODE"
        pcode_parent = f"ADM{admin_level-1}_PCODE"
        if pcode_self in pcode_columns:
            self_series = pcodes[pcode_self]
            series = self_series[~self_series.isna() & ~self_series.map(is_empty)]
            row["pcode_lengths"] = series.map(len).nunique()
            row["pcode_duplicated"] = series.duplicated().sum()
            if pcode_parent in pcode_columns:
                row["pcode_not_nested"] = pcodes.apply(
                    lambda row, pcode_self=pcode_self, pcode_parent=pcode_parent: (
                        not row[pcode_self].startswith(row[pcode_parent])
                        if row[pcode_self]
                        and row[pcode_self].strip()
                        and row[pcode_parent]
                        and row[pcode_parent].strip()
                        else False
                    ),
                    axis=1,
                ).sum()
        check_results.append(row)
    return check_results
