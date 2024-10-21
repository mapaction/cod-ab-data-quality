from hdx.location.country import Country
from icu import USET_ADD_CASE_MAPPINGS, LocaleData, ULocaleDataExemplarSetType
from langcodes import tag_is_valid

from src.config import m49, unterm


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


official_langs = ["ar", "en", "es", "fr", "ru", "zh"]

auxiliary_codes = {
    "ar-TUN": get_aux_codes("ar"),
    "en-CHN": get_aux_codes("en"),
    "en-PHL": get_aux_codes("en"),
    "en-ZAF": get_aux_codes("en"),
    "es-PAN": get_aux_codes("es"),
    "fa-IRN": get_aux_codes("fa"),
    "ht-HTI": get_aux_codes("ht"),
    "hy-ARM": get_aux_codes("hy"),
    "ky-KGZ": [*get_aux_codes("ky"), "U+04C9", "U+04CA"],
    "my-MMR": [*get_aux_codes("my"), "U+104A", "U+200B"],
    "pt-BRA": get_aux_codes("pt"),
    "si-LKA": get_aux_codes("si"),
    "tr-TUR": get_aux_codes("tr"),
    "vi-VNM": [*get_aux_codes("vi"), "U+0300", "U+0301"],
}
exception_lang = ["zh"]

number_codes = [f"U+{ord(str(n)):04X}" for n in range(10)]  # U+0030-0039
punctuation_codes = [
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
    *number_codes,
    "U+003A",
]
punctuation_set = [chr(int(x[2:], 16)) for x in punctuation_codes]


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
    ] + [chr(int(x[2:], 16)) for x in auxiliary_codes.get(f"{lang}-{iso3}", [])]


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
    return "".join({char for char in name if char not in char_set + punctuation_set})


def is_invalid_adm0(column: str, name: str | None, iso3: str) -> bool:
    """Checks if Admin 0 name is invalid.

    Args:
        column: Admin 0 column to check.
        name: value of column.
        iso3: ISO-3 country code.

    Returns:
        True if name doesn't match the official UN name from UNTERM.
    """
    lang = column.split("_")[1].lower()
    if iso3 in unterm:
        return name != unterm[iso3][f"{lang}_short"]
    if iso3 in m49:
        return name != m49[iso3][f"{lang}_short"]
    if lang == "en":
        return name != Country.get_country_name_from_iso3(iso3)
    return False


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
    return any(char not in char_set + punctuation_set for char in name)


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
