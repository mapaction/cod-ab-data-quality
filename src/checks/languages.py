"""Check for summarizing language info."""

from re import compile

from geopandas import GeoDataFrame

from src.config import CheckReturnList


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
        - output: "lang_1", "lang_2", "lang_3", etc...

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of results to output as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        row = {"iso3": iso3, "level": admin_level}
        columns = list(gdf.columns)
        p = compile(rf"^ADM{admin_level}_\w{{2}}$")
        langs = [x.split("_")[1].lower() for x in columns if p.search(x)]
        langs = list(dict.fromkeys(langs))
        for index, lang in enumerate(langs):
            row[f"lang_{index+1}"] = lang
        check_results.append(row)
    return check_results
