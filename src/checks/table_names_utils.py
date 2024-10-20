from icu import USET_ADD_CASE_MAPPINGS, LocaleData, ULocaleDataExemplarSetType
from langcodes import tag_is_valid


def get_aux_codes(lang: str) -> list[str]:
    """Gets auxiliary characters for a language.

    Args:
        lang: 2 letter language code.

    Returns:
        List of auxiliary codes in U+0000 format.
    """
    return [
        f"U+{ord(x):04X}"
        for y in LocaleData(lang).getExemplarSet(
            USET_ADD_CASE_MAPPINGS,
            ULocaleDataExemplarSetType.ES_AUXILIARY,
        )
        for x in y
    ]


exception_codes = {
    "en-CHN": get_aux_codes("en"),
    "en-PHL": get_aux_codes("en"),
    "en-ZAF": get_aux_codes("en"),
    "es-PAN": get_aux_codes("es"),
    "ht-HTI": get_aux_codes("ht"),
    "hy-ARM": get_aux_codes("hy"),
    "ky-KGZ": [*get_aux_codes("ky"), "U+04C9", "U+04CA"],
    "my-MMR": [*get_aux_codes("my"), "U+104A"],
    "pt-BRA": get_aux_codes("pt"),
    "tr-TUR": get_aux_codes("tr"),
    "vi-VNM": [*get_aux_codes("vi"), "U+0300", "U+0301"],
}
exception_lang = ["zh"]

numbers = [f"U+{ord(str(n)):04X}" for n in range(10)]  # U+0030-0039
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
    *numbers,
    "U+003A",
    "U+0640",
    "U+200B",
    "U+200C",
    "U+200D",
    "U+200E",
    "U+200F",
]
aux_set = [chr(int(x[2:], 16)) for x in aux_codes]


def get_char_set(lang: str, iso3: str) -> list[str]:
    """Get character set for a language code.

    Args:
        lang: 2 letter language code.
        iso3: ISO-3 country code.

    Returns:
        List of valid characters for a language.
    """
    return [
        x
        for y in LocaleData(lang).getExemplarSet(
            USET_ADD_CASE_MAPPINGS,
            ULocaleDataExemplarSetType.ES_STANDARD,
        )
        for x in y
    ] + [chr(int(x[2:], 16)) for x in exception_codes.get(f"{lang}-{iso3}", [])]


def get_invalid_chars(column: str, name: str | None, iso3: str) -> str:
    """Check if a value within a column is a valid name based on it's language code.

    Args:
        column: column to check.
        name: value of column.
        iso3: ISO-3 country code.

    Returns:
        True if there are any characters in the name not found in the languages's
        character set.
    """
    lang = column.split("_")[1].lower()
    if not name or not name.strip() or not tag_is_valid(lang) or lang in exception_lang:
        return ""
    char_set = get_char_set(lang, iso3)
    return "".join({char for char in name if char not in char_set + aux_set})


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


def is_punctuation(column: str, name: str | None, iso3: str) -> bool:
    """Check if a value within a column is a valid name based on it's language code.

    Args:
        column: column to check.
        name: value of column.
        iso3: ISO-3 country code.

    Returns:
        True if there are any characters in the name not found in the languages's
        character set.
    """
    lang = column.split("_")[1].lower()
    if not name or not name.strip() or not tag_is_valid(lang):
        return False
    char_set = get_char_set(lang, iso3)
    return all(char not in char_set for char in name)


def is_invalid(column: str, name: str | None, iso3: str) -> bool:
    """Check if a value within a column is a valid name based on it's language code.

    Args:
        column: column to check.
        name: value of column.
        iso3: ISO-3 country code.

    Returns:
        True if there are any characters in the name not found in the languages's
        character set.
    """
    lang = column.split("_")[1].lower()
    if not name or not name.strip() or not tag_is_valid(lang) or lang in exception_lang:
        return False
    char_set = get_char_set(lang, iso3)
    return any(char not in char_set + aux_set for char in name)


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
