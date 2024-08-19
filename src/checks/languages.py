"""Check for validating dates."""

from re import compile

from geopandas import GeoDataFrame


def main(result: list, iso3: str, gdfs: list[GeoDataFrame]):
    for level, gdf in enumerate(gdfs):
        row = {"iso3": iso3, "level": level}
        columns = list(gdf.columns)
        p = compile(rf"^ADM{level}_\w{{2}}$")
        langs = [x.split("_")[1].lower() for x in columns if p.search(x)]
        langs = list(dict.fromkeys(langs))
        for index, lang in enumerate(langs):
            row[f"lang_{index+1}"] = lang
        result.append(row)
