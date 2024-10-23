from hdx.location.country import Country
from icu import USET_ADD_CASE_MAPPINGS, LocaleData, ULocaleDataExemplarSetType
from langcodes import tag_is_valid

from src.config import m49, official_languages, unterm

from .table_names_config import auxiliary_codes, exclude_check, punctuation_set


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
    if not name or not name.strip() or not tag_is_valid(lang) or lang in exclude_check:
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
    if lang not in official_languages:
        return False
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
    if not name or not name.strip() or not tag_is_valid(lang) or lang in exclude_check:
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
