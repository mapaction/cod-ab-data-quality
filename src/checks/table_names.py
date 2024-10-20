from re import match

from geopandas import GeoDataFrame

from src.config import CheckReturnList
from src.utils import is_empty

from .table_names_utils import (
    get_invalid_chars,
    has_double_spaces,
    has_strippable_spaces,
    is_invalid,
    is_lower,
    is_punctuation,
    is_upper,
)


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
        names = gdf[name_columns]
        invalid_chars = "".join(
            {
                names[col].map(lambda x, col=col: get_invalid_chars(col, x, iso3)).sum()
                for col in name_columns
            },
        )
        row = {
            "iso3": iso3,
            "level": admin_level,
            "name_column_levels": sum(
                [
                    any(
                        bool(match(rf"^ADM{level}_[A-Z][A-Z]$", column))
                        for column in gdf.columns
                    )
                    for level in range(admin_level + 1)
                ],
            ),
            "name_column_count": len(name_columns),
            "name_cell_count": max(names.size, 1),
            "name_empty": (names.isna() | names.map(is_empty)).sum().sum(),
            "name_spaces_strip": sum(
                [names[col].map(has_strippable_spaces).sum() for col in name_columns],
            ),
            "name_spaces_double": sum(
                [names[col].map(has_double_spaces).sum() for col in name_columns],
            ),
            "name_upper": sum(
                [names[col].map(is_upper).sum() for col in name_columns],
            ),
            "name_lower": sum(
                [names[col].map(is_lower).sum() for col in name_columns],
            ),
            "name_no_valid": sum(
                [
                    names[col]
                    .map(lambda x, col=col: is_punctuation(col, x, iso3))
                    .sum()
                    for col in name_columns
                ],
            ),
            "name_invalid": sum(
                [
                    names[col].map(lambda x, col=col: is_invalid(col, x, iso3)).sum()
                    for col in name_columns
                ],
            ),
            "name_invalid_char_count": len({*list(invalid_chars)}),
            "name_invalid_chars": ",".join(
                sorted({f"U+{ord(x):04X}" for x in invalid_chars}),
            ),
        }
        check_results.append(row)
    return check_results
