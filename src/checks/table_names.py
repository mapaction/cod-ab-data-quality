from re import match

from geopandas import GeoDataFrame
from icu import USET_ADD_CASE_MAPPINGS, LocaleData, ULocaleDataExemplarSetType
from langcodes import tag_is_valid

from src.config import CheckReturnList
from src.utils import is_empty

exception_codes = {
    "ar": ["U+0640"],
    "ht": ["U+00F2"],
    "hy": ["U+0587"],
    "my": [
        "U+1040",
        "U+1041",
        "U+1042",
        "U+1043",
        "U+1044",
        "U+1045",
        "U+1046",
        "U+1047",
        "U+1048",
        "U+1049",
        "U+104A",
    ],
    "pt": ["U+00FC"],
    "tr": ["U+00C2", "U+00E2"],
    "vi": ["U+004A", "U+006A", "U+0300", "U+0301"],
}
exception_lang = ["zh"]

numbers = [f"U+{ord(str(n)):04X}" for n in range(10)]
aux_codes = [
    "U+0020",
    "U+0022",
    "U+0023",
    "U+0026",
    "U+0027",
    "U+0028",
    "U+0029",
    "U+002C",
    "U+002D",
    "U+002E",
    "U+002F",
    "U+003A",
    *numbers,
    "U+200B",
    "U+200C",
    "U+200D",
    "U+200E",
    "U+200F",
]
aux_set = [chr(int(x[2:], 16)) for x in aux_codes]


def get_char_set(lang: str) -> list[str]:
    """Get character set for a language code.

    Args:
        lang: 2 letter language code.

    Returns:
        List of valid characters for a language.
    """
    examplar = LocaleData(lang)
    return [
        x
        for y in examplar.getExemplarSet(
            USET_ADD_CASE_MAPPINGS,
            ULocaleDataExemplarSetType.ES_STANDARD,
        )
        for x in y
    ] + [chr(int(x[2:], 16)) for x in exception_codes.get(lang, [])]


def is_upper(name: str | None) -> bool:
    """Checks if name is all uppercase.

    Args:
        name: Name string.

    Returns:
        True if name is all uppercase.
    """
    if not name or not name.strip():
        return False
    return name == name.upper() and name.lower() != name.upper()


def is_lower(name: str | None) -> bool:
    """Checks if name is all lowercase.

    Args:
        name: Name string.

    Returns:
        True if name is all lowercase.
    """
    if not name or not name.strip():
        return False
    return name == name.lower() and name.lower() != name.upper()


def has_strippable_spaces(name: str | None) -> bool:
    """Checks if string has strippable spaces.

    Args:
        name: string.

    Returns:
        True if name has leading or trailing spaces.
    """
    if not name or not name.strip():
        return False
    return name != name.strip()


def has_double_spaces(name: str | None) -> bool:
    """Checks if string has double spaces.

    Args:
        name: string.

    Returns:
        True if name has double spaces.
    """
    if not name or not name.strip():
        return False
    return "  " in name


def is_punctuation(column: str, name: str | None) -> bool:
    """Check if a value within a column is a valid name based on it's language code.

    Args:
        column: column to check.
        name: value of column.

    Returns:
        True if there are any characters in the name not found in the languages's
        character set.
    """
    lang = column.split("_")[1].lower()
    if not name or not name.strip() or not tag_is_valid(lang):
        return False
    char_set = get_char_set(lang)
    return all(char not in char_set for char in name)


def is_invalid(column: str, name: str | None) -> bool:
    """Check if a value within a column is a valid name based on it's language code.

    Args:
        column: column to check.
        name: value of column.

    Returns:
        True if there are any characters in the name not found in the languages's
        character set.
    """
    lang = column.split("_")[1].lower()
    if not name or not name.strip() or not tag_is_valid(lang) or lang in exception_lang:
        return False
    char_set = get_char_set(lang)
    return any(char not in char_set + aux_set for char in name)


def get_illegal_chars(column: str, name: str | None) -> str:
    """Check if a value within a column is a valid name based on it's language code.

    Args:
        column: column to check.
        name: value of column.

    Returns:
        True if there are any characters in the name not found in the languages's
        character set.
    """
    lang = column.split("_")[1].lower()
    if not name or not name.strip() or not tag_is_valid(lang) or lang in exception_lang:
        return ""
    char_set = get_char_set(lang)
    return "".join({char for char in name if char not in char_set + aux_set})


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
        illegal_chars = "".join(
            {
                names[col].map(lambda x, col=col: get_illegal_chars(col, x)).sum()
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
                    names[col].map(lambda x, col=col: is_punctuation(col, x)).sum()
                    for col in name_columns
                ],
            ),
            "name_invalid": sum(
                [
                    names[col].map(lambda x, col=col: is_invalid(col, x)).sum()
                    for col in name_columns
                ],
            ),
            "name_illegal_char_count": len({*list(illegal_chars)}),
            "name_illegal_chars": ",".join(
                sorted({f"U+{ord(x):04X}" for x in illegal_chars}),
            ),
        }
        check_results.append(row)
    return check_results
