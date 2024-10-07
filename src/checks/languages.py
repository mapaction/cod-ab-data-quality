from math import inf
from re import compile

from geopandas import GeoDataFrame
from langcodes import Language

from src.config import CheckReturnList


def get_langs(gdf: GeoDataFrame, admin_level: int) -> list[str]:
    """Gets a list of language codes.

    Args:
        gdf: Current layer's GeoDataFrame.
        admin_level: Current layer's admin level.

    Returns:
        _description_
    """
    columns = list(gdf.columns)
    p = compile(rf"^ADM{admin_level}_\w{{2}}$")
    langs = [x.split("_")[1].lower() for x in columns if p.search(x)]
    return list(dict.fromkeys(langs))


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Checks for which languages are used within dataset.

    Datasets use the following pattern in their field names for identifying languages:
    "ADM{LEVEL}_{LANGUAGE_CODE}". For example, a dataset containing English, French,
    and Haitian Creole for admin level 1 would have the following field names:
    ADM1_EN, ADM1_FR, ADM1_HT. Regex is used to identify field names, this may pick up
    columns such as identification fields if they are named like ADM1_ID. However, this
    would be a valid column if it was used for Indonesian names.

    The following are a list of source and output columns:
    - source: "ADM{LEVEL}_{LANGUAGE_CODE}"
        - output: "language_count", "language_1", "language_2", "language_3", etc...

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of results to output as a CSV.
    """
    check_results = []
    language_min = inf
    language_max = -inf
    for admin_level, gdf in enumerate(gdfs):
        lang_count = len(get_langs(gdf, admin_level))
        if lang_count:
            language_min = min(language_min, lang_count)
            language_max = max(language_max, lang_count)
    if language_min == inf:
        language_min = None
        language_max = None
    for admin_level, gdf in enumerate(gdfs):
        row = {
            "iso3": iso3,
            "level": admin_level,
            "language_min": language_min,
            "language_max": language_max,
            "language_count": 0,
            "language_invalid": 0,
        }
        langs = get_langs(gdf, admin_level)
        for index, lang in enumerate(langs):
            row["language_count"] += 1
            row[f"language_{index+1}"] = lang
            if not Language.get(lang).is_valid():
                row["language_invalid"] += 1
        check_results.append(row)
    return check_results
